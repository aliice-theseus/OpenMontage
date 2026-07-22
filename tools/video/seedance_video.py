"""Seedance 2.0 (ByteDance) video generation via 火山引擎 Ark API.

直接调用火山引擎 Ark 上的 Seedance 2.0 模型。
适用于中国大陆网络环境。

配置方式：
  1. 设置环境变量 ARK_API_KEY（火山引擎 Ark API Key）
  2. 可选设置环境变量 SEEDANCE_ENDPOINT_ID（推理接入点 ID，有默认值）
  3. 或在调用时通过 model 参数指定 Endpoint ID

调用示例（curl）：
  curl -X POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks \\
    -H "Content-Type: application/json" \\
    -H "Authorization: Bearer $ARK_API_KEY" \\
    -d '{
      "model": "ep-20260707160429-ghxd2",
      "content": [
        {"type": "text", "text": "a cat playing piano"},
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
import os
import time
from pathlib import Path
from typing import Any

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
DEFAULT_ENDPOINT_ID = "ep-20260707160429-ghxd2"


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
        "reference-conditioned generation (up to 9 images + 3 video clips + 3 audio clips)",
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
            "prompt": {"type": "string", "description": "视频内容描述/提示词"},
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
            # ----- 首帧/单张图片输入（兼容 video_selector 路由） -----
            "image_url": {
                "type": "string",
                "description": "首帧参考图片 URL（用于 i2v，将被加入 content 数组）",
            },
            "image_path": {
                "type": "string",
                "description": "本地首帧参考图片路径，将转为 data URI 发送",
            },
            # ----- 多参考素材输入（用于 reference_to_video） -----
            "reference_image_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "参考图片 URL 列表，最多 9 张",
            },
            "reference_image_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "本地参考图片路径列表，将转为 data URI 发送，最多 9 张",
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
        """火山引擎 Ark Seedance 2.0 按 token 计费，此处保持同等量级估算。"""
        duration = inputs.get("duration", 5)
        resolution = inputs.get("resolution", "720p")
        # 粗略估算：时长 x 分辨率系数
        res_factor = 1.5 if resolution == "1080p" else 1.0 if resolution == "720p" else 0.7
        return round(0.06 * duration * res_factor, 2)

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        """通常 5 秒视频约 60-120 秒，10 秒视频约 120-180 秒。"""
        duration = inputs.get("duration", 5)
        return 60.0 + float(duration) * 8.0

    # ------------------------------------------------------------------ #
    #  辅助方法
    # ------------------------------------------------------------------ #

    @staticmethod
    def _file_to_data_uri(path: str) -> str:
        """将本地文件转为 data URI。"""
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

        Ark API 的 content 数组结构：
        [
          {"type": "text", "text": "提示词"},
          {"type": "image_url", "image_url": {"url": "..."}, "role": "reference_image"},
          {"type": "video_url", "video_url": {"url": "..."}, "role": "reference_video"},
          {"type": "audio_url", "audio_url": {"url": "..."}, "role": "reference_audio"},
        ]
        """
        content: list[dict] = [
            {"type": "text", "text": inputs.get("prompt", "")}
        ]

        # 1. 处理单张首帧图片（来自 image_url / image_path / 或 selector 传递的 image_url）
        image_url = inputs.get("image_url")
        if not image_url and inputs.get("image_path"):
            image_url = self._file_to_data_uri(inputs["image_path"])
        if image_url:
            content.append({
                "type": "image_url",
                "image_url": {"url": image_url},
                "role": "reference_image",
            })

        # 2. 处理多参考图片
        ref_image_urls = list(inputs.get("reference_image_urls") or [])
        for local_path in inputs.get("reference_image_paths") or []:
            ref_image_urls.append(self._file_to_data_uri(local_path))
        if len(ref_image_urls) > 9:
            raise ValueError(
                f"Seedance 2.0 最多接受 9 张参考图片，收到 {len(ref_image_urls)} 张"
            )
        for url in ref_image_urls:
            content.append({
                "type": "image_url",
                "image_url": {"url": url},
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
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - start, 2),
            model=endpoint_id,
        )
