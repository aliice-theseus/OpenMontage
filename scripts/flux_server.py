"""FLUX 模型常驻推理服务器 — 一次加载，持续服务。

用法:
  python scripts/flux_server.py start              # 单卡模式（默认）
  python scripts/flux_server.py start --num-gpus 6 # 多卡模式

环境变量:
  FLUX2_MODEL_PATH  — 模型路径（默认 /home/roy/.cache/...）
  FLUX_SERVER_PORT  — 端口号（默认 19530）
"""

from __future__ import annotations

import argparse, base64, io, json, os, socket, struct, sys, time, threading
from pathlib import Path
from PIL import Image

MODEL_PATH = os.environ.get(
    "FLUX2_MODEL_PATH",
    "/home/roy/.cache/modelscope/Black-Forest-Labs/FLUX.2-dev/",
)
PORT = int(os.environ.get("FLUX_SERVER_PORT", "19530"))
SOCKET_PATH = f"/tmp/flux_server_{PORT}.sock"

# ── 模型管理 ──────────────────────────────────────────────

_pipe = None
_lock = threading.Lock()
_NUM_GPUS = 1


# ── 多卡分发策略（来自 ~/flux2_6gpu.py）──────────────

def _build_transformer_device_map(num_gpus: int) -> dict:
    dm = {}
    dm.update({k: 0 for k in [
        'time_guidance_embed', 'x_embedder', 'norm_out', 'proj_out',
    ]})
    dm.update({k: 1 for k in [
        'double_stream_modulation_img', 'double_stream_modulation_txt',
        'single_stream_modulation', 'context_embedder',
    ]})
    double_per_gpu = [2, 1, 1, 1, 1, 2]
    if num_gpus < 6:
        double_per_gpu = [8 // num_gpus + (1 if i < 8 % num_gpus else 0) for i in range(num_gpus)]
    idx = 0
    for gpu_id, count in enumerate(double_per_gpu):
        for _ in range(count):
            dm[f'transformer_blocks.{idx}'] = gpu_id
            idx += 1
    single_per_gpu = 48 // num_gpus
    remain = 48 % num_gpus
    for i in range(48):
        gpu = i // (single_per_gpu + 1) if i < remain * (single_per_gpu + 1) else (i - remain) // single_per_gpu
        if gpu >= num_gpus:
            gpu = num_gpus - 1
        dm[f'single_transformer_blocks.{i}'] = gpu
    return dm


def _build_text_encoder_device_map(num_gpus: int) -> dict:
    dm = {}
    dm.update({k: 0 for k in [
        'model.vision_tower', 'model.multi_modal_projector',
    ]})
    dm['model.language_model.embed_tokens'] = min(1, num_gpus - 1)
    num_layers = 40
    base = num_layers // num_gpus
    rem = num_layers % num_gpus
    idx = 0
    for gpu_id in range(num_gpus):
        count = base + (1 if gpu_id < rem else 0)
        for _ in range(count):
            dm[f'model.language_model.layers.{idx}'] = gpu_id
            idx += 1
    dm.update({k: num_gpus - 1 for k in [
        'model.language_model.norm', 'model.language_model.rotary_emb', 'lm_head',
    ]})
    return dm


def load_model(num_gpus: int = 1):
    global _pipe, _NUM_GPUS
    if _pipe is not None:
        return _pipe
    _NUM_GPUS = num_gpus
    t0 = time.time()
    print(f"[flux_server] Loading model on {num_gpus} GPU(s) from {MODEL_PATH}...", flush=True)
    import torch
    from diffusers import Flux2Pipeline
    from accelerate import dispatch_model
    import torch, os
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    _pipe = Flux2Pipeline.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    if num_gpus <= 1:
        _pipe.enable_sequential_cpu_offload()
        used = torch.cuda.memory_allocated(0) / 1024**3
    else:
        dispatch_model(_pipe.transformer, device_map=_build_transformer_device_map(num_gpus))
        dispatch_model(_pipe.text_encoder, device_map=_build_text_encoder_device_map(num_gpus))
        _pipe.vae = _pipe.vae.to("cuda:0")
        used = sum((torch.cuda.memory_allocated(i) for i in range(num_gpus))) / 1024**3
    torch.cuda.empty_cache()
    print(f"[flux_server] Model ready in {time.time()-t0:.0f}s (total ~{used:.1f} GiB)", flush=True)
    if num_gpus > 1:
        for i in range(num_gpus):
            free, total = torch.cuda.mem_get_info(i)
            used_i = (total - free) / 1024**3
            print(f"  GPU {i}: {used_i:.1f}/{total/1024**3:.0f} GiB", flush=True)
    return _pipe


def generate(prompt: str, **kwargs) -> bytes:
    pipe = load_model(kwargs.get("num_gpus", _NUM_GPUS))
    width = kwargs.get("width", 1024)
    height = kwargs.get("height", 576)
    steps = kwargs.get("steps", 20)
    guidance = kwargs.get("guidance", 3.5)
    seed = kwargs.get("seed", None)

    gen = None
    if seed is not None:
        import torch
        gen = torch.Generator(device="cuda").manual_seed(seed)

    import torch
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    with torch.no_grad():
        pipe.set_progress_bar_config(disable=True)
        result = pipe(
            prompt=prompt,
            width=width, height=height,
            num_inference_steps=steps,
            guidance_scale=guidance,
            generator=gen,
        )
    img = result.images[0]
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ── 服务端（常驻） ──────────────────────────────────────────

def _handle_request(conn):
    try:
        raw_len = conn.recv(4)
        if not raw_len:
            return
        msg_len = struct.unpack("!I", raw_len)[0]
        raw_msg = b""
        while len(raw_msg) < msg_len:
            chunk = conn.recv(msg_len - len(raw_msg))
            if not chunk:
                return
            raw_msg += chunk
        req = json.loads(raw_msg.decode("utf-8"))

        prompt = req.get("prompt", "")
        img_bytes = generate(prompt, **req.get("params", {}))

        resp = json.dumps({"success": True, "size": len(img_bytes)}).encode("utf-8")
        conn.sendall(struct.pack("!I", len(resp)))
        conn.sendall(resp)
        conn.sendall(struct.pack("!I", len(img_bytes)))
        conn.sendall(img_bytes)
    except Exception as e:
        try:
            resp = json.dumps({"success": False, "error": str(e)}).encode("utf-8")
            conn.sendall(struct.pack("!I", len(resp)))
            conn.sendall(resp)
        except Exception:
            pass


def run_server(num_gpus: int = 1):
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)
    load_model(num_gpus)  # 预热
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(16)
    print(f"[flux_server] Listening on {SOCKET_PATH}", flush=True)
    while True:
        conn, _ = server.accept()
        threading.Thread(target=_handle_request, args=(conn,), daemon=True).start()


