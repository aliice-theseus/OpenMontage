"""Seedance 2.0 (ByteDance) video generation via 火山引擎 Ark API.

直接调用火山引擎 Ark 上的 Seedance 2.0 模型，遵循 Ark v3 content 协议。
适用于中国大陆网络环境。

⚠️ 提示词语言规则：prompt 必须使用中文编写，仅专业影视术语
（wide shot, close-up, dolly in, the same character 等）允许使用英文。

配置方式：
  1. 设置环境变量 ARK_API_KEY（火山引擎 Ark API Key）
  2. 可选设置环境变量 SEEDANCE_ENDPOINT_ID（推理接入点 ID，有默认值）
  3. 或在调用时通过 model 参数指定 Endpoint ID

Ark API 图片 role 区分：
  first_frame     — 首帧锁定，模型从此帧开始续接（适用于分段视频尾帧衔接）
  reference_image — 多模态参考，模型参考其视觉特征（角色/场景/风格参考）

调用示例（curl）：
  curl -X POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks \\
    -H "Content-Type: application/json" \\
    -H "Authorization: Bearer $ARK_API_KEY" \\
    -d '{
      "model": "ep-20260707160030-dt7sw",
      "content": [
        {"type": "text", "text": "a cat playing piano"},
        {"type": "image_url", "image_url": {"url": "https://..."}, "role": "first_frame"},
        {"type": "image_url", "image_url": {"url": "https://..."}, "role": "reference_image"}
      ],
      "ratio": "16:9",
      "duration": 5,
      "generate_audio": true,
      "watermark": false
    }'
"""

from __future__ import annotations

import base64
import io
import os
import time
from pathlib import Path
from typing import Any

# 参考图最大尺寸（宽×高），超出则等比例缩放到此范围
REFERENCE_IMAGE_MAX_WIDTH = 1280
REFERENCE_IMAGE_MAX_HEIGHT = 720

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)

# 默认火山引擎 Ark API 地址
ARK_API_BASE = "https://ark.cn-beijing.volces.com/api/v3"
# 默认推理接入点 Endpoint ID（用户可通过环境变量 SEEDANCE_ENDPOINT_ID 覆盖）
DEFAULT_ENDPOINT_ID = "ep-20260707160030-dt7sw"


