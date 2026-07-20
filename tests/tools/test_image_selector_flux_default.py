"""Regression tests for the video pipeline's default FLUX image routing."""

from __future__ import annotations

from types import SimpleNamespace

from tools.base_tool import ToolStatus
from tools.graphics.image_selector import (
    ImageSelector,
    _DEFAULT_TEXT_TO_IMAGE_PROVIDER,
)


def test_schema_defaults_text_to_image_to_local_flux():
    selector = ImageSelector()
    assert _DEFAULT_TEXT_TO_IMAGE_PROVIDER == "local_diffusion"
    assert (
        selector.input_schema["properties"]["preferred_provider"]["default"]
        == "local_diffusion"
    )
    assert selector.supports["default_text_to_image_model_family"] == "FLUX"


def test_plain_text_to_image_defaults_to_local_flux():
    selector = ImageSelector()
    assert selector._resolve_preferred_provider({"prompt": "cinematic landscape"}) == "local_diffusion"


def test_explicit_provider_overrides_flux_default():
    selector = ImageSelector()
    assert (
        selector._resolve_preferred_provider(
            {"prompt": "brand poster", "preferred_provider": "recraft"}
        )
        == "recraft"
    )


def test_explicit_auto_overrides_flux_default():
    selector = ImageSelector()
    assert selector._resolve_preferred_provider(
        {"prompt": "choose for me", "preferred_provider": "auto"}
    ) == "auto"


def test_allowed_provider_policy_overrides_flux_default():
    selector = ImageSelector()
    assert selector._resolve_preferred_provider(
        {"prompt": "stock image", "allowed_providers": ["pexels", "pixabay"]}
    ) == "auto"


def test_image_edit_uses_capability_routing():
    selector = ImageSelector()
    assert selector._resolve_preferred_provider(
        {"prompt": "repaint", "generation_mode": "edit", "image_path": "source.png"}
    ) == "auto"


def test_custom_comfyui_workflow_uses_capability_routing():
    selector = ImageSelector()
    assert selector._resolve_preferred_provider(
        {"prompt": "render", "workflow_path": "workflow.json", "output_node": "9"}
    ) == "auto"


def test_unavailable_default_flux_does_not_silently_fall_back(monkeypatch):
    selector = ImageSelector()
    unavailable_flux = SimpleNamespace(
        provider="local_diffusion",
        name="local_diffusion",
        get_status=lambda: ToolStatus.UNAVAILABLE,
    )
    available_api = SimpleNamespace(
        provider="openai",
        name="openai_image",
        get_status=lambda: ToolStatus.AVAILABLE,
    )
    rankings = [
        SimpleNamespace(provider="openai"),
        SimpleNamespace(provider="local_diffusion"),
    ]
    monkeypatch.setattr("lib.scoring.rank_providers", lambda candidates, context: rankings)

    tool, score = selector._select_best_tool(
        {"prompt": "portrait"},
        [unavailable_flux, available_api],
        {},
    )

    assert tool is None
    assert score is None
