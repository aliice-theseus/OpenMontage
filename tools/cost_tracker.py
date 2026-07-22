"""成本追踪核心：估算、预留、对账，持久化到 cost_log.json。

实现预算治理规则：
- 每个付费操作产生执行前估算（人民币 CNY）
- 编排器在执行前预留预算
- 超预算时暂停（warn/cap 模式）
- 工具执行完成后对账实际花费
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from lib.config_model import BudgetMode


class EntryStatus(str, Enum):
    ESTIMATED = "estimated"
    RESERVED = "reserved"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class BudgetExceededError(Exception):
    """Raised when an operation would exceed the budget in cap mode."""
    pass


class ApprovalRequiredError(Exception):
    """Raised when an operation needs user approval before proceeding."""
    pass


class CostTracker:
    """追踪管道项目的估算、预留和实际成本（人民币 CNY）。"""

    def __init__(
        self,
        budget_total_cny: float = 70.0,
        reserve_pct: float = 0.10,
        single_action_approval_cny: float = 3.50,
        require_approval_for_new_paid_tool: bool = True,
        mode: BudgetMode = BudgetMode.WARN,
        cost_log_path: Optional[Path] = None,
    ) -> None:
        self.budget_total_cny = budget_total_cny
        self.reserve_pct = reserve_pct
        self.single_action_approval_cny = single_action_approval_cny
        self.require_approval_for_new_paid_tool = require_approval_for_new_paid_tool
        self.mode = mode
        self.cost_log_path = cost_log_path
        self.entries: list[dict[str, Any]] = []
        self._approved_tools: set[str] = set()

        if cost_log_path and cost_log_path.exists():
            self._load()

    # ---- 预算计算 ----

    @property
    def budget_reserved_cny(self) -> float:
        return sum(
            e.get("reserved_cny", 0.0)
            for e in self.entries
            if e["status"] == EntryStatus.RESERVED.value
        )

    @property
    def budget_spent_cny(self) -> float:
        return sum(
            e.get("actual_cny", 0.0)
            for e in self.entries
            if e["status"] in (EntryStatus.COMPLETED.value, EntryStatus.FAILED.value)
        )

    @property
    def budget_remaining_cny(self) -> float:
        return self.budget_total_cny - self.budget_spent_cny - self.budget_reserved_cny

    @property
    def usable_budget_cny(self) -> float:
        """预算减去预留储备。"""
        holdback = self.budget_total_cny * self.reserve_pct
        return max(0.0, self.budget_remaining_cny - holdback)

    def cost_snapshot(self) -> dict[str, float]:
        return {
            "total_spent_cny": round(self.budget_spent_cny, 4),
            "total_reserved_cny": round(self.budget_reserved_cny, 4),
            "budget_remaining_cny": round(self.budget_remaining_cny, 4),
        }

    # ---- 核心操作 ----

    def estimate(self, tool: str, operation: str, estimated_cny: float) -> str:
        """记录估算。返回条目 ID。"""
        entry_id = self._new_id()
        self.entries.append({
            "id": entry_id,
            "tool": tool,
            "operation": operation,
            "status": EntryStatus.ESTIMATED.value,
            "estimated_cny": round(estimated_cny, 4),
            "reserved_cny": 0.0,
            "actual_cny": 0.0,
            "timestamp": self._now(),
        })
        self._save()
        return entry_id

    def reserve(self, entry_id: str) -> None:
        """为已估算条目预留预算。

        在 cap 模式下抛出 BudgetExceededError，
        当操作超过单次审批阈值时抛出 ApprovalRequiredError。
        """
        entry = self._find(entry_id)
        estimated = entry["estimated_cny"]

        # 检查单次操作审批阈值
        if estimated > self.single_action_approval_cny:
            if self.mode != BudgetMode.OBSERVE:
                raise ApprovalRequiredError(
                    f"操作花费 ¥{estimated:.2f}，超过 "
                    f"单次操作审批阈值 ¥{self.single_action_approval_cny:.2f}"
                )

        # 检查新付费工具审批
        if self.require_approval_for_new_paid_tool and estimated > 0:
            if entry["tool"] not in self._approved_tools:
                if self.mode != BudgetMode.OBSERVE:
                    raise ApprovalRequiredError(
                        f"首次付费使用工具 {entry['tool']!r} 需要审批"
                    )

        # 检查预算
        if estimated > self.usable_budget_cny:
            if self.mode == BudgetMode.CAP:
                raise BudgetExceededError(
                    f"预留 ¥{estimated:.2f} 超过可用预算 "
                    f"¥{self.usable_budget_cny:.2f}"
                )

        entry["status"] = EntryStatus.RESERVED.value
        entry["reserved_cny"] = estimated
        entry["timestamp"] = self._now()
        self._save()

    def approve_tool(self, tool: str) -> None:
        """标记工具为已批准付费操作。"""
        self._approved_tools.add(tool)

    def reconcile(self, entry_id: str, actual_cny: float, success: bool = True) -> None:
        """工具执行后对账实际花费。"""
        entry = self._find(entry_id)
        entry["status"] = EntryStatus.COMPLETED.value if success else EntryStatus.FAILED.value
        entry["actual_cny"] = round(actual_cny, 4)
        entry["reserved_cny"] = 0.0
        entry["timestamp"] = self._now()
        self._save()

    def refund(self, entry_id: str) -> None:
        """取消预留而不执行。"""
        entry = self._find(entry_id)
        entry["status"] = EntryStatus.REFUNDED.value
        entry["reserved_cny"] = 0.0
        entry["timestamp"] = self._now()
        self._save()

    # ---- 参考驱动估算 ----

    def estimate_from_reference(
        self,
        video_analysis_brief: dict,
        target_duration_seconds: int,
        tool_plan: dict,
    ) -> dict:
        """基于参考分析 + 目标时长估算制作成本（人民币 CNY）。

        Args:
            video_analysis_brief: 视频分析产物
            target_duration_seconds: 输出视频时长（秒）
            tool_plan: 每种资产类型使用的工具，例如：
                {
                    "image_generation": {"tool": "flux_fal", "cost_per_unit": 0.36},
                    "video_generation": {"tool": "kling_fal", "cost_per_unit": 2.16,
                                         "clip_duration_seconds": 5},
                    "tts": {"tool": "doubao_tts", "cost_per_word": 0.0002},
                    "music": {"tool": "music_gen", "cost_per_track": 0.72},
                }

        Returns:
            逐项成本分解，包含行项目、总计、样本成本和假设说明。
        """
        structure = video_analysis_brief.get("structure_analysis", {})
        pacing = structure.get("pacing_profile", {})
        narration = video_analysis_brief.get("narration_transcript", {})
        ref_duration = video_analysis_brief.get("source", {}).get("duration_seconds", 60)
        pacing_style = pacing.get("pacing_style", "steady_educational")

        # ── 场景数估算 ──
        # 不要单纯线性缩放——使用参考视频的节奏密度。
        # 一个 162 秒 8 个场景的音乐视频有约 3 个切/分钟。
        # 缩放到 60s 应保留切率，而不是降低场景数。
        ref_scenes = structure.get("total_scenes", 8)
        if ref_duration > 0:
            cuts_per_minute = ref_scenes / (ref_duration / 60)
        else:
            cuts_per_minute = 4.0  # 默认：中等节奏

        # 按节奏类型设置最小场景数
        min_scenes_by_pacing = {
            "rapid_fire": 10,
            "dynamic_social": 8,
            "steady_educational": 5,
            "slow_contemplative": 3,
            "variable": 6,
        }
        min_scenes = min_scenes_by_pacing.get(pacing_style, 5)

        density_based_scenes = round(cuts_per_minute * (target_duration_seconds / 60))
        estimated_scenes = max(min_scenes, density_based_scenes)

        # ── 旁白字数 ──
        ref_word_count = narration.get("word_count", 0)
        if ref_duration > 0 and ref_word_count > 0:
            actual_wpm = (ref_word_count / ref_duration) * 60
        else:
            actual_wpm = 150  # 默认对话速度（英文），中文约 200 字/分
        estimated_words = round(actual_wpm * (target_duration_seconds / 60))

        # ── 参考视频运动比例 ──
        scenes_list = structure.get("scenes", [])
        motion_ratio, motion_basis = self._estimate_motion_ratio(
            video_analysis_brief=video_analysis_brief,
            scenes_list=scenes_list,
            pacing_style=pacing_style,
        )

        estimated_motion_scenes = (
            max(1, round(estimated_scenes * motion_ratio))
            if motion_ratio > 0
            else 0
        )
        estimated_still_scenes = estimated_scenes - estimated_motion_scenes

        # ── 视频片段覆盖 ──
        vid_plan = tool_plan.get("video_generation", {})
        clip_duration = vid_plan.get("clip_duration_seconds", 5) if vid_plan else 5
        motion_seconds = target_duration_seconds * motion_ratio
        clips_needed_for_coverage = max(
            estimated_motion_scenes,
            round(motion_seconds / clip_duration)
        ) if vid_plan else 0

        # ── 重试/浪费缓冲 ──
        retry_multiplier = 1.3  # 约 30% 额外用于重试和废弃输出

        # ── 图片数量 ──
        images_per_scene = 2.0 if pacing_style in ("dynamic_social", "rapid_fire") else 1.5
        estimated_images = max(
            estimated_scenes,
            round(estimated_scenes * images_per_scene)
        )

        # 构建行项目
        line_items = []
        assumptions = []

        assumptions.append(
            f"{estimated_scenes} 个场景（参考视频 {cuts_per_minute:.1f} 切/分钟，"
            f"节奏: {pacing_style}）"
        )
        assumptions.append(motion_basis)

        # 图片生成
        img_plan = tool_plan.get("image_generation", {})
        if img_plan:
            img_count = round(estimated_images * retry_multiplier)
            unit_cost = img_plan.get("cost_per_unit", 0.36)
            line_items.append({
                "category": "image_generation",
                "provider": img_plan.get("tool", "unknown"),
                "quantity": img_count,
                "unit_cost_cny": unit_cost,
                "total_cny": round(img_count * unit_cost, 4),
                "basis": (
                    f"~{images_per_scene:.0f} 张/场景 x {estimated_scenes} 场景 "
                    f"+ {round((retry_multiplier - 1) * 100)}% 重试缓冲"
                ),
            })

        # 视频生成
        if vid_plan and clips_needed_for_coverage > 0:
            clip_count = round(clips_needed_for_coverage * retry_multiplier)
            unit_cost = vid_plan.get("cost_per_unit", 2.16)
            line_items.append({
                "category": "video_generation",
                "provider": vid_plan.get("tool", "unknown"),
                "quantity": clip_count,
                "unit_cost_cny": unit_cost,
                "total_cny": round(clip_count * unit_cost, 4),
                "basis": (
                    f"{motion_seconds:.0f}秒动态 / {clip_duration}秒片段 = "
                    f"{clips_needed_for_coverage} 个片段 + 重试缓冲"
                ),
            })
            assumptions.append(
                f"{round(motion_ratio * 100)}% 运动比例 → "
                f"{motion_seconds:.0f}秒需要 {clips_needed_for_coverage} 个片段 "
                f"（每个 {clip_duration}秒）"
            )

        # TTS 旁白
        tts_plan = tool_plan.get("tts", {})
        if tts_plan and estimated_words > 10:
            cost_per_word = tts_plan.get("cost_per_word", 0.0002)
            tts_cost = round(estimated_words * cost_per_word, 4)
            line_items.append({
                "category": "tts_narration",
                "provider": tts_plan.get("tool", "unknown"),
                "quantity": estimated_words,
                "unit_cost_cny": cost_per_word,
                "total_cny": tts_cost,
                "basis": f"旁白 {round(actual_wpm)} 字/分 = 约 {estimated_words} 字",
            })
            assumptions.append(
                f"旁白 {round(actual_wpm)} 字/分 = 约 {estimated_words} 字 "
                f"共 {target_duration_seconds} 秒"
            )

        # 音乐
        music_plan = tool_plan.get("music", {})
        if music_plan:
            music_cost = music_plan.get("cost_per_track", 0.0)
            line_items.append({
                "category": "music",
                "provider": music_plan.get("tool", "unknown"),
                "quantity": 1,
                "unit_cost_cny": music_cost,
                "total_cny": music_cost,
                "basis": "1 首背景音乐",
            })

        subtotal = round(sum(item["total_cny"] for item in line_items), 4)

        # ── 成本范围 ──
        # Low: 一次成功。High: 完全消耗重试缓冲。
        low_total = round(subtotal / retry_multiplier, 4)
        high_total = round(subtotal * 1.15, 4)

        # 样本成本：2 个场景的资产
        sample_scenes = 2
        sample_fraction = sample_scenes / max(estimated_scenes, 1)
        sample_cost = round(subtotal * sample_fraction, 4)

        # 置信度
        if scenes_list and narration.get("word_count", 0) > 0:
            confidence = "high"
        elif scenes_list or narration.get("word_count", 0) > 0:
            confidence = "medium"
        else:
            confidence = "low"

        return {
            "line_items": line_items,
            "total_cny": subtotal,
            "total_range_cny": {"low": low_total, "high": high_total},
            "sample_cost_cny": sample_cost,
            "confidence": confidence,
            "assumptions": assumptions,
            "estimated_scenes": estimated_scenes,
            "estimated_images": estimated_images,
            "estimated_clips": clips_needed_for_coverage,
            "estimated_words": estimated_words,
            "motion_ratio": round(motion_ratio, 2),
            "cuts_per_minute": round(cuts_per_minute, 1),
            "target_duration_seconds": target_duration_seconds,
        }

    def _estimate_motion_ratio(
        self,
        *,
        video_analysis_brief: dict,
        scenes_list: list[dict[str, Any]],
        pacing_style: str,
    ) -> tuple[float, str]:
        """Estimate how much of the target treatment truly needs motion."""
        motion_weights = {
            "animation": 1.0,
            "b_roll": 1.0,
            "stock_footage": 1.0,
            "product_shot": 0.9,
            "transition": 0.6,
            "screen_recording": 0.45,
            "talking_head": 0.35,
            "diagram": 0.25,
            "chart": 0.25,
            "text_card": 0.2,
        }
        classified_weights = [
            motion_weights[visual_type]
            for scene in scenes_list
            if (visual_type := scene.get("visual_type")) in motion_weights
        ]
        if classified_weights:
            ratio = sum(classified_weights) / len(classified_weights)
            unknown_count = max(0, len(scenes_list) - len(classified_weights))
            if unknown_count:
                fallback_ratio, _ = self._fallback_motion_ratio(
                    video_analysis_brief=video_analysis_brief,
                    pacing_style=pacing_style,
                )
                ratio = (
                    (sum(classified_weights) + fallback_ratio * unknown_count)
                    / len(scenes_list)
                )
                basis = (
                    "motion ratio blended from classified scene types and "
                    "reference-style fallback for unclassified scenes"
                )
            else:
                basis = "motion ratio derived from classified scene types"
            return round(min(max(ratio, 0.0), 0.95), 2), basis

        return self._fallback_motion_ratio(
            video_analysis_brief=video_analysis_brief,
            pacing_style=pacing_style,
        )

    def _fallback_motion_ratio(
        self,
        *,
        video_analysis_brief: dict,
        pacing_style: str,
    ) -> tuple[float, str]:
        """Fallback heuristic for motion ratio before scene vision enrichment."""
        source_type = video_analysis_brief.get("source", {}).get("type", "")
        replication = video_analysis_brief.get("replication_guidance", {})
        motion_required = bool(replication.get("motion_required"))
        suggested_pipeline = replication.get("suggested_pipeline", "")

        base_by_pacing = {
            "rapid_fire": 0.8,
            "dynamic_social": 0.65,
            "steady_educational": 0.35,
            "slow_contemplative": 0.2,
            "variable": 0.5,
        }
        ratio = base_by_pacing.get(pacing_style, 0.5)

        if source_type in ("shorts", "instagram", "tiktok"):
            ratio = max(ratio, 0.7)
        if motion_required:
            ratio = max(ratio, 0.6)
        if suggested_pipeline == "cinematic":
            ratio = max(ratio, 0.55)

        ratio = round(min(max(ratio, 0.1), 0.95), 2)
        basis = (
            "motion ratio inferred from pacing/style because scene visual types "
            "have not been enriched yet"
        )
        return ratio, basis

    # ---- 持久化 ----

    def _save(self) -> None:
        if self.cost_log_path is None:
            return
        data = {
            "version": "2.0",
            "budget_total_cny": self.budget_total_cny,
            "budget_reserved_cny": round(self.budget_reserved_cny, 4),
            "budget_spent_cny": round(self.budget_spent_cny, 4),
            "entries": self.entries,
        }
        self.cost_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cost_log_path, "w") as f:
            json.dump(data, f, indent=2)

    def _load(self) -> None:
        with open(self.cost_log_path) as f:  # type: ignore[arg-type]
            data = json.load(f)
        self.entries = data.get("entries", [])
        # 兼容旧版 USD 字段，新版使用 CNY
        if "budget_total_cny" in data:
            self.budget_total_cny = data["budget_total_cny"]
        elif "budget_total_usd" in data:
            self.budget_total_cny = data["budget_total_usd"] * 7.2

    # ---- Helpers ----

    def _find(self, entry_id: str) -> dict[str, Any]:
        for entry in self.entries:
            if entry["id"] == entry_id:
                return entry
        raise KeyError(f"Cost entry {entry_id!r} not found")

    @staticmethod
    def _new_id() -> str:
        return uuid.uuid4().hex[:12]

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()