class SeedanceVideo(BaseTool):
    name = "seedance_video"
    version = "0.3.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "seedance"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = []
    install_instructions = (
        "Set ARK_API_KEY to your 火山引擎 Ark API key.\n"
        "  Get one at https://console.volcengine.com/ark\n"
        "Optionally set SEEDANCE_ENDPOINT_ID to specify the inference endpoint ID."
    )
    agent_skills = ["seedance-2-0", "ai-video-gen"]

    capabilities = ["text_to_video", "image_to_video", "reference_to_video"]
    supports = {
        "text_to_video": True,          # content 只有 text
        "image_to_video": True,         # content 含 image_url
        "reference_to_video": True,     # content 含 image/video/audio_url
        "multiple_reference_images": True,
        "reference_image": True,
        "native_audio": True,
        "cinematic_quality": True,
        "camera_direction": True,
        "lip_sync": True,
        "multi_shot": True,
        "aspect_ratio": True,
        "seed": True,
    }
    best_for = [
        "preferred video gen in China when ARK_API_KEY is available",
        "cinematic trailers, teasers, and high-fidelity clips with native synchronized audio",
        "director-level camera control and multi-shot editing in a single generation",
        "lip-sync from quoted dialogue in prompts",
        "reference-conditioned generation (up to 9 total reference images + 3 video clips + 3 audio clips)",
        "consistent character identity across shots",
        "direct connection via 火山引擎 Ark",
    ]
    not_good_for = ["offline generation", "budget-constrained projects"]
    fallback_tools = ["wan_video"]
    # Premium model — beat out "experimental stability" baseline. The scoring
    # engine reads quality_score directly when present (see lib/scoring.py).
    quality_score = 0.95

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string", "description": "视频内容描述/提示词（必须用中文，仅专业影视术语可用英文）"},
            "model": {
                "type": "string",
                "default": DEFAULT_ENDPOINT_ID,
                "description": "火山引擎 Ark 推理接入点 Endpoint ID（覆盖 SEEDANCE_ENDPOINT_ID 环境变量）",
            },
            "duration": {
                "type": "integer",
                "minimum": 4,
                "maximum": 15,
                "default": 5,
                "description": "视频时长（秒）",
            },
            "ratio": {
                "type": "string",
                "enum": ["16:9", "9:16", "4:3", "3:4", "1:1", "21:9"],
                "default": "16:9",
                "description": "画幅宽高比",
            },
            "resolution": {
                "type": "string",
                "enum": ["480p", "720p", "1080p"],
                "default": "720p",
                "description": "输出分辨率",
            },
            "generate_audio": {
                "type": "boolean",
                "default": True,
                "description": "是否生成与画面对齐的音频",
            },
            "watermark": {
                "type": "boolean",
                "default": False,
                "description": "是否添加水印",
            },
            # ----- 首帧/单张图片输入（兼容 video_selector 路由，计入 9 张总数） -----
            "image_url": {
                "type": "string",
                "description": "首帧图片 URL（Ark API role: first_frame，用于视频续接；计入 9 张参考图总数，自动缩放至 1280×720 以内）",
            },
            "image_path": {
                "type": "string",
                "description": "本地首帧图片路径（Ark API role: first_frame，用于视频续接；计入 9 张参考图总数，自动缩放至 1280×720 以内）",
            },
            # ----- 多参考素材输入（用于 reference_to_video） -----
            "reference_image_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "多模态参考图片 URL 列表（Ark API role: reference_image，用于角色/场景/风格参考；与首帧合计不超过 9 张，自动缩放至 1280×720 以内）",
            },
            "reference_image_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "多模态参考图片路径列表（Ark API role: reference_image；与首帧合计不超过 9 张，自动缩放至 1280×720 以内）",
            },
            "reference_video_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "参考视频 URL 列表，最多 3 个",
            },
            "reference_audio_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "参考音频 URL 列表，最多 3 个",
            },
            "require_identity_lock": {
                "type": "boolean",
                "default": False,
                "description": "强制角色身份锁。设为 true 时，建议通过 reference_image_urls/paths 传入四视图参考图；"
                               "未传入时会提示用户确认，经用户批准后可通过 _confirm_skip_identity_lock=true 继续。",
            },
            "_confirm_skip_identity_lock": {
                "type": "boolean",
                "default": False,
                "description": "内部标记。用户确认跳过角色身份锁、以纯 text_to_video 继续时设为 true。",
            },
            # ----- 其他 -----
            "seed": {
                "type": "integer",
                "description": "随机种子，用于可复现的生成",
            },
            "output_path": {
                "type": "string",
                "description": "输出视频文件路径",
            },
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=500, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=2, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["prompt", "model", "duration", "ratio", "seed"]
    side_effects = ["writes video file to output_path", "calls 火山引擎 Ark API"]
    user_visible_verification = [
        "Watch generated clip for motion coherence, audio sync, and visual quality"
    ]

    # ------------------------------------------------------------------ #
    #  配置方法
    # ------------------------------------------------------------------ #

    def _get_api_key(self) -> str | None:
        return os.environ.get("ARK_API_KEY")

    def _get_endpoint_id(self) -> str:
        """返回 Endpoint ID，优先级：环境变量 > 类默认值。"""
        return os.environ.get("SEEDANCE_ENDPOINT_ID") or DEFAULT_ENDPOINT_ID

    def get_status(self) -> ToolStatus:
        if self._get_api_key():
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    # ------------------------------------------------------------------ #
    #  成本与耗时估算
    # ------------------------------------------------------------------ #

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        """火山引擎 Ark Seedance 2.0 国内定价约 0.5元/秒，按时长和分辨率估算。"""
        duration = inputs.get("duration", 5)
        resolution = inputs.get("resolution", "720p")
        # 粗略估算（CNY）：时长 x 分辨率系数
        res_factor = 1.5 if resolution == "1080p" else 1.0 if resolution == "720p" else 0.7
        return round(0.50 * duration * res_factor, 2)

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        """通常 5 秒视频约 60-120 秒，10 秒视频约 120-180 秒。"""
        duration = inputs.get("duration", 5)
        return 60.0 + float(duration) * 8.0

    # ------------------------------------------------------------------ #
    #  辅助方法
    # ------------------------------------------------------------------ #

    @staticmethod
    def _resize_to_max(image_path: str, max_w: int = REFERENCE_IMAGE_MAX_WIDTH, max_h: int = REFERENCE_IMAGE_MAX_HEIGHT) -> bytes:
        """将图片等比例缩放到不超过 max_w × max_h，返回编码后的图片字节。

        使用 Pillow 做高质量缩放（LANCZOS），PNG 输入转 JPEG 输出以减小 data URI 体积。
        若图片本身已在范围内，则直接读取原文件字节（不做重编码以避免质量损失）。

        Args:
            image_path: 本地图片路径。
            max_w: 最大宽度。
            max_h: 最大高度。

        Returns:
            缩放后的图片字节（JPEG 编码）。
        """
        from PIL import Image as PILImage

        img = PILImage.open(image_path)
        orig_w, orig_h = img.size

        # 若已在范围内，直接返回原始字节（不做无损→有损转换）
        if orig_w <= max_w and orig_h <= max_h:
            with open(image_path, "rb") as f:
                return f.read()

        # 等比例缩放
        ratio = min(max_w / orig_w, max_h / orig_h)
        new_w = int(orig_w * ratio)
        new_h = int(orig_h * ratio)
        resized = img.resize((new_w, new_h), PILImage.LANCZOS)

        buf = io.BytesIO()
        # 统一输出为 JPEG 以减小体积
        resized.convert("RGB").save(buf, format="JPEG", quality=92)
        return buf.getvalue()

    @staticmethod
    def _download_image(url: str, timeout: int = 30) -> bytes:
        """下载远程图片到内存。"""
        import requests
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.content

    def _process_image_to_data_uri(self, path_or_url: str) -> str:
        """将图片（本地路径或远程 URL）缩放到 1280×720 以内后转为 data URI。

        已为 data URI 的图片直接透传（已在之前被处理过）。
        优先处理本地路径；若为 http(s):// 开头则先下载再缩放。
        """
        # data URI → 已处理过，直接透传
        if path_or_url.startswith("data:"):
            return path_or_url

        is_url = path_or_url.startswith(("http://", "https://"))
        if is_url:
            # 远程 URL → 下载到内存 → 缩放到临时文件 → data URI
            raw = self._download_image(path_or_url)
            tmp_dir = Path(self._get_output_dir()) / ".ref_resized"
            tmp_dir.mkdir(parents=True, exist_ok=True)
            tmp_path = tmp_dir / f"ref_{hash(path_or_url)}.jpg"
            if not tmp_path.exists():
                from PIL import Image as PILImage
                buf = io.BytesIO(raw)
                img = PILImage.open(buf)
                orig_w, orig_h = img.size
                if orig_w <= REFERENCE_IMAGE_MAX_WIDTH and orig_h <= REFERENCE_IMAGE_MAX_HEIGHT:
                    # 已在范围内，直接保存原格式
                    tmp_path.write_bytes(raw)
                else:
                    ratio = min(REFERENCE_IMAGE_MAX_WIDTH / orig_w, REFERENCE_IMAGE_MAX_HEIGHT / orig_h)
                    new_w = int(orig_w * ratio)
                    new_h = int(orig_h * ratio)
                    resized = img.resize((new_w, new_h), PILImage.LANCZOS)
                    resized.convert("RGB").save(str(tmp_path), format="JPEG", quality=92)
            return self._file_to_data_uri(str(tmp_path))
        else:
            # 本地路径 → 直接缩放
            resized_bytes = self._resize_to_max(path_or_url)
            b64 = base64.b64encode(resized_bytes).decode("ascii")
            return f"data:image/jpeg;base64,{b64}"

    def _get_output_dir(self) -> str:
        """获取当前执行的基础输出目录（用于存放临时文件），默认为 './.seedance_tmp'。"""
        # 尝试从 inputs 上下文中获取，但在 _build_content_array 阶段不易获取，
        # 使用类级别或进程级临时目录
        tmp = Path("./.seedance_tmp")
        tmp.mkdir(parents=True, exist_ok=True)
        return str(tmp)

    @staticmethod
    def _file_to_data_uri(path: str) -> str:
        """将本地文件转为 data URI（不缩放，仅转换）。"""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"文件不存在: {path}")
        suffix = p.suffix.lower().lstrip(".")
        mime_map = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "webp": "image/webp",
            "gif": "image/gif",
            "mp4": "video/mp4",
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "m4a": "audio/mp4",
        }
        mime = mime_map.get(suffix, "application/octet-stream")
        data = p.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:{mime};base64,{b64}"

    def _build_content_array(self, inputs: dict[str, Any]) -> list[dict]:
        """根据输入参数构建火山引擎 Ark 的 content 数组。

        Ark API 的 content 数组结构（遵循火山引擎 v3 协议）：
        [
          {"type": "text", "text": "提示词"},
          # 首帧锁定（用于视频衔接，从前一段的尾帧提取）
          {"type": "image_url", "image_url": {"url": "..."}, "role": "first_frame"},
          # 多模态参考图（角色四视图、场景关键帧、风格参考等）
          {"type": "image_url", "image_url": {"url": "..."}, "role": "reference_image"},
          {"type": "video_url", "video_url": {"url": "..."}, "role": "reference_video"},
          {"type": "audio_url", "audio_url": {"url": "..."}, "role": "reference_audio"},
        ]

        role 区分：
          first_frame     — 首帧图（图生视频/视频衔接用），模型从此帧开始续接
          last_frame      — 尾帧图（图生视频首尾帧用）
          reference_image — 多模态参考图（角色/场景/风格参考），模型参考其视觉特征

        ⚠️  Seedance 2.0 所有参考图片（first_frame + reference_image）合计不得超过 9 张。
        """
        content: list[dict] = [
            {"type": "text", "text": inputs.get("prompt", "")}
        ]

        # --------------------------------------------------------------- #
        # 收集参考图片，区分 role 并统一计数（合计 ≤ 9）
        # 所有图片均自动缩放到 1280×720 以内（等比例）
        # --------------------------------------------------------------- #
        first_frame_uri: str | None = None
        ref_image_uris: list[str] = []

        # 1. 首帧图（来自 image_url / image_path，通常为前一段视频的尾帧）
        raw_image_url = inputs.get("image_url")
        if not raw_image_url and inputs.get("image_path"):
            first_frame_uri = self._process_image_to_data_uri(inputs["image_path"])
        elif raw_image_url:
            first_frame_uri = self._process_image_to_data_uri(raw_image_url)

        # 2. 多模态参考图（角色四视图、场景关键帧、风格参考等）
        for url in inputs.get("reference_image_urls") or []:
            ref_image_uris.append(self._process_image_to_data_uri(url))
        for local_path in inputs.get("reference_image_paths") or []:
            ref_image_uris.append(self._process_image_to_data_uri(local_path))

        # 3. 统一检查上限（首帧 + 参考图合计 ≤ 9）
        total_images = (1 if first_frame_uri else 0) + len(ref_image_uris)
        if total_images > 9:
            raise ValueError(
                f"Seedance 2.0 最多接受 9 张参考图片（含首帧），"
                f"收到 {total_images} 张"
            )

        # 4. 按 Ark API 协议写入 content，区分 role
        #    首帧图 → role: "first_frame"（视频续接锚点）
        #    参考图 → role: "reference_image"（多模态视觉参考）
        if first_frame_uri:
            content.append({
                "type": "image_url",
                "image_url": {"url": first_frame_uri},
                "role": "first_frame",
            })
        for data_uri in ref_image_uris:
            content.append({
                "type": "image_url",
                "image_url": {"url": data_uri},
                "role": "reference_image",
            })

        # 3. 处理参考视频
        ref_video_urls = list(inputs.get("reference_video_urls") or [])
        if len(ref_video_urls) > 3:
            raise ValueError(
                f"Seedance 2.0 最多接受 3 个参考视频，收到 {len(ref_video_urls)} 个"
            )
        for url in ref_video_urls:
            content.append({
                "type": "video_url",
                "video_url": {"url": url},
                "role": "reference_video",
            })

        # 4. 处理参考音频
        ref_audio_urls = list(inputs.get("reference_audio_urls") or [])
        if len(ref_audio_urls) > 3:
            raise ValueError(
                f"Seedance 2.0 最多接受 3 个参考音频，收到 {len(ref_audio_urls)} 个"
            )
        for url in ref_audio_urls:
            content.append({
                "type": "audio_url",
                "audio_url": {"url": url},
                "role": "reference_audio",
            })

        return content

    # ------------------------------------------------------------------ #
    #  核心执行
    # ------------------------------------------------------------------ #

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = self._get_api_key()
        if not api_key:
            return ToolResult(
                success=False,
                error="ARK_API_KEY 未设置。 " + self.install_instructions,
            )

        import requests

        start = time.time()
        endpoint_id = inputs.get("model") or self._get_endpoint_id()

        # 身份锁守卫：require_identity_lock=true 但无参考图时提示用户确认
        if inputs.get("require_identity_lock") and not inputs.get("_confirm_skip_identity_lock"):
            has_ref = bool(
                inputs.get("reference_image_urls")
                or inputs.get("reference_image_paths")
                or inputs.get("image_url")
                or inputs.get("image_path")
            )
            if not has_ref:
                return ToolResult(
                    success=False,
                    error=(
                        "require_identity_lock=true 但未提供角色参考图。\n"
                        "涉及角色的 Seedance 视频建议从 CharacterRegistry.build_reference_config()\n"
                        "获取四视图参考图，通过 reference_image_urls 或 reference_image_paths 传入。\n"
                        "\n"
                        "如用户确认无需角色身份锁、以纯 text_to_video 继续，请传入\n"
                        "_confirm_skip_identity_lock=true 后重试。"
                    ),
                )

        # 构建 content 数组
        try:
            content = self._build_content_array(inputs)
        except (FileNotFoundError, ValueError) as e:
            return ToolResult(success=False, error=str(e))

        # 构建请求 payload
        payload: dict[str, Any] = {
            "model": endpoint_id,
            "content": content,
            "ratio": inputs.get("ratio", "16:9"),
            "duration": inputs.get("duration", 5),
            "generate_audio": inputs.get("generate_audio", True),
            "watermark": inputs.get("watermark", False),
        }
        if inputs.get("resolution"):
            payload["resolution"] = inputs["resolution"]
        if inputs.get("seed") is not None:
            payload["seed"] = inputs["seed"]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        try:
            # 步骤 1：创建视频生成任务
            submit_resp = requests.post(
                f"{ARK_API_BASE}/contents/generations/tasks",
                headers=headers,
                json=payload,
                timeout=30,
            )
            submit_resp.raise_for_status()
            task_data = submit_resp.json()
            task_id = task_data.get("id")
            if not task_id:
                return ToolResult(
                    success=False,
                    error=f"创建任务失败，响应中缺少 id: {task_data}",
                )

            # 步骤 2：轮询任务状态
            status_url = f"{ARK_API_BASE}/contents/generations/tasks/{task_id}"
            poll_interval = 5
            while True:
                time.sleep(poll_interval)
                status_resp = requests.get(status_url, headers=headers, timeout=15)
                status_resp.raise_for_status()
                status_data = status_resp.json()
                status = status_data.get("status", "UNKNOWN")

                if status == "succeeded":
                    break
                if status in ("failed", "expired", "cancelled"):
                    error_msg = status_data.get("error", {}).get("message", status)
                    return ToolResult(
                        success=False,
                        error=f"Seedance 2.0 视频生成 {status}: {error_msg}",
                    )
                # 指数退避，最大 30 秒
                poll_interval = min(poll_interval * 1.5, 30)

            # 步骤 3：获取结果
            video_url = status_data.get("content", {}).get("video_url")
            if not video_url:
                return ToolResult(
                    success=False,
                    error="任务成功但响应中缺少 video_url",
                )

            # 步骤 4：下载视频
            video_response = requests.get(video_url, timeout=180)
            video_response.raise_for_status()

            output_path = Path(inputs.get("output_path", "seedance_output.mp4"))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(video_response.content)

        except requests.RequestException as e:
            return ToolResult(
                success=False,
                error=f"Seedance 2.0 via Ark API 请求失败: {e}",
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Seedance 2.0 via Ark API 处理失败: {e}",
            )

        from tools.video._shared import probe_output

        probed = probe_output(output_path)
        return ToolResult(
            success=True,
            data={
                "provider": "seedance",
                "gateway": "volcengine-ark",
                "model": endpoint_id,
                "endpoint_id": endpoint_id,
                "prompt": inputs.get("prompt", ""),
                "ratio": inputs.get("ratio", "16:9"),
                "resolution": inputs.get("resolution", "720p"),
                "generate_audio": inputs.get("generate_audio", True),
                "watermark": inputs.get("watermark", False),
                "seed": status_data.get("seed"),
                "duration": status_data.get("duration"),
                "task_id": task_id,
                "output": str(output_path),
                "output_path": str(output_path),
                "format": "mp4",
                **probed,
            },
            artifacts=[str(output_path)],
            cost_cny=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - start, 2),
            model=endpoint_id,
        )
