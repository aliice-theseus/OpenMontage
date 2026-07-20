"""Pipeline manifest loader.

Loads and validates pipeline YAML manifests from pipeline_defs/.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

import yaml
import jsonschema

PIPELINE_DEFS_DIR = Path(__file__).resolve().parent.parent / "pipeline_defs"
SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent
    / "schemas"
    / "pipelines"
    / "pipeline_manifest.schema.json"
)


# Stages using these tools create new moving-image output.  They must declare
# an explicit entry approval gate so generation cannot begin merely because an
# earlier creative checkpoint was approved.
VIDEO_GENERATION_ENTRY_TOOLS = frozenset({
    "video_selector",
    "talking_head",
    "lip_sync",
    "character_rig_renderer",
    "video_compose",
    "hyperframes_compose",
})


def _load_manifest_schema() -> dict:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_pipeline(name: str, defs_dir: Optional[Path] = None) -> dict[str, Any]:
    """Load and validate a pipeline manifest by name.

    Args:
        name: Pipeline name (without .yaml extension).
        defs_dir: Override directory for pipeline definitions.

    Returns:
        Validated pipeline manifest dict.
    """
    defs_dir = defs_dir or PIPELINE_DEFS_DIR
    path = defs_dir / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Pipeline manifest not found: {path}")

    # Pipeline manifests contain typographic punctuation and multilingual
    # guidance.  Relying on the platform default encoding makes valid UTF-8
    # manifests fail on Windows systems configured for GBK/CP936.
    with open(path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    schema = _load_manifest_schema()
    jsonschema.validate(instance=manifest, schema=schema)
    _validate_video_generation_entry_gates(manifest)

    return manifest


def _stage_declared_tools(stage: dict[str, Any]) -> set[str]:
    """Collect every tool explicitly declared on a stage."""
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


def _validate_video_generation_entry_gates(manifest: dict[str, Any]) -> None:
    """Reject manifests that can generate video without an entry approval.

    ``human_approval_default`` is an exit checkpoint and therefore cannot
    protect the first generation call in a stage.  Every compose stage and
    every stage exposing a moving-image generation tool must opt into the
    dedicated entry gate.
    """
    for stage in manifest.get("stages", []):
        declared_tools = _stage_declared_tools(stage)
        creates_video = (
            stage.get("name") == "compose"
            or bool(declared_tools & VIDEO_GENERATION_ENTRY_TOOLS)
        )
        if creates_video and not stage.get("entry_human_approval_required", False):
            raise jsonschema.ValidationError(
                "Pipeline stage "
                f"{manifest.get('name', '<unknown>')}.{stage.get('name', '<unknown>')} "
                "can generate video and must set entry_human_approval_required: true"
            )
        for sub_stage in stage.get("sub_stages", []):
            sub_tools = set(sub_stage.get("tools_available", []))
            if (
                sub_tools & VIDEO_GENERATION_ENTRY_TOOLS
                and not sub_stage.get("entry_human_approval_required", False)
            ):
                raise jsonschema.ValidationError(
                    "Pipeline sub-stage "
                    f"{manifest.get('name', '<unknown>')}.{stage.get('name')}."
                    f"{sub_stage.get('name', '<unknown>')} can generate video and must "
                    "set entry_human_approval_required: true"
                )


def list_pipelines(defs_dir: Optional[Path] = None) -> list[str]:
    """List all available pipeline manifest names."""
    defs_dir = defs_dir or PIPELINE_DEFS_DIR
    return [p.stem for p in defs_dir.glob("*.yaml")]


def _condition_is_active(condition: Optional[str], context: Optional[dict[str, Any]]) -> bool:
    """Evaluate a simple manifest condition against runtime context."""
    if not condition:
        return True
    if not context:
        return False
    return bool(context.get(condition))


def get_reference_input_config(manifest: dict) -> dict[str, Any]:
    """Return reference-input configuration, defaulting to disabled."""
    return manifest.get("reference_input", {}) or {}


def pipeline_supports_reference_input(manifest: dict) -> bool:
    """Whether the manifest declares support for reference-video input."""
    return bool(get_reference_input_config(manifest).get("supported", False))


def get_stage_sub_stages(
    manifest: dict,
    stage_name: str,
    *,
    context: Optional[dict[str, Any]] = None,
    include_inactive: bool = True,
) -> list[dict[str, Any]]:
    """Return sub-stage definitions for a stage.

    By default this returns all declared sub-stages so agents can inspect the
    full workflow shape. Pass ``include_inactive=False`` with context to filter
    to active sub-stages only.
    """
    for stage in manifest["stages"]:
        if stage["name"] != stage_name:
            continue
        sub_stages = list(stage.get("sub_stages", []))
        if include_inactive:
            return sub_stages
        return [
            sub_stage
            for sub_stage in sub_stages
            if _condition_is_active(sub_stage.get("condition"), context)
        ]
    return []


def get_stage_order(
    manifest: dict,
    *,
    include_sub_stages: bool = False,
    context: Optional[dict[str, Any]] = None,
) -> list[str]:
    """Extract the ordered list of stage names from a manifest.

    ``include_sub_stages=True`` exposes declarative sample/preview units to the
    agent without turning them into mandatory checkpoint stages. Sub-stages are
    emitted as ``<stage>.<sub_stage>``.
    """
    order: list[str] = []
    for stage in manifest["stages"]:
        order.append(stage["name"])
        if not include_sub_stages:
            continue
        for sub_stage in get_stage_sub_stages(
            manifest,
            stage["name"],
            context=context,
            include_inactive=context is None,
        ):
            order.append(f"{stage['name']}.{sub_stage['name']}")
    return order


def get_required_tools(manifest: dict) -> set[str]:
    """Collect tools across stages, sub-stages, and reference-input analysis."""
    tools: set[str] = set()
    for stage in manifest["stages"]:
        tools.update(stage.get("preferred_tools", []))
        tools.update(stage.get("fallback_tools", []))
        tools.update(stage.get("tools_available", []))
        for sub_stage in stage.get("sub_stages", []):
            tools.update(sub_stage.get("tools_available", []))
    tools.update(get_reference_input_config(manifest).get("analysis_tools", []))
    return tools


def get_stage_skill(manifest: dict, stage_name: str) -> Optional[str]:
    """Get the skill path for an instruction-driven stage."""
    for stage in manifest["stages"]:
        if stage["name"] == stage_name:
            return stage.get("skill")
    return None


def get_stage_review_focus(manifest: dict, stage_name: str) -> list[str]:
    """Get the review focus items for a stage."""
    for stage in manifest["stages"]:
        if stage["name"] == stage_name:
            return stage.get("review_focus", [])
    return []


def get_stage_required_artifacts(manifest: dict, stage_name: str) -> list[str]:
    """Get the list of artifact names required as input for a stage.

    Reads the ``required_artifacts_in`` field of the stage definition.
    These are the artifacts that must exist (as completed checkpoints from
    their producing stages) before the stage can begin.
    """
    for stage in manifest["stages"]:
        if stage["name"] == stage_name:
            return stage.get("required_artifacts_in", [])
    return []


def get_producing_stage(manifest: dict, artifact_name: str) -> Optional[str]:
    """Find the stage that produces a given artifact.

    Scans each stage's ``produces`` list for the artifact name.
    Returns the first matching stage name, or ``None`` if not found.
    """
    for stage in manifest["stages"]:
        produces = [a.strip() for a in stage.get("produces", [])]
        if artifact_name in produces:
            return stage["name"]
    # Fallback: check CANONICAL_STAGE_ARTIFACTS reverse mapping
    from lib.checkpoint import CANONICAL_STAGE_ARTIFACTS
    for stage_name, produced_artifact in CANONICAL_STAGE_ARTIFACTS.items():
        if produced_artifact == artifact_name:
            return stage_name
    return None


def get_stage_allowed_tools(manifest: dict, stage_name: str) -> set[str]:
    """Get the set of tool names permitted in a given stage.

    Collects from ALL tool-related fields on the stage and its sub-stages,
    so the pipeline gate in ``BaseTool`` can authorise or deny a call.

    Fields scanned on the stage itself:
      ``tools_available``, ``required_tools``, ``optional_tools``,
      ``preferred_tools``, ``fallback_tools``

    Sub-stage tool lists are also included because a stage's sub-stages
    share the same parent stage context.
    """
    tools: set[str] = set()
    parent_name, separator, sub_stage_name = stage_name.partition(".")
    for stage in manifest["stages"]:
        if stage["name"] != parent_name:
            continue
        if separator:
            for sub in stage.get("sub_stages", []):
                if sub.get("name") == sub_stage_name:
                    return set(sub.get("tools_available", []))
            return tools
        # 主阶段的所有工具字段
        for field in ("tools_available", "required_tools", "optional_tools",
                      "preferred_tools", "fallback_tools"):
            tools.update(stage.get(field, []))
        # 子阶段的 tools_available
        for sub in stage.get("sub_stages", []):
            tools.update(sub.get("tools_available", []))
        return tools  # 找到对应阶段后立即返回
    return tools  # 没找到则返回空集


def stage_requires_entry_human_approval(
    manifest: dict[str, Any], stage_name: str,
) -> bool:
    """Return whether a stage is blocked until the user explicitly confirms."""
    parent_name, separator, sub_stage_name = stage_name.partition(".")
    for stage in manifest["stages"]:
        if stage["name"] != parent_name:
            continue
        if separator:
            for sub_stage in stage.get("sub_stages", []):
                if sub_stage.get("name") == sub_stage_name:
                    return bool(sub_stage.get("entry_human_approval_required", False))
            return False
        return bool(stage.get("entry_human_approval_required", False))
    return False


# ---------------------------------------------------------------------------
# Capability-Extension Enforcement
# ---------------------------------------------------------------------------

class ExtensionNotPermitted(PermissionError):
    """Raised when a capability extension is used but not permitted by the pipeline."""


def check_extension_permitted(
    manifest: dict,
    extension_type: str,
) -> None:
    """Enforce that a capability extension is permitted by the pipeline manifest.

    Args:
        manifest: Loaded pipeline manifest dict.
        extension_type: One of 'custom_scripts', 'custom_playbooks',
                        'custom_skills', 'custom_tools'.

    Raises:
        ExtensionNotPermitted: If the extension is not allowed.
    """
    valid_extensions = {"custom_scripts", "custom_playbooks", "custom_skills", "custom_tools"}
    if extension_type not in valid_extensions:
        raise ValueError(
            f"Unknown extension type {extension_type!r}. "
            f"Valid types: {sorted(valid_extensions)}"
        )

    extensions = manifest.get("extensions", {})
    if not extensions.get(extension_type, False):
        raise ExtensionNotPermitted(
            f"Pipeline {manifest.get('name', 'unknown')!r} does not permit "
            f"{extension_type}. Set extensions.{extension_type}: true in the "
            f"pipeline manifest to allow this."
        )


def get_permitted_extensions(manifest: dict) -> dict[str, bool]:
    """Return the extension permission flags for a pipeline."""
    defaults = {
        "custom_scripts": False,
        "custom_playbooks": False,
        "custom_skills": False,
        "custom_tools": False,
    }
    extensions = manifest.get("extensions", {})
    return {k: extensions.get(k, v) for k, v in defaults.items()}
