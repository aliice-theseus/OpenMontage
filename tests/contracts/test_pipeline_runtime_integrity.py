"""Regression coverage for pipeline loading, stage order, and checkpoints."""

from pathlib import Path

import pytest

import lib.checkpoint as checkpoint_module
import lib.pipeline_loader as pipeline_loader
from lib.checkpoint import get_pipeline_stages, validate_checkpoint
from lib.pipeline_context import (
    PipelineContext,
    StagePrerequisiteError,
    check_stage_prerequisites,
)


def test_every_manifest_loads_as_utf8_and_validates():
    """All shipped manifests must load through the real runtime loader."""
    names = sorted(pipeline_loader.list_pipelines())
    assert names

    loaded = {name: pipeline_loader.load_pipeline(name) for name in names}

    assert set(loaded) == set(names)
    assert loaded["documentary-montage"]["category"] == "documentary"
    assert {mode["name"] for mode in loaded["screen-demo"]["production_modes"]} == {
        "real_capture",
        "synthetic_terminal",
    }


def test_explicit_pipeline_load_errors_are_not_silently_replaced(monkeypatch):
    def fail_load(_name):
        raise RuntimeError("manifest validation failed")

    monkeypatch.setattr(pipeline_loader, "load_pipeline", fail_load)

    with pytest.raises(RuntimeError, match="manifest validation failed"):
        get_pipeline_stages("screen-demo")


def test_all_declared_stages_are_resumable_with_checkpoints():
    """The checkpoint-driven state machine needs a durable completion marker."""
    for name in pipeline_loader.list_pipelines():
        manifest = pipeline_loader.load_pipeline(name)
        disabled = [
            stage["name"]
            for stage in manifest["stages"]
            if stage.get("checkpoint_required", True) is False
        ]
        assert disabled == [], f"{name} has non-resumable stages: {disabled}"


def test_rig_plan_checkpoint_validates():
    rig_plan = {
        "version": "1.0",
        "characters": [
            {
                "character_id": "lead",
                "parts": [],
                "joints": {},
                "layers": [],
                "required_poses": [],
            }
        ],
    }
    pose_library = {
        "version": "1.0",
        "characters": [{"character_id": "lead", "poses": {}}],
    }

    checkpoint = {
        "version": "1.0",
        "project_id": "character-project",
        "pipeline_type": "character-animation",
        "stage": "rig_plan",
        "status": "completed",
        "timestamp": "2026-07-20T00:00:00+00:00",
        "checkpoint_policy": "guided",
        "human_approval_required": False,
        "human_approved": False,
        "artifacts": {"rig_plan": rig_plan, "pose_library": pose_library},
    }

    validate_checkpoint(checkpoint)
    assert checkpoint["artifacts"]["rig_plan"] == rig_plan
    assert checkpoint["artifacts"]["pose_library"] == pose_library


def test_completed_checkpoint_must_contain_the_required_artifact(
    monkeypatch,
):
    manifest = {
        "name": "test-pipeline",
        "stages": [
            {"name": "producer", "produces": ["expected_artifact"]},
            {
                "name": "consumer",
                "required_artifacts_in": ["expected_artifact"],
            },
        ],
    }

    monkeypatch.setattr(pipeline_loader, "load_pipeline", lambda _name: manifest)
    monkeypatch.setattr(
        checkpoint_module,
        "read_checkpoint",
        lambda *_args, **_kwargs: {"status": "completed", "artifacts": {}},
    )
    context = PipelineContext(
        pipeline_type="test-pipeline",
        current_stage="consumer",
        project_id="project",
        pipeline_dir=Path("."),
    )

    with pytest.raises(StagePrerequisiteError) as exc_info:
        check_stage_prerequisites(context)

    assert exc_info.value.missing_artifacts == [
        ("expected_artifact", "producer")
    ]


def test_documentary_compose_declares_final_review():
    manifest = pipeline_loader.load_pipeline("documentary-montage")
    compose = next(stage for stage in manifest["stages"] if stage["name"] == "compose")

    assert "render_report" in compose["produces"]
    assert "final_review" in compose["produces"]
