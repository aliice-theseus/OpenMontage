"""角色身份注册表 — 跨视频角色一致性管理。

当同一项目需要制作多个视频（如系列短片、多集解说），
角色身份注册表确保后续视频可以使用与前一集相同的角色形象。

工作流程::

    1. 第一个视频的 character_design 阶段锁定角色 → 写入注册表
    2. 后续视频的 character_design 阶段先查询注册表
    3. 如果找到已有角色，复用 identity_lock 包，跳过生成四视图
    4. 如果需要新角色或更新现有角色，正常生成并更新注册表

文件存储: ``projects/<project-id>/character_registry.json``
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ---------------------------------------------------------------------------
# 角色身份锁 — 一个角色的完整身份包
# ---------------------------------------------------------------------------

@dataclass
class CharacterIdentity:
    """角色身份锁定记录。

    包含角色的四视图种子、提示词和参考图路径，
    供后续视频或同一视频的不同阶段复用。
    """
    character_id: str
    display_name: str
    seed_image_path: str          # 最清晰的角色正面照路径
    image_path_front: str
    image_path_side: str
    image_path_back: str
    prompt: str                   # 生成四视图使用的完整提示词
    identity_phrases: list[str]   # 身份锁定短语列表
    source_tool: str
    seed: Optional[int] = None
    description: str = ""
    visual_style: str = ""
    registered_at: str = ""


# ---------------------------------------------------------------------------
# 注册表
# ---------------------------------------------------------------------------

class CharacterRegistry:
    """角色身份注册表，存储在项目目录中。

    Args:
        registry_dir: 注册表文件所在目录。通常为 ``projects/<project-id>/``。
    """

    def __init__(self, registry_dir: Path) -> None:
        self._path = registry_dir / "character_registry.json"
        self._identities: dict[str, CharacterIdentity] = {}
        self._load()

    # ------------------------------------------------------------------
    # 持久化
    # ------------------------------------------------------------------

    def _load(self) -> None:
        if not self._path.is_file():
            return
        try:
            with open(self._path, encoding="utf-8") as f:
                data = json.load(f)
            for item in data.get("identities", []):
                identity = CharacterIdentity(**item)
                self._identities[identity.character_id] = identity
        except (json.JSONDecodeError, KeyError, TypeError):
            # 损坏的注册表文件，从头开始
            self._identities = {}

    def save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "1.0",
            "project_id": self._path.parent.name,
            "identities": [asdict(id) for id in self._identities.values()],
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------
    # 查询
    # ------------------------------------------------------------------

    def has(self, character_id: str) -> bool:
        return character_id in self._identities

    def get(self, character_id: str) -> Optional[CharacterIdentity]:
        return self._identities.get(character_id)

    def list_all(self) -> list[CharacterIdentity]:
        return list(self._identities.values())

    # ------------------------------------------------------------------
    # 注册
    # ------------------------------------------------------------------

    def register(self, identity: CharacterIdentity) -> None:
        """注册或更新一个角色身份。

        如果 character_id 已存在则更新，否则新增。
        """
        if not identity.registered_at:
            identity.registered_at = datetime.now(timezone.utc).isoformat()
        self._identities[identity.character_id] = identity
        self.save()

    def register_from_character_design(
        self,
        character_design_artifact: dict[str, Any],
    ) -> list[str]:
        """从 character_design 产物中批量注册角色。

        Args:
            character_design_artifact: 符合 ``character_design.schema.json`` 的产物。

        Returns:
            新注册的角色 ID 列表。
        """
        registered: list[str] = []
        identity_lock = character_design_artifact.get("identity_lock", {})

        for char in character_design_artifact.get("characters", []):
            char_id = char.get("id", "")
            if not char_id:
                continue

            identity = CharacterIdentity(
                character_id=char_id,
                display_name=char.get("display_name", char_id),
                seed_image_path=identity_lock.get("seed_image_path", ""),
                image_path_front=char.get("image_path_front", ""),
                image_path_side=char.get("image_path_side", ""),
                image_path_back=char.get("image_path_back", ""),
                prompt=char.get("prompt", ""),
                identity_phrases=identity_lock.get("identity_phrases", []),
                source_tool=char.get("source_tool", ""),
                seed=char.get("seed"),
                description=char.get("description", ""),
                visual_style=char.get("style", ""),
            )
            self.register(identity)
            registered.append(char_id)

        return registered

    # ------------------------------------------------------------------
    # 工具函数 — 为 Seedance 等工具构建 reference 参数
    # ------------------------------------------------------------------

    def build_reference_config(
        self,
        character_ids: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """构建视频生成工具（如 Seedance）的 reference 配置。

        Args:
            character_ids: 需要引用的角色 ID 列表。为 None 时使用所有已注册角色。

        Returns:
            可直接传入 ``video_selector`` 或 ``seedance_video`` 的 ``reference_image_urls``
            和 ``identity_lock`` 参数字段。
        """
        identities = (
            [self._identities[cid] for cid in character_ids if cid in self._identities]
            if character_ids
            else list(self._identities.values())
        )

        reference_image_urls: list[str] = []
        all_phrases: list[str] = []

        for identity in identities:
            if identity.seed_image_path:
                reference_image_urls.append(identity.seed_image_path)
            # 也加入四视图中的正面照
            if identity.image_path_front and identity.image_path_front != identity.seed_image_path:
                reference_image_urls.append(identity.image_path_front)
            all_phrases.extend(identity.identity_phrases)

        return {
            "reference_image_urls": reference_image_urls,
            "identity_lock": {
                "enabled": len(reference_image_urls) > 0,
                "phrases": all_phrases,
            },
        }
