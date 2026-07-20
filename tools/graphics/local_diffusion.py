"""Local FLUX.1/FLUX.2 and Stable Diffusion generation via diffusers."""

from __future__ import annotations

import gc
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


_DEFAULT_MODEL = "black-forest-labs/FLUX.1-schnell"
_DEFAULT_FLUX2_MODEL = "black-forest-labs/FLUX.2-dev"


def _is_flux_model(model_id: str, pipeline_type: str = "auto") -> bool:
    """Resolve the pipeline family, allowing local paths to be overridden."""
    if pipeline_type != "auto":
        return pipeline_type == "flux"
    return "flux" in model_id.lower()


def _is_flux2_model(model_id: str) -> bool:
    """Return whether a model ID/path names the second-generation FLUX family."""
    normalized = model_id.lower().replace("_", "").replace("-", "")
    return "flux.2" in model_id.lower() or "flux2" in normalized


def _default_generation_parameters(model_id: str, is_flux: bool) -> tuple[int, float]:
    """Return sensible defaults when callers omit steps and guidance."""
    if not is_flux:
        return 30, 7.5
    if "schnell" in model_id.lower():
        return 4, 0.0
    return 28, 3.5


def _normalise_loras(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    """Accept a simple LoRA string or a list of strings/config objects."""
    raw_loras = inputs.get("lora_models")
    if raw_loras is None and inputs.get("lora_model"):
        raw_loras = [
            {
                "model": inputs["lora_model"],
                "weight_name": inputs.get("lora_weight_name"),
                "scale": inputs.get("lora_scale", 1.0),
            }
        ]
    if raw_loras is None:
        return []
    if isinstance(raw_loras, (str, dict)):
        raw_loras = [raw_loras]
    if not isinstance(raw_loras, list):
        raise ValueError("lora_models must be a string, object, or list")

    loras: list[dict[str, Any]] = []
    for index, item in enumerate(raw_loras):
        item = {"model": item} if isinstance(item, str) else item
        if not isinstance(item, dict) or not item.get("model"):
            raise ValueError(f"LoRA entry {index} must contain a non-empty 'model'")
        try:
            scale = float(item.get("scale", 1.0))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"LoRA entry {index} has an invalid scale") from exc
        loras.append(
            {
                "model": str(item["model"]),
                "weight_name": item.get("weight_name"),
                "adapter_name": str(item.get("adapter_name") or f"lora_{index}"),
                "scale": scale,
            }
        )
    return loras


def _load_loras(
    pipe: Any,
    loras: list[dict[str, Any]],
    *,
    local_files_only: bool,
) -> None:
    """Load LoRA adapters and activate their requested weights."""
    for lora in loras:
        kwargs = {
            "adapter_name": lora["adapter_name"],
            "local_files_only": local_files_only,
        }
        if lora["weight_name"]:
            kwargs["weight_name"] = lora["weight_name"]
        pipe.load_lora_weights(lora["model"], **kwargs)

    if not loras:
        return
    if hasattr(pipe, "set_adapters"):
        pipe.set_adapters(
            [lora["adapter_name"] for lora in loras],
            adapter_weights=[lora["scale"] for lora in loras],
        )
    elif len(loras) > 1 or loras[0]["scale"] != 1.0:
        raise RuntimeError(
            "Installed diffusers version cannot apply multiple/scaled LoRA adapters; "
            "upgrade diffusers or use one LoRA with scale=1.0"
        )


