"""Pipeline execution context — 工具调用时的流水线门禁。

在流水线执行期间，EP（执行制片人）在每个阶段开始时设置当前上下文。
``BaseTool.execute()`` 会检查此上下文，确保工具只能在清单允许的阶段中被调用。

用法::

    from lib.pipeline_context import set_pipeline_context, clear_pipeline_context, PipelineContext

    ctx = PipelineContext(
        pipeline_type="cinematic",
        current_stage="assets",
        project_id="my-project",
        pipeline_dir=Path("projects"),
    )
    set_pipeline_context(ctx)
    try:
        # 此作用域内的所有 tool.execute() 都会触发门禁检查
        tool.execute(params)
    finally:
        clear_pipeline_context()
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# PipelineContext — 描述当前流水线的执行位置
# ---------------------------------------------------------------------------

@dataclass
class PipelineContext:
    """当前流水线的执行上下文。

    Attributes:
        pipeline_type: 管道类型名，对应 ``pipeline_defs/<name>.yaml``。
        current_stage: 当前阶段名，须与清单中的 ``stages[].name`` 匹配。
        project_id: 项目标识符，用于检查点路径解析。
        pipeline_dir: 流水线工作目录（含检查点子目录的根目录）。
    """
    pipeline_type: str
    current_stage: str
    project_id: str
    pipeline_dir: Path


# ---------------------------------------------------------------------------
# 全局上下文（单线程 EP 编排，因此全局变量够用）
# ---------------------------------------------------------------------------

_current_context: Optional[PipelineContext] = None


def set_pipeline_context(ctx: Optional[PipelineContext]) -> None:
    """设置当前流水线上下文。在阶段开始时调用。

    传入 ``None`` 可清除上下文（等价于调用 ``clear_pipeline_context()``）。
    """
    global _current_context
    _current_context = ctx


def get_pipeline_context() -> Optional[PipelineContext]:
    """获取当前流水线上下文，如果不在流水线执行中则返回 None。"""
    return _current_context


def clear_pipeline_context() -> None:
    """清除当前流水线上下文。在阶段结束时调用。"""
    global _current_context
    _current_context = None


# ---------------------------------------------------------------------------
# 门禁异常
# ---------------------------------------------------------------------------

class ToolNotPermittedError(PermissionError):
    """工具在当前流水线阶段中不被允许时抛出。"""

    def __init__(
        self,
        tool_name: str,
        pipeline_type: str,
        current_stage: str,
        allowed_tools: set[str],
    ) -> None:
        self.tool_name = tool_name
        self.pipeline_type = pipeline_type
        self.current_stage = current_stage
        self.allowed_tools = allowed_tools
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        return (
            f"[PIPELINE GATE] 工具 '{self.tool_name}' 在流水线 "
            f"'{self.pipeline_type}' 的阶段 '{self.current_stage}' 中不被允许。\n"
            f"允许的工具: {sorted(self.allowed_tools)}\n\n"
            f"解决办法: 使用选择器（如 video_selector）替代直接调用提供商工具，"
            f"或在正确的阶段（如 assets）调用。"
        )


class StagePrerequisiteError(PermissionError):
    """阶段的前置产物检查不通过时抛出。"""

    def __init__(
        self,
        current_stage: str,
        pipeline_type: str,
        missing_artifacts: list[tuple[str, str]],
    ) -> None:
        """
        Args:
            current_stage: 当前阶段名。
            pipeline_type: 管道类型。
            missing_artifacts: 缺失产物列表，每项为 (artifact_name, producing_stage)。
        """
        self.current_stage = current_stage
        self.pipeline_type = pipeline_type
        self.missing_artifacts = missing_artifacts
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        items = "\n".join(
            f"  - {artifact}（由 {stage} 阶段产出）"
            for artifact, stage in self.missing_artifacts
        )
        return (
            f"[PIPELINE GATE] 阶段 '{self.current_stage}' 的前置产物不满足 "
            f"（流水线 '{self.pipeline_type}'）。\n"
            f"缺失的产物:\n{items}\n\n"
            f"解决办法: 必须先完成上游阶段后再进入当前阶段。"
        )


# ---------------------------------------------------------------------------
# 门禁检查函数（由 BaseTool.execute() 调用）
# ---------------------------------------------------------------------------

def check_stage_prerequisites(ctx: PipelineContext) -> None:
    """检查当前阶段的所有前置产物是否已作为 completed checkpoint 存在。

    从管道清单中读取当前阶段的 ``required_artifacts_in``，
    找到每个产物对应的产出阶段，然后检查该阶段的 checkpoint 状态。

    Args:
        ctx: 当前流水线上下文。

    Raises:
        StagePrerequisiteError: 如果有前置产物缺失。
    """
    from lib.pipeline_loader import (
        load_pipeline,
        get_stage_required_artifacts,
        get_producing_stage,
    )
    from lib.checkpoint import read_checkpoint

    manifest = load_pipeline(ctx.pipeline_type)
    required = get_stage_required_artifacts(manifest, ctx.current_stage)

    missing: list[tuple[str, str]] = []
    for artifact_name in required:
        producing_stage = get_producing_stage(manifest, artifact_name)
        if producing_stage is None:
            # 找不到产出阶段，跳过检查（可能是外部产物）
            continue
        # 跳过自身（一个阶段不能依赖自己的产出）
        if producing_stage == ctx.current_stage:
            continue
        try:
            checkpoint = read_checkpoint(
                ctx.pipeline_dir, ctx.project_id, producing_stage,
            )
            cp_ok = checkpoint and checkpoint.get("status") == "completed"
        except Exception:
            # read_checkpoint 可能因 schema 验证失败而抛出异常，
            # 此时视为该阶段的 checkpoint 不存在或无效。
            cp_ok = False
        if not cp_ok:
            missing.append((artifact_name, producing_stage))

    if missing:
        raise StagePrerequisiteError(
            current_stage=ctx.current_stage,
            pipeline_type=ctx.pipeline_type,
            missing_artifacts=missing,
        )


def check_tool_permitted(tool_name: str, ctx: PipelineContext) -> None:
    """检查工具是否在当前流水线上下文中被允许。

    做两层检查:
      1. 工具是否在当前阶段的允许工具列表中。
         选择器（video_selector / image_selector / tts_selector）可绕过此项
         以便它们能路由到提供商工具。
      2. 当前阶段的前置产物是否齐全（completed checkpoint）。
         此项对所有工具均强制——选择器也不例外。

    Args:
        tool_name: 待检查的工具名。
        ctx: 当前流水线上下文。

    Raises:
        ToolNotPermittedError: 如果工具不在当前阶段的允许列表中（非选择器）。
        StagePrerequisiteError: 如果前置产物不满足。
    """
    from lib.pipeline_loader import load_pipeline, get_stage_allowed_tools

    manifest = load_pipeline(ctx.pipeline_type)
    allowed = get_stage_allowed_tools(manifest, ctx.current_stage)

    # 第 1 层：工具权限检查。
    # 选择器可在任何阶段调（它们负责路由到提供商工具），
    # 但提供商工具必须明确在阶段的允许列表中。
    _SELECTORS = frozenset({"video_selector", "image_selector", "tts_selector", "screen_capture_selector"})
    if tool_name not in _SELECTORS and tool_name not in allowed:
        raise ToolNotPermittedError(
            tool_name=tool_name,
            pipeline_type=ctx.pipeline_type,
            current_stage=ctx.current_stage,
            allowed_tools=allowed,
        )

    # 第 2 层：前置产物完整性（所有工具均强制执行）
    check_stage_prerequisites(ctx)
