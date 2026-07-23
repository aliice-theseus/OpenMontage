"""Contracts for mandatory user confirmation before video generation."""

from pathlib import Path

import jsonschema
import pytest

from lib.pipeline_context import (
    PipelineContext,
    StageEntryApprovalRequiredError,
    check_stage_entry_approval,
)
from lib.pipeline_loader import (
    VIDEO_GENERATION_ENTRY_TOOLS,
    _validate_video_generation_entry_gates,
    list_pipelines,
    load_pipeline,
    stage_requires_entry_human_approval,
)


def _declared_stage_tools(stage: dict) -> set[str]:
    tools: set[str] = set()
    for field in (
        "tools_available",
        "required_tools",
        "optional_tools",
        "preferred_tools",
        "fallback_tools",
    ):
        tools.update(stage.get(field, []))
    return tools


def test_every_video_generation_stage_has_entry_confirmation_gate():
    for pipeline_name in list_pipelines():
        manifest = load_pipeline(pipeline_name)
        for stage in manifest["stages"]:
            stage_tools = _declared_stage_tools(stage)
            if stage["name"] == "compose" or stage_tools & VIDEO_GENERATION_ENTRY_TOOLS:
                assert stage.get("entry_human_approval_required") is True, (
                    f"{pipeline_name}.{stage['name']} can generate video without "
                    "an explicit entry confirmation"
                )
            for sub_stage in stage.get("sub_stages", []):
                sub_tools = set(sub_stage.get("tools_available", []))
                if sub_tools & VIDEO_GENERATION_ENTRY_TOOLS:
                    assert sub_stage.get("entry_human_approval_required") is True


def test_manifest_validation_rejects_ungated_video_generation_stage():
    manifest = {
        "name": "unsafe",
        "version": "1.0",
        "stages": [
            {
                "name": "assets",
                "tools_available": ["video_selector"],
            }
        ],
    }

    with pytest.raises(jsonschema.ValidationError, match="must set entry_human"):
        _validate_video_generation_entry_gates(manifest)


def test_runtime_blocks_video_stage_until_current_stage_is_confirmed():
    blocked = PipelineContext(
        pipeline_type="animated-explainer",
        current_stage="assets",
        project_id="confirmation-test",
        pipeline_dir=Path("pipelines"),
    )
    with pytest.raises(StageEntryApprovalRequiredError):
        check_stage_entry_approval(blocked)

    approved = PipelineContext(
        pipeline_type="animated-explainer",
        current_stage="assets",
        project_id="confirmation-test",
        pipeline_dir=Path("pipelines"),
        entry_human_approved=True,
    )
    check_stage_entry_approval(approved)


def test_sample_sub_stage_has_its_own_confirmation_gate():
    manifest = load_pipeline("animated-explainer")
    assert stage_requires_entry_human_approval(manifest, "proposal.sample") is True
