"""Tests for the deterministic FLUX.2 character reference workflow."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from tools.base_tool import ToolResult
from tools.graphics.character_ref_sheet import CharacterRefSheet, DEFAULT_CHARACTER_MODEL


class _FakeSelector:
    def __init__(self):
        self.calls = []

    def execute(self, inputs):
        self.calls.append(dict(inputs))
        colors = {
            "front": "#DDEEFF",
            "side": "#EEDDEE",
            "back": "#EEFFDD",
            "closeup": "#FFEEDD",
        }
        view = next(key for key in colors if inputs["output_path"].endswith(f"-{key}.png"))
        Image.new("RGB", (inputs["width"], inputs["height"]), colors[view]).save(
            inputs["output_path"]
        )
        return ToolResult(success=True, data={"output": inputs["output_path"]})


def test_character_sheet_uses_front_as_flux2_reference_and_stitches(monkeypatch):
    selector = _FakeSelector()
    monkeypatch.setattr(CharacterRefSheet, "_selector", staticmethod(lambda: selector))
    monkeypatch.setattr(CharacterRefSheet, "_release_local_pipeline", staticmethod(lambda: None))

    character_id = "test-flux2-hero"
    try:
        result = CharacterRefSheet().execute(
            {
                "character_id": character_id,
                "character_core": "A 28-year-old woman with a high ponytail and layered white robes.",
                "output_dir": "tests",
                "seed": 77,
                "_force_full_approval": True,  # 单元测试直接测试全量生成功能
            }
        )

        assert result.success is True
        assert result.model == DEFAULT_CHARACTER_MODEL
        assert len(selector.calls) == 4
        assert "image_path" not in selector.calls[0]
        assert [call["generation_mode"] for call in selector.calls[1:]] == ["edit"] * 3
        assert all(call["image_path"].endswith(f"{character_id}-front.png") for call in selector.calls[1:])
        assert all(call["preferred_provider"] == "local_diffusion" for call in selector.calls)
        assert all(call["offload_mode"] == "sequential" for call in selector.calls)
        assert all(call["reuse_pipeline"] is True for call in selector.calls)
        assert [(call["width"], call["height"]) for call in selector.calls] == [
            (1024, 1536),
            (832, 1248),
            (832, 1248),
            (832, 1248),
        ]

        with Image.open(result.data["sheet_path"]) as sheet:
            assert sheet.size == (1280, 720)
        assert result.data["layout"]["columns"] == [281, 281, 281, 437]
        assert len(result.artifacts) == 5
    finally:
        for suffix in ("front", "side", "back", "closeup", "reference-sheet"):
            Path(f"tests/{character_id}-{suffix}.png").unlink(missing_ok=True)


def test_character_sheet_rejects_non_flux2_model(monkeypatch):
    monkeypatch.setattr(CharacterRefSheet, "_release_local_pipeline", staticmethod(lambda: None))
    result = CharacterRefSheet().execute(
        {
            "character_id": "hero",
            "character_core": "A consistent adult character.",
            "output_dir": "tests",
            "model": "black-forest-labs/FLUX.1-dev",
        }
    )

    assert result.success is False
    assert "requires a FLUX.2 model" in result.error


def test_front_only_stops_at_approval_gate(monkeypatch):
    selector = _FakeSelector()
    monkeypatch.setattr(CharacterRefSheet, "_selector", staticmethod(lambda: selector))
    monkeypatch.setattr(CharacterRefSheet, "_release_local_pipeline", staticmethod(lambda: None))
    character_id = "test-front-gate"
    try:
        result = CharacterRefSheet().execute(
            {
                "character_id": character_id,
                "character_core": "A consistent adult character in a tailored grey uniform.",
                "output_dir": "tests",
                "operation": "front_only",
            }
        )

        assert result.success is True
        assert len(selector.calls) == 1
        assert result.data["workflow_status"] == "awaiting_front_approval"
        assert result.data["next_operation"] == "complete_from_front"
        assert len(result.artifacts) == 1
        assert Path(result.artifacts[0]).name == f"{character_id}-front.png"
    finally:
        Path(f"tests/{character_id}-front.png").unlink(missing_ok=True)


def test_complete_from_approved_front_skips_front_regeneration(monkeypatch):
    selector = _FakeSelector()
    monkeypatch.setattr(CharacterRefSheet, "_selector", staticmethod(lambda: selector))
    monkeypatch.setattr(CharacterRefSheet, "_release_local_pipeline", staticmethod(lambda: None))
    character_id = "test-approved-front"
    approved_front = Path(f"tests/{character_id}-approved.png")
    Image.new("RGB", (1024, 1536), "#DDEEFF").save(approved_front)
    try:
        result = CharacterRefSheet().execute(
            {
                "character_id": character_id,
                "character_core": "A consistent adult character in a tailored grey uniform.",
                "output_dir": "tests",
                "operation": "complete_from_front",
                "front_image_path": str(approved_front),
            }
        )

        assert result.success is True
        assert len(selector.calls) == 3
        assert all(call["generation_mode"] == "edit" for call in selector.calls)
        assert all(call["image_path"] == str(approved_front) for call in selector.calls)
        assert result.data["view_paths"]["front"] == str(approved_front)
        assert result.data["operation"] == "complete_from_front"
    finally:
        approved_front.unlink(missing_ok=True)
        for suffix in ("side", "back", "closeup", "reference-sheet"):
            Path(f"tests/{character_id}-{suffix}.png").unlink(missing_ok=True)
