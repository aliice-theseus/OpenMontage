"""Generate a consistent four-panel character reference sheet with local FLUX.2 Dev."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)
from tools.graphics.local_diffusion import _is_flux2_model, get_flux2_model_path


# 通过 get_flux2_model_path() 获取模型路径；可通过 FLUX2_MODEL_PATH 环境变量配置
DEFAULT_CHARACTER_MODEL = get_flux2_model_path()
_VIEW_SPECS = {
    "front": {
        "width": 1024,
        "height": 1536,
        "instruction": (
            "Create a full-body front view of this exact person, standing upright and facing "
            "the camera, with a neutral balanced stance, arms relaxed, and the complete head, "
            "hands, legs, and feet visible."
        ),
    },
    "side": {
        "width": 832,
        "height": 1248,
        "instruction": (
            "Using the reference image as the identity and wardrobe anchor, create the exact same "
            "person in a strict 90-degree left-facing full-body side profile, with a neutral "
            "balanced stance and the complete head, hands, legs, and feet visible."
        ),
    },
    "back": {
        "width": 832,
        "height": 1248,
        "instruction": (
            "Using the reference image as the identity and wardrobe anchor, create the exact same "
            "person in a strict full-body back view, facing directly away from the camera, clearly "
            "showing the rear hairstyle, garment construction, and footwear."
        ),
    },
    "closeup": {
        "width": 832,
        "height": 1248,
        "instruction": (
            "Using the reference image as the identity and wardrobe anchor, create a chest-up front "
            "portrait of the exact same person, facing the camera, with the complete head and both "
            "shoulders visible and clear facial, hair, collar, fabric, and accessory details."
        ),
    },
}


def _compose_prompt(view: str, character_core: str) -> str:
    shared = (
        "A professional photorealistic character modeling reference on a pure white seamless studio "
        "background, evenly lit by soft diffused studio light. Preserve one exact identity, facial "
        "structure, hairstyle, clothing layers, materials, colors, accessories, body build, and "
        "natural human proportions. The frame contains one unobstructed person with realistic skin "
        "texture and crisp garment construction."
    )
    return f"{_VIEW_SPECS[view]['instruction']} {character_core.strip()} {shared}"


def _fit_panel(image: Any, target_width: int, target_height: int) -> Any:
    """Scale to panel height and crop centrally, matching the documented stitch contract."""
    from PIL import Image

    ratio = target_height / image.height
    resized_width = max(target_width, round(image.width * ratio))
    resized = image.resize((resized_width, target_height), Image.Resampling.LANCZOS)
    left = max(0, (resized_width - target_width) // 2)
    return resized.crop((left, 0, left + target_width, target_height))


class CharacterRefSheet(BaseTool):
    """Create front/side/back/close-up views, then stitch a deterministic 16:9 sheet."""

    name = "character_ref_sheet"
    version = "1.0.0"
    tier = ToolTier.GENERATE
    capability = "character_reference"
    provider = "local_diffusion"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.SEEDED
    runtime = ToolRuntime.LOCAL_GPU
    agent_skills = ["flux-best-practices", "flux-character-turnaround"]

    capabilities = ["character_turnaround", "character_reference_sheet", "identity_reference"]
    supports = {
        "front_t2i": True,
        "reference_conditioned_views": True,
        "seamless_stitch": True,
        "default_model": DEFAULT_CHARACTER_MODEL,
    }
    best_for = [
        "consistent character front/side/back reference views",
        "identity-lock source sheets for downstream video generation",
        "local privacy-sensitive character development",
    ]
    not_good_for = ["CPU-only machines", "commercial use without checking the model license"]
    install_instructions = (
        "Install the FLUX.2 local stack with requirements-gpu.txt and cache "
        f"{DEFAULT_CHARACTER_MODEL}; model downloads require explicit approval."
    )

    input_schema = {
        "type": "object",
        "required": ["character_id", "character_core", "output_dir"],
        "properties": {
            "character_id": {"type": "string"},
            "character_core": {
                "type": "string",
                "description": "Shared identity, face, hair, body, clothing, material, and accessory description.",
            },
            "output_dir": {"type": "string"},
            "model": {"type": "string", "default": DEFAULT_CHARACTER_MODEL},
            "seed": {"type": "integer", "default": 42},
            "num_inference_steps": {"type": "integer", "default": 20},
            "guidance_scale": {"type": "number", "default": 3.5},
            "num_gpus": {"type": "integer", "default": 6, "description": "Multi-GPU dispatch. 默认6卡."},
            "allow_model_download": {"type": "boolean", "default": False},
            "operation": {
                "type": "string",
                "enum": ["full", "front_only", "complete_from_front"],
                "default": "full",
                "description": (
                    "Use front_only for the approval gate, then complete_from_front with the "
                    "approved front_image_path. full is available for explicitly approved batch runs."
                ),
            },
            "front_image_path": {
                "type": "string",
                "description": "Approved front image required by complete_from_front.",
            },
            "_force_full_approval": {
                "type": "boolean",
                "default": False,
                "description": "内部标记。仅当用户明确批准跳过 front_only 审批时才设为 true，配合 operation='full' 使用。",
            },
        },
    }
    output_schema = {
        "type": "object",
        "properties": {
            "sheet_path": {"type": "string"},
            "view_paths": {"type": "object"},
            "model": {"type": "string"},
            "seed": {"type": "integer"},
        },
    }
    resource_profile = ResourceProfile(
        cpu_cores=8, ram_mb=64000, vram_mb=24000, disk_mb=60000, network_required=False
    )
    idempotency_key_fields = ["character_id", "character_core", "model", "seed"]
    side_effects = ["writes four source images and one stitched reference sheet"]
    user_visible_verification = ["Inspect identity, wardrobe, view angles, anatomy, and crop completeness"]

    def get_status(self) -> ToolStatus:
        try:
            from diffusers import Flux2Pipeline  # noqa: F401
            from PIL import Image  # noqa: F401
            return ToolStatus.AVAILABLE
        except (ImportError, RuntimeError):
            return ToolStatus.UNAVAILABLE

    @staticmethod
    def _selector() -> Any:
        from tools.graphics.image_selector import ImageSelector

        return ImageSelector()

    @staticmethod
    def _release_local_pipeline() -> None:
        try:
            from tools.tool_registry import registry

            registry.ensure_discovered()
            local_tool = registry.get("local_diffusion")
            if local_tool is not None and hasattr(local_tool, "release_cached_models"):
                local_tool.release_cached_models()
        except Exception:
            # Cleanup is best effort and must not hide the generation result.
            pass

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        from PIL import Image

        start = time.time()
        character_id = inputs["character_id"].strip()
        if not character_id:
            return ToolResult(success=False, error="character_id must not be empty")
        character_core = inputs["character_core"].strip()
        if not character_core:
            return ToolResult(success=False, error="character_core must not be empty")

        output_dir = Path(inputs["output_dir"])
        output_dir.mkdir(parents=True, exist_ok=True)
        model = inputs.get("model", DEFAULT_CHARACTER_MODEL)
        if not _is_flux2_model(model):
            return ToolResult(success=False, error="character_ref_sheet requires a FLUX.2 model")

        seed = inputs.get("seed", 42)
        operation = inputs.get("operation", "full")
        force_full = inputs.get("_force_full_approval", False)
        # 流程守卫：禁止绕过 front_only 审批直接全量生成
        if operation == "full" and not force_full:
            return ToolResult(
                success=False,
                error=(
                    "四视图生成必须经过 front_only 审批 → complete_from_front 分步流程。\n"
                    "如已获得用户明确批准可跳过审批，请传入 _force_full_approval=true。"
                ),
            )
        prompts = {view: _compose_prompt(view, character_core) for view in _VIEW_SPECS}
        paths = {
            view: output_dir / f"{character_id}-{view}.png"
            for view in _VIEW_SPECS
        }
        if operation == "complete_from_front":
            approved_front = inputs.get("front_image_path")
            if not approved_front:
                return ToolResult(
                    success=False,
                    error="complete_from_front requires front_image_path",
                )
            paths["front"] = Path(approved_front)
            if not paths["front"].is_file():
                return ToolResult(
                    success=False,
                    error=f"Approved front image does not exist: {paths['front']}",
                )
        generated: list[str] = []
        selector = self._selector()

        try:
            views_to_generate = (
                ["front"]
                if operation == "front_only"
                else ["side", "back", "closeup"]
                if operation == "complete_from_front"
                else list(_VIEW_SPECS)
            )
            for view in views_to_generate:
                spec = _VIEW_SPECS[view]
                request = {
                    "prompt": prompts[view],
                    "preferred_provider": "local_diffusion",
                    "model": model,
                    "pipeline_type": "flux",
                    "width": spec["width"],
                    "height": spec["height"],
                    "seed": seed,
                    "num_inference_steps": inputs.get("num_inference_steps", 20),
                    "guidance_scale": inputs.get("guidance_scale", 3.5),
                    "num_gpus": inputs.get("num_gpus", 6),
                    "offload_mode": "sequential",
                    "reuse_pipeline": True,
                    "allow_model_download": inputs.get("allow_model_download", False),
                    "output_path": str(paths[view]),
                }
                if view != "front":
                    request.update(
                        {
                            "generation_mode": "edit",
                            "image_path": str(paths["front"]),
                        }
                    )
                result = selector.execute(request)
                if not result.success:
                    return ToolResult(
                        success=False,
                        error=f"Character reference {view} generation failed: {result.error}",
                        artifacts=generated,
                        duration_seconds=round(time.time() - start, 2),
                        seed=seed,
                        model=model,
                    )
                generated.append(str(paths[view]))

            if operation == "front_only":
                return ToolResult(
                    success=True,
                    data={
                        "provider": "local_diffusion",
                        "selected_tool": self.name,
                        "model": model,
                        "seed": seed,
                        "front_path": str(paths["front"]),
                        "view_paths": {"front": str(paths["front"])},
                        "prompts": {"front": prompts["front"]},
                        "workflow_status": "awaiting_front_approval",
                        "next_operation": "complete_from_front",
                    },
                    artifacts=generated,
                    cost_cny=0.0,
                    duration_seconds=round(time.time() - start, 2),
                    seed=seed,
                    model=model,
                )

            with Image.open(paths["front"]) as source:
                front = source.convert("RGB").copy()
            with Image.open(paths["side"]) as source:
                side = source.convert("RGB").copy()
            with Image.open(paths["back"]) as source:
                back = source.convert("RGB").copy()
            with Image.open(paths["closeup"]) as source:
                closeup = source.convert("RGB").copy()

            closeup = closeup.crop((0, 0, closeup.width, round(closeup.height * 0.8)))
            canvas_width, canvas_height = 1280, 720
            body_width = int(canvas_width * 0.22)
            closeup_width = canvas_width - (body_width * 3)
            panels = [
                _fit_panel(front, body_width, canvas_height),
                _fit_panel(side, body_width, canvas_height),
                _fit_panel(back, body_width, canvas_height),
                _fit_panel(closeup, closeup_width, canvas_height),
            ]
            sheet = Image.new("RGB", (canvas_width, canvas_height), "#FFFFFF")
            x = 0
            for panel in panels:
                sheet.paste(panel, (x, 0))
                x += panel.width
            sheet_path = output_dir / f"{character_id}-reference-sheet.png"
            sheet.save(sheet_path)
            generated.append(str(sheet_path))
        except Exception as exc:
            return ToolResult(
                success=False,
                error=f"Character reference sheet processing failed: {exc}",
                artifacts=generated,
                duration_seconds=round(time.time() - start, 2),
                seed=seed,
                model=model,
            )
        finally:
            self._release_local_pipeline()

        return ToolResult(
            success=True,
            data={
                "provider": "local_diffusion",
                "selected_tool": self.name,
                "model": model,
                "seed": seed,
                "sheet_path": str(sheet_path),
                "view_paths": {view: str(path) for view, path in paths.items()},
                "prompts": prompts,
                "layout": {"canvas": [1280, 720], "columns": [body_width] * 3 + [closeup_width]},
                "generation_strategy": "front_t2i_then_flux2_reference_conditioning",
                "operation": operation,
            },
            artifacts=generated,
            cost_cny=0.0,
            duration_seconds=round(time.time() - start, 2),
            seed=seed,
            model=model,
        )