class LocalDiffusion(BaseTool):
    name = "local_diffusion"
    version = "0.3.0"
    tier = ToolTier.GENERATE
    capability = "image_generation"
    provider = "local_diffusion"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.SEEDED
    runtime = ToolRuntime.LOCAL_GPU

    dependencies = []  # checked dynamically
    install_instructions = (
        "Install diffusers for local FLUX/Stable Diffusion:\n"
        "  pip install 'diffusers>=0.36.0' transformers accelerate torch "
        "sentencepiece protobuf safetensors"
    )
    agent_skills = ["flux-best-practices"]

    capabilities = ["generate_image", "generate_illustration", "text_to_image"]
    supports = {
        "negative_prompt": True,
        "seed": True,
        "offline": True,
        "custom_size": True,
        "lora": True,
        "multiple_loras": True,
        "image_edit": True,
        "image_edit_models": ["FLUX.2"],
        "reference_images": True,
        "negative_prompt_for_flux": False,
        "explicit_download_approval": True,
    }
    best_for = [
        "offline/air-gapped generation",
        "free image generation (no API cost)",
        "privacy-sensitive workflows",
    ]
    not_good_for = [
        "CPU-only machines (very slow)",
        "highest quality output (API models are better)",
    ]

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "negative_prompt": {"type": "string", "default": ""},
            "width": {"type": "integer", "default": 1024},
            "height": {"type": "integer", "default": 1024},
            "model": {
                "type": "string",
                "default": _DEFAULT_MODEL,
            },
            "pipeline_type": {
                "type": "string",
                "enum": ["auto", "flux", "stable_diffusion"],
                "default": "auto",
                "description": "Override auto-detection, especially for local model paths.",
            },
            "generation_mode": {
                "type": "string",
                "enum": ["generate", "edit"],
                "default": "generate",
            },
            "image_path": {
                "type": "string",
                "description": "Local reference image for FLUX.2 image-conditioned generation.",
            },
            "image_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Local reference images for FLUX.2 multi-reference generation.",
            },
            "seed": {"type": "integer"},
            "num_inference_steps": {
                "type": "integer",
                "default": 4,
                "description": "Defaults to 4 for FLUX.1-schnell, 28 for other FLUX, 30 for SD.",
            },
            "guidance_scale": {
                "type": "number",
                "default": 0.0,
                "description": "Defaults to 0 for schnell, 3.5 for other FLUX, 7.5 for SD.",
            },
            "enable_model_cpu_offload": {
                "type": "boolean",
                "default": True,
                "description": "Reduce CUDA VRAM use by offloading model components to CPU.",
            },
            "offload_mode": {
                "type": "string",
                "enum": ["sequential", "model", "none"],
                "description": (
                    "CUDA memory strategy. Character reference generation uses sequential; "
                    "when omitted, enable_model_cpu_offload preserves the legacy model/none behavior."
                ),
            },
            "reuse_pipeline": {
                "type": "boolean",
                "default": False,
                "description": "Reuse the loaded pipeline for a same-process multi-view batch.",
            },
            "release_pipeline_after": {
                "type": "boolean",
                "default": False,
                "description": "Release any cached pipeline after this generation finishes.",
            },
            "allow_model_download": {
                "type": "boolean",
                "default": False,
                "description": (
                    "Allow downloading missing base-model or LoRA files. "
                    "Defaults to false so production must explicitly approve large downloads."
                ),
            },
            "lora_model": {
                "type": "string",
                "description": "LoRA local path or Hugging Face repository (simple single-LoRA form).",
            },
            "lora_weight_name": {"type": "string"},
            "lora_scale": {"type": "number", "default": 1.0},
            "lora_models": {
                "type": "array",
                "description": "One or more LoRA paths/repositories with optional adapter settings.",
                "items": {
                    "oneOf": [
                        {"type": "string"},
                        {
                            "type": "object",
                            "required": ["model"],
                            "properties": {
                                "model": {"type": "string"},
                                "weight_name": {"type": "string"},
                                "adapter_name": {"type": "string"},
                                "scale": {"type": "number", "default": 1.0},
                            },
                        },
                    ]
                },
            },
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=4, ram_mb=24000, vram_mb=12000, disk_mb=30000, network_required=False
    )
    retry_policy = RetryPolicy(max_retries=1)
    idempotency_key_fields = ["prompt", "width", "height", "seed", "model", "image_path"]
    side_effects = [
        "writes image file to output_path",
        "downloads model/LoRA weights only when allow_model_download=true",
    ]
    user_visible_verification = ["Inspect generated image for relevance and quality"]

    def get_status(self) -> ToolStatus:
        try:
            import torch  # noqa: F401
            from diffusers import FluxPipeline  # noqa: F401
            return ToolStatus.AVAILABLE
        except (ImportError, RuntimeError):
            return ToolStatus.UNAVAILABLE

    def release_cached_models(self) -> None:
        """Release pipelines retained for an explicit multi-image batch."""
        cache = getattr(self, "_pipeline_cache", None)
        if cache is not None:
            cache.clear()
        gc.collect()
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except (ImportError, RuntimeError):
            pass

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        return 0.0

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        return 45.0  # varies substantially with model, GPU, and CPU offload

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        if self.get_status() != ToolStatus.AVAILABLE:
            return ToolResult(
                success=False,
                error="diffusers not installed. " + self.install_instructions,
            )

        import torch
        import diffusers
        from PIL import Image

        start = time.time()
        prompt = inputs["prompt"]
        negative = inputs.get("negative_prompt", "")
        width = inputs.get("width", 1024)
        height = inputs.get("height", 1024)
        seed = inputs.get("seed")
        model_id = inputs.get("model", _DEFAULT_MODEL)
        pipeline_type = inputs.get("pipeline_type", "auto")
        is_flux = _is_flux_model(model_id, pipeline_type)
        is_flux2 = is_flux and _is_flux2_model(model_id)
        default_steps, default_guidance = _default_generation_parameters(model_id, is_flux)
        steps = inputs.get("num_inference_steps", default_steps)
        guidance = inputs.get("guidance_scale", default_guidance)
        allow_model_download = inputs.get("allow_model_download", False)
        local_files_only = not allow_model_download
        reference_paths = inputs.get("image_paths") or []
        if inputs.get("image_path"):
            reference_paths = [inputs["image_path"]]
        if reference_paths and not is_flux2:
            return ToolResult(
                success=False,
                error="Local reference-image conditioning is supported only by FLUX.2 models.",
            )

        try:
            if torch.cuda.is_available():
                device = "cuda"
            else:
                mps = getattr(getattr(torch, "backends", None), "mps", None)
                device = "mps" if mps and mps.is_available() else "cpu"
            if device == "cuda" and torch.cuda.is_bf16_supported():
                dtype = torch.bfloat16
            elif device in {"cuda", "mps"}:
                dtype = torch.float16
            else:
                dtype = torch.float32

            loras = _normalise_loras(inputs)
            if is_flux2:
                pipeline_class = getattr(diffusers, "Flux2Pipeline", None)
                if pipeline_class is None:
                    return ToolResult(
                        success=False,
                        error=(
                            "Installed diffusers does not provide Flux2Pipeline. "
                            "Upgrade to diffusers>=0.36.0."
                        ),
                    )
            elif is_flux:
                pipeline_class = diffusers.FluxPipeline
            else:
                pipeline_class = diffusers.StableDiffusionPipeline

            lora_key = tuple(
                (item["model"], item["weight_name"], item["adapter_name"], item["scale"])
                for item in loras
            )
            cache_key = (model_id, str(dtype), local_files_only, lora_key)
            cache = getattr(self, "_pipeline_cache", None)
            if cache is None:
                cache = self._pipeline_cache = {}
            pipe = cache.get(cache_key) if inputs.get("reuse_pipeline", False) else None
            if pipe is None:
                try:
                    pipe = pipeline_class.from_pretrained(
                        model_id,
                        torch_dtype=dtype,
                        local_files_only=local_files_only,
                    )
                except Exception as exc:
                    if local_files_only:
                        return ToolResult(
                            success=False,
                            error=(
                                f"Model '{model_id}' is not available or complete in the local cache. "
                                "Downloading is disabled by default. Confirm the download, then retry "
                                "with allow_model_download=true. "
                                f"Original error: {exc}"
                            ),
                        )
                    raise

                try:
                    _load_loras(pipe, loras, local_files_only=local_files_only)
                except Exception as exc:
                    if local_files_only:
                        lora_names = ", ".join(lora["model"] for lora in loras)
                        return ToolResult(
                            success=False,
                            error=(
                                f"LoRA model(s) '{lora_names}' are not available or complete in the "
                                "local cache. Downloading is disabled by default. Confirm the download, "
                                "then retry with allow_model_download=true. "
                                f"Original error: {exc}"
                            ),
                        )
                    raise

                offload_mode = inputs.get("offload_mode")
                if offload_mode is None:
                    offload_mode = (
                        "model" if inputs.get("enable_model_cpu_offload", True) else "none"
                    )
                if device == "cuda" and offload_mode == "sequential":
                    pipe.enable_sequential_cpu_offload()
                elif device == "cuda" and offload_mode == "model":
                    pipe.enable_model_cpu_offload()
                else:
                    pipe = pipe.to(device)
                if inputs.get("reuse_pipeline", False):
                    cache[cache_key] = pipe

            generator = None
            if seed is not None:
                generator = torch.Generator(device=device).manual_seed(seed)

            generation_args: dict[str, Any] = {
                "prompt": prompt,
                "width": width,
                "height": height,
                "num_inference_steps": steps,
                "guidance_scale": guidance,
                "generator": generator,
            }
            if not is_flux and negative:
                generation_args["negative_prompt"] = negative
            if reference_paths:
                references = []
                for reference_path in reference_paths:
                    with Image.open(reference_path) as source:
                        references.append(source.convert("RGB").resize((width, height), Image.LANCZOS))
                generation_args["image"] = references[0] if len(references) == 1 else references
            image = pipe(**generation_args).images[0]

            output_path = Path(inputs.get("output_path", "generated_image.png"))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(str(output_path))

            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        except Exception as e:
            return ToolResult(success=False, error=f"Local diffusion generation failed: {e}")
        finally:
            if inputs.get("release_pipeline_after", False):
                self.release_cached_models()

        return ToolResult(
            success=True,
            data={
                "provider": "local_diffusion",
                "model": model_id,
                "prompt": prompt,
                "output": str(output_path),
                "pipeline_type": "flux" if is_flux else "stable_diffusion",
                "pipeline_class": (
                    "Flux2Pipeline" if is_flux2 else "FluxPipeline" if is_flux else "StableDiffusionPipeline"
                ),
                "reference_images": [str(path) for path in reference_paths],
                "loras": loras,
            },
            artifacts=[str(output_path)],
            cost_usd=0.0,
            duration_seconds=round(time.time() - start, 2),
            seed=seed,
            model=model_id,
        )
