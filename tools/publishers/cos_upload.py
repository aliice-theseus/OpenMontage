"""Tencent COS (Cloud Object Storage) 上传工具。

将管道中生成的角色图、场景草图等资产上传到腾讯COS，
返回公开访问URL供下游使用（如Seedance reference_image_urls）。
配置从 .env 读取，不硬编码凭据。
"""

from __future__ import annotations

import mimetypes
import os
import time
from pathlib import Path
from typing import Any, Optional

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolTier,
)


class CosUpload(BaseTool):
    """将本地资产文件上传到腾讯云对象存储（COS）。

    支持角色图、场景草图、参考图、最终视频等资产的云端存储。
    COS 凭据从环境变量读取（TENCENT_COS_SECRET_ID / _SECRET_KEY / _BUCKET / _REGION / _DOMAIN）。

    典型用法：
        cos_upload.execute({
            "file_path": "/path/to/character-front.png",
            "cos_key": "projects/my-video/characters/hero-front.png",
        })
        # => {"url": "https://...", "cos_key": "projects/my-video/characters/hero-front.png"}

    或在管道中自动生成 COS key：
        cos_upload.execute({
            "file_path": "/path/to/scene-sketch-01.png",
            "project_id": "my-video",
            "asset_type": "scene-sketches",
        })
        # => 自动拼接为 "projects/my-video/scene-sketches/scene-sketch-01.png"
    """

    name = "cos_upload"
    version = "1.0.0"
    tier = ToolTier.PUBLISH
    capability = "cloud_storage"
    provider = "tencent_cos"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.DETERMINISTIC
    runtime = ToolRuntime.API

    capabilities = [
        "asset_upload",
        "image_upload",
        "video_upload",
        "reference_image_hosting",
    ]
    supports = {
        "max_file_size_mb": 500,
        "public_urls": True,
        "path_auto_generation": True,
    }
    best_for = [
        "上传角色四视图到COS供Seedance reference_image_urls引用",
        "上传场景草图到COS供用户预览和下游引用",
        "上传最终渲染视频到COS用于分发",
    ]
    not_good_for = [
        "超大型文件（>500MB，建议分片上传）",
        "需要实时低延迟的场景（COS是对象存储，非CDN）",
    ]
    install_instructions = (
        "在 .env 中设置 TENCENT_COS_SECRET_ID, TENCENT_COS_SECRET_KEY, "
        "TENCENT_COS_BUCKET, TENCENT_COS_REGION, TENCENT_COS_DOMAIN。"
    )

    dependencies = [
        "env:TENCENT_COS_SECRET_ID",
        "env:TENCENT_COS_SECRET_KEY",
        "env:TENCENT_COS_BUCKET",
        "env:TENCENT_COS_REGION",
    ]

    input_schema = {
        "type": "object",
        "required": ["file_path"],
        "properties": {
            "file_path": {
                "type": "string",
                "description": "要上传的本地文件绝对路径",
            },
            "cos_key": {
                "type": "string",
                "description": "COS上的对象键（路径）。不传则从 project_id + asset_type + 文件名自动生成",
            },
            "project_id": {
                "type": "string",
                "description": "项目标识符，用于自动生成 COS key（需要配合 asset_type）",
            },
            "asset_type": {
                "type": "string",
                "enum": ["characters", "scene-sketches", "renders", "references", "thumbnails", "other"],
                "description": "资产类型，用于自动生成 COS key 的子目录",
            },
            "overwrite": {
                "type": "boolean",
                "default": True,
                "description": "是否覆盖COS上已存在的同名文件",
            },
        },
    }
    output_schema = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "文件的公开访问URL"},
            "cos_key": {"type": "string", "description": "COS上的对象键"},
            "bucket": {"type": "string"},
            "region": {"type": "string"},
            "file_size_bytes": {"type": "integer"},
            "content_type": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=0,
        ram_mb=64,
        vram_mb=0,
        disk_mb=0,
        network_required=True,
    )
    user_visible_verification = [
        "确认返回的URL可以通过浏览器访问",
        "确认 COS key 与项目目录结构一致",
    ]

    # ------------------------------------------------------------------
    # COS 客户端（懒加载）
    # ------------------------------------------------------------------

    _client = None  # 模块级缓存，避免重复创建

    @staticmethod
    def _get_env(key: str) -> str:
        """获取环境变量，如果缺失则抛错。"""
        value = os.environ.get(key)
        if not value:
            raise EnvironmentError(
                f"缺少环境变量 {key}，请在 .env 中配置腾讯COS凭据"
            )
        return value.strip()

    def _get_client(self) -> Any:
        """懒加载 COS 客户端（qcloud_cos）。"""
        if self._client is not None:
            return self._client

        secret_id = self._get_env("TENCENT_COS_SECRET_ID")
        secret_key = self._get_env("TENCENT_COS_SECRET_KEY")
        region = self._get_env("TENCENT_COS_REGION")

        try:
            from qcloud_cos import CosConfig, CosS3Client
        except ImportError:
            raise ImportError(
                "缺少 cos-python-sdk-v5 依赖，请运行: pip install cos-python-sdk-v5"
            )

        config = CosConfig(
            Region=region,
            SecretId=secret_id,
            SecretKey=secret_key,
        )
        self.__class__._client = CosS3Client(config)
        return self._client

    # ------------------------------------------------------------------
    # COS key 生成
    # ------------------------------------------------------------------

    @staticmethod
    def _auto_cos_key(
        file_path: Path,
        project_id: Optional[str],
        asset_type: Optional[str],
    ) -> str:
        """自动生成 COS key。

        规则：
            projects/{project_id}/{asset_type}/{filename}
        如果 project_id 未提供，直接以 assets/{filename} 作为 key。
        """
        filename = file_path.name
        if project_id and asset_type:
            return f"projects/{project_id}/{asset_type}/{filename}"
        elif project_id:
            return f"projects/{project_id}/{filename}"
        else:
            return f"assets/{filename}"

    @staticmethod
    def _detect_content_type(file_path: Path) -> str:
        """根据文件扩展名检测 MIME 类型。"""
        mime, _ = mimetypes.guess_type(str(file_path))
        if mime:
            return mime
        # 兜底映射
        suffix_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
            ".mp4": "video/mp4",
            ".webm": "video/webm",
            ".mov": "video/quicktime",
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".json": "application/json",
            ".srt": "text/plain",
            ".vtt": "text/vtt",
        }
        return suffix_map.get(file_path.suffix.lower(), "application/octet-stream")

    # ------------------------------------------------------------------
    # 执行
    # ------------------------------------------------------------------

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()

        # --- 解析输入 ---
        file_path_str = inputs.get("file_path", "").strip()
        if not file_path_str:
            return ToolResult(
                success=False,
                error="缺少必填参数 file_path",
            )

        file_path = Path(file_path_str)
        if not file_path.is_file():
            return ToolResult(
                success=False,
                error=f"文件不存在: {file_path}",
            )

        cos_key = inputs.get("cos_key", "").strip()
        if not cos_key:
            cos_key = self._auto_cos_key(
                file_path,
                inputs.get("project_id"),
                inputs.get("asset_type"),
            )

        overwrite = inputs.get("overwrite", True)

        # --- 获取 COS 配置 ---
        try:
            bucket = self._get_env("TENCENT_COS_BUCKET")
            domain = os.environ.get("TENCENT_COS_DOMAIN", "").strip()
            client = self._get_client()
        except (EnvironmentError, ImportError) as e:
            return ToolResult(success=False, error=str(e))

        # --- 检查文件是否已存在（不覆盖模式） ---
        if not overwrite:
            try:
                resp = client.head_object(Bucket=bucket, Key=cos_key)
                if resp.get("ETag"):
                    # 文件已存在，直接返回已有URL
                    url = f"{domain.rstrip('/')}/{cos_key}" if domain else (
                        f"https://{bucket}.cos.{self._get_env('TENCENT_COS_REGION')}.myqcloud.com/{cos_key}"
                    )
                    file_size = file_path.stat().st_size
                    return ToolResult(
                        success=True,
                        data={
                            "url": url,
                            "cos_key": cos_key,
                            "bucket": bucket,
                            "region": self._get_env("TENCENT_COS_REGION"),
                            "file_size_bytes": file_size,
                            "content_type": self._detect_content_type(file_path),
                            "skipped": True,
                            "reason": "文件已存在，未覆盖",
                        },
                        duration_seconds=round(time.time() - start, 2),
                    )
            except Exception:
                pass  # 文件不存在，继续上传

        # --- 上传 ---
        try:
            content_type = self._detect_content_type(file_path)
            file_size = file_path.stat().st_size

            with open(file_path, "rb") as fp:
                resp = client.put_object(
                    Bucket=bucket,
                    Body=fp,
                    Key=cos_key,
                    ContentType=content_type,
                )

            if not resp.get("ETag"):
                return ToolResult(
                    success=False,
                    error=f"COS上传失败，响应: {resp}",
                    duration_seconds=round(time.time() - start, 2),
                )

            # 构造公开访问URL
            url = f"{domain.rstrip('/')}/{cos_key}" if domain else (
                f"https://{bucket}.cos.{self._get_env('TENCENT_COS_REGION')}.myqcloud.com/{cos_key}"
            )

            return ToolResult(
                success=True,
                data={
                    "url": url,
                    "cos_key": cos_key,
                    "bucket": bucket,
                    "region": self._get_env("TENCENT_COS_REGION"),
                    "file_size_bytes": file_size,
                    "content_type": content_type,
                    "etag": resp.get("ETag", "").strip('"'),
                },
                artifacts=[str(file_path)],
                duration_seconds=round(time.time() - start, 2),
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"COS上传异常: {e}",
                duration_seconds=round(time.time() - start, 2),
            )

    # ------------------------------------------------------------------
    # 快捷方法：上传角色图
    # ------------------------------------------------------------------

    @staticmethod
    def upload_character_image(
        file_path: str,
        project_id: str,
        character_id: str,
        view: str = "front",
    ) -> dict[str, Any]:
        """便捷方法：上传角色图并返回结果dict。

        参数:
            file_path: 本地文件路径
            project_id: 项目标识
            character_id: 角色ID
            view: 视图名称（front/side/back/closeup/sheet）

        返回:
            {"url": str, "cos_key": str}
        """
        tool = CosUpload()
        cos_key = f"projects/{project_id}/characters/{character_id}-{view}.png"
        result = tool.execute({
            "file_path": file_path,
            "cos_key": cos_key,
        })
        if result.success:
            return result.data
        raise RuntimeError(f"角色图上传失败: {result.error}")

    # ------------------------------------------------------------------
    # 快捷方法：上传场景草图
    # ------------------------------------------------------------------

    @staticmethod
    def upload_scene_sketch(
        file_path: str,
        project_id: str,
        scene_id: str,
    ) -> dict[str, Any]:
        """便捷方法：上传场景草图并返回结果dict。

        参数:
            file_path: 本地文件路径
            project_id: 项目标识
            scene_id: 场景ID

        返回:
            {"url": str, "cos_key": str}
        """
        tool = CosUpload()
        cos_key = f"projects/{project_id}/scene-sketches/{scene_id}.png"
        result = tool.execute({
            "file_path": file_path,
            "cos_key": cos_key,
        })
        if result.success:
            return result.data
        raise RuntimeError(f"场景草图上传失败: {result.error}")
