"""Contracts for document-derived director skills and pipeline routing."""

from pathlib import Path

from tools.base_tool import BaseTool, ToolResult
from tools.video.video_selector import VideoSelector


ROOT = Path(__file__).resolve().parents[2]
SKILLS = {
    "direct-action-scenes": "action-language.md",
    "direct-visual-quality": "visual-treatment-library.md",
    "direct-camera-movement": "camera-language.md",
}


class _ProviderStub(BaseTool):
    name = "provider_stub"
    agent_skills = ["provider-specific-skill"]

    def execute(self, inputs: dict) -> ToolResult:
        return ToolResult(success=True)


def test_director_skills_have_complete_packages():
    for skill_name, reference_name in SKILLS.items():
        skill_dir = ROOT / ".agents" / "skills" / skill_name
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        metadata_text = (skill_dir / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )

        assert skill_text.startswith(f"---\nname: {skill_name}\n")
        assert "TODO" not in skill_text
        assert (skill_dir / "references" / reference_name).is_file()
        assert f"${skill_name}" in metadata_text


def test_video_selector_exposes_base_and_conditional_director_skills():
    selector = VideoSelector()
    info = selector.get_info()
    payload = selector._tool_context_payload(_ProviderStub())

    assert info["conditional_agent_skills"]["action_or_combat_scene"] == [
        "direct-action-scenes"
    ]
    assert "direct-visual-quality" in payload["required_agent_skills"]
    assert "direct-camera-movement" in payload["required_agent_skills"]
    assert "provider-specific-skill" in payload["required_agent_skills"]
    assert payload["conditional_agent_skills"]["action_or_combat_scene"] == [
        "direct-action-scenes"
    ]


def test_pipeline_stage_guidance_routes_director_skills():
    shared = (ROOT / "skills" / "creative" / "video-gen-prompting.md").read_text(
        encoding="utf-8"
    )
    for skill_name in SKILLS:
        assert skill_name in shared

    for pipeline in ("explainer", "animation", "cinematic"):
        scene_director = (
            ROOT / "skills" / "pipelines" / pipeline / "scene-director.md"
        ).read_text(encoding="utf-8")
        assert "skills/creative/video-gen-prompting.md" in scene_director

    expected_routes = {
        "skills/pipelines/hybrid/scene-director.md": SKILLS,
        "skills/pipelines/avatar-spokesperson/scene-director.md": {
            "direct-visual-quality",
            "direct-camera-movement",
        },
        "skills/pipelines/character-animation/scene-director.md": {
            "direct-camera-movement",
            "direct-action-scenes",
        },
        "skills/pipelines/character-animation/edit-director.md": {
            "direct-action-scenes",
        },
        "skills/pipelines/cinematic/edit-director.md": {
            "direct-action-scenes",
        },
        "skills/pipelines/explainer/asset-director.md": {
            "direct-action-scenes",
            "required_agent_skills",
        },
        "skills/pipelines/animation/asset-director.md": {
            "direct-action-scenes",
            "required_agent_skills",
        },
        "skills/pipelines/cinematic/asset-director.md": {
            "direct-action-scenes",
            "required_agent_skills",
        },
        "skills/pipelines/hybrid/asset-director.md": {
            "direct-action-scenes",
            "required_agent_skills",
        },
    }
    for relative_path, required_skills in expected_routes.items():
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for skill_name in required_skills:
            assert skill_name in text, f"{relative_path} does not route {skill_name}"
