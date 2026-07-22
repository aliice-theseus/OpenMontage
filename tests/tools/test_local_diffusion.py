"""Unit tests for local FLUX/Stable Diffusion routing and LoRA loading."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from tools.base_tool import ToolStatus
from tools.graphics.local_diffusion import LocalDiffusion, _DEFAULT_MODEL


def _mock_runtime(monkeypatch, *, cuda: bool = True):
    fake_torch = MagicMock()
    fake_torch.cuda.is_available.return_value = cuda
    fake_torch.cuda.is_bf16_supported.return_value = True
    fake_torch.bfloat16 = "bfloat16"
    fake_torch.float16 = "float16"
    fake_torch.float32 = "float32"
    fake_torch.Generator.return_value.manual_seed.return_value = "generator"
    fake_torch.backends.mps.is_available.return_value = False

    image = MagicMock()
    pipe = MagicMock()
    pipe.to.return_value = pipe
    pipe.return_value = SimpleNamespace(images=[image])
    flux_class = MagicMock()
    flux_class.from_pretrained.return_value = pipe
    flux2_class = MagicMock()
    flux2_class.from_pretrained.return_value = pipe
    sd_class = MagicMock()
    sd_class.from_pretrained.return_value = pipe
    fake_diffusers = SimpleNamespace(
        FluxPipeline=flux_class,
        Flux2Pipeline=flux2_class,
        StableDiffusionPipeline=sd_class,
    )

    monkeypatch.setitem(sys.modules, "torch", fake_torch)
    monkeypatch.setitem(sys.modules, "diffusers", fake_diffusers)
    monkeypatch.setattr(LocalDiffusion, "get_status", lambda self: ToolStatus.AVAILABLE)
    return fake_torch, flux_class, sd_class, pipe, image


def test_default_model_is_flux():
    tool = LocalDiffusion()
    assert tool.input_schema["properties"]["model"]["default"] == _DEFAULT_MODEL
    assert "FLUX" in _DEFAULT_MODEL


def test_default_flux_loads_lora_and_omits_negative_prompt(monkeypatch):
    _, flux_class, sd_class, pipe, image = _mock_runtime(monkeypatch)
    output = "tests/flux-test-output.png"

    result = LocalDiffusion().execute(
        {
            "prompt": "portrait",
            "negative_prompt": "must not be forwarded to FLUX",
            "lora_model": "org/portrait-lora",
            "lora_weight_name": "portrait.safetensors",
            "lora_scale": 0.7,
            "seed": 42,
            "output_path": output,
        }
    )

    assert result.success is True
    flux_class.from_pretrained.assert_called_once_with(
        _DEFAULT_MODEL, torch_dtype="bfloat16", local_files_only=True
    )
    sd_class.from_pretrained.assert_not_called()
    pipe.load_lora_weights.assert_called_once_with(
        "org/portrait-lora",
        adapter_name="lora_0",
        local_files_only=True,
        weight_name="portrait.safetensors",
    )
    pipe.set_adapters.assert_called_once_with(["lora_0"], adapter_weights=[0.7])
    pipe.enable_model_cpu_offload.assert_called_once_with()
    call_args = pipe.call_args.kwargs
    assert call_args["num_inference_steps"] == 4
    assert call_args["guidance_scale"] == 0.0
    assert "negative_prompt" not in call_args
    image.save.assert_called_once_with(str(Path(output)))
    assert result.data["pipeline_type"] == "flux"
    assert result.data["loras"][0]["model"] == "org/portrait-lora"


def test_multiple_loras_are_loaded_with_adapter_weights(monkeypatch):
    _, _, _, pipe, _ = _mock_runtime(monkeypatch)

    result = LocalDiffusion().execute(
        {
            "prompt": "illustration",
            "lora_models": [
                "org/style-lora",
                {"model": "C:/models/detail.safetensors", "scale": 0.4},
            ],
            "output_path": "tests/multi-lora-test-output.png",
        }
    )

    assert result.success is True
    assert pipe.load_lora_weights.call_count == 2
    pipe.set_adapters.assert_called_once_with(
        ["lora_0", "lora_1"], adapter_weights=[1.0, 0.4]
    )


def test_stable_diffusion_compatibility_keeps_negative_prompt(monkeypatch):
    _, flux_class, sd_class, pipe, _ = _mock_runtime(monkeypatch, cuda=False)

    result = LocalDiffusion().execute(
        {
            "prompt": "landscape",
            "negative_prompt": "blurry",
            "model": "stabilityai/stable-diffusion-2-1-base",
            "output_path": "tests/sd-test-output.png",
        }
    )

    assert result.success is True
    flux_class.from_pretrained.assert_not_called()
    sd_class.from_pretrained.assert_called_once_with(
        "stabilityai/stable-diffusion-2-1-base",
        torch_dtype="float32",
        local_files_only=True,
    )
    assert pipe.call_args.kwargs["negative_prompt"] == "blurry"
    assert pipe.call_args.kwargs["num_inference_steps"] == 30
    assert pipe.call_args.kwargs["guidance_scale"] == 7.5
    assert result.data["pipeline_type"] == "stable_diffusion"


@pytest.mark.parametrize("pipeline_type, expected", [("flux", True), ("stable_diffusion", False)])
def test_pipeline_type_overrides_local_path_auto_detection(pipeline_type, expected):
    from tools.graphics.local_diffusion import _is_flux_model

    assert _is_flux_model("C:/models/custom-model", pipeline_type) is expected


@pytest.mark.parametrize(
    "model_id",
    [
        "black-forest-labs/FLUX.2-dev",
        "/home/roy/.cache/modelscope/Black-Forest-Labs/FLUX___2-dev",
        "C:/models/flux2-dev",
    ],
)
def test_flux2_model_detection_accepts_hub_and_local_paths(model_id):
    from tools.graphics.local_diffusion import _is_flux2_model

    assert _is_flux2_model(model_id) is True


def test_missing_cached_model_prompts_for_explicit_download(monkeypatch):
    _, flux_class, _, _, _ = _mock_runtime(monkeypatch)
    flux_class.from_pretrained.side_effect = OSError("model not found in cache")

    result = LocalDiffusion().execute({"prompt": "portrait"})

    assert result.success is False
    assert "is not available or complete in the local cache" in result.error
    assert "allow_model_download=true" in result.error
    assert "HF cache path" in result.error


def test_explicit_download_approval_disables_local_only_mode(monkeypatch):
    _, flux_class, _, _, _ = _mock_runtime(monkeypatch)

    result = LocalDiffusion().execute(
        {
            "prompt": "portrait",
            "allow_model_download": True,
            "output_path": "tests/download-approved-test-output.png",
        }
    )

    assert result.success is True
    flux_class.from_pretrained.assert_called_once_with(
        _DEFAULT_MODEL, torch_dtype="bfloat16", local_files_only=False
    )


def test_flux2_reference_image_uses_flux2_pipeline_and_sequential_offload(monkeypatch):
    fake_torch, flux_class, sd_class, pipe, _ = _mock_runtime(monkeypatch)
    from PIL import Image

    reference = Path("tests/flux2-reference-input.png")
    try:
        Image.new("RGB", (64, 96), "white").save(reference)
        result = LocalDiffusion().execute(
            {
                "prompt": "the exact same character in side profile",
                "model": "black-forest-labs/FLUX.2-dev",
                "pipeline_type": "flux",
                "generation_mode": "edit",
                "image_path": str(reference),
                "width": 832,
                "height": 1248,
                "num_inference_steps": 20,
                "guidance_scale": 3.5,
                "offload_mode": "sequential",
                "output_path": "tests/flux2-reference-output.png",
            }
        )

        assert result.success is True
        flux_class.from_pretrained.assert_not_called()
        sd_class.from_pretrained.assert_not_called()
        flux2_class = sys.modules["diffusers"].Flux2Pipeline
        flux2_class.from_pretrained.assert_called_once_with(
            "black-forest-labs/FLUX.2-dev",
            torch_dtype="bfloat16",
            local_files_only=True,
        )
        pipe.enable_sequential_cpu_offload.assert_called_once_with()
        assert pipe.call_args.kwargs["image"].size == (832, 1248)
        assert pipe.call_args.kwargs["num_inference_steps"] == 20
        assert result.data["reference_images"] == [str(reference)]
        fake_torch.cuda.empty_cache.assert_called()
    finally:
        reference.unlink(missing_ok=True)