# ── 客户端 ──────────────────────────────────────────────────

def send_request(prompt: str, **params) -> tuple[bool, bytes | str]:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(120)
    try:
        sock.connect(SOCKET_PATH)
    except FileNotFoundError:
        return False, "Server not running. Start with: python scripts/flux_server.py start"
    req = json.dumps({"prompt": prompt, "params": params}).encode("utf-8")
    sock.sendall(struct.pack("!I", len(req)))
    sock.sendall(req)

    raw_len = sock.recv(4)
    resp_len = struct.unpack("!I", raw_len)[0]
    raw_resp = b""
    while len(raw_resp) < resp_len:
        raw_resp += sock.recv(resp_len - len(raw_resp))
    resp = json.loads(raw_resp.decode("utf-8"))
    if not resp["success"]:
        return False, resp.get("error", "unknown")

    raw_len = sock.recv(4)
    img_len = struct.unpack("!I", raw_len)[0]
    img_bytes = b""
    while len(img_bytes) < img_len:
        img_bytes += sock.recv(img_len - len(img_bytes))
    return True, img_bytes


# ── CLI ────────────────────────────────────────────────────

def cli():
    parser = argparse.ArgumentParser(description="FLUX 模型常驻推理服务器")
    sub = parser.add_subparsers(dest="cmd")

    start_p = sub.add_parser("start", help="启动常驻服务")
    start_p.add_argument("--port", type=int, default=PORT)
    start_p.add_argument("--num-gpus", type=int, default=1, help="多卡分发（默认1，6=全卡）")

    gen_p = sub.add_parser("generate", help="生成一张图片")
    gen_p.add_argument("--prompt", required=True)
    gen_p.add_argument("--output", "-o", default="output.png")
    gen_p.add_argument("--width", type=int, default=1024)
    gen_p.add_argument("--height", type=int, default=576)
    gen_p.add_argument("--steps", type=int, default=20)
    gen_p.add_argument("--guidance", type=float, default=3.5)
    gen_p.add_argument("--seed", type=int)

    args = parser.parse_args()
    if args.cmd == "start":
        run_server(num_gpus=args.num_gpus)
    elif args.cmd == "generate":
        t0 = time.time()
        ok, result = send_request(
            args.prompt,
            width=args.width, height=args.height,
            steps=args.steps, guidance=args.guidance,
            seed=args.seed,
        )
        if not ok:
            print(f"Error: {result}", flush=True)
            sys.exit(1)
        Path(args.output).write_bytes(result)
        print(f"Saved {args.output} ({time.time()-t0:.1f}s)", flush=True)
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
