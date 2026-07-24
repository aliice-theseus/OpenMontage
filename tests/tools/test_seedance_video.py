"""Tests for Seedance 2.0 via 火山引擎 Ark (tools/video/seedance_video.py).

Covers:
- Config resolution (API key, endpoint ID from env vs defaults)
- Tool metadata (name, version, capabilities, quality score)
- Cost and runtime estimation
- Content array construction (text-only, with images, with video/audio references)
- Local file to data URI conversion
- Input validation (reference count limits)
- Execute path with missing API key

These tests do NOT make real API calls — they validate the tool's
configuration, estimation, and input-building logic in isolation.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from tools.video.seedance_video import (
    SeedanceVideo,
)


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------


@pytest.fixture
def tool() -> SeedanceVideo:
    return SeedanceVideo()


@pytest.fixture
def tool_with_key(monkeypatch) -> SeedanceVideo:
    monkeypatch.setenv("ARK_API_KEY", "ark-test-key-12345")
    monkeypatch.setenv("SEEDANCE_ENDPOINT_ID", "ep-test-endpoint-001")
    monkeypatch.setenv("SEEDANCE_API_BASE", "https://ark-test.example.com/api/v3")
    return SeedanceVideo()


@pytest.fixture
def sample_image(tmp_path) -> Path:
    p = tmp_path / "test_img.png"
    p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    return p


def valid_reference_contract() -> dict:
    return {
        "operation": "reference_to_video",
        "require_identity_lock": True,
        "reference_image_urls": [
            "https://example.com/character-turnaround.jpg",
            "https://example.com/scene-sketch.jpg",
        ],
        "reference_image_roles": ["character_turnaround", "scene_sketch"],
        "prompt": (
            "@Image1 是角色四视图，the same character, no drift, no face morph。\n"
            "@Image2 是场景草图，保持该构图。"
        ),
    }


# ----------------------------------------------------------------------
# Config resolution
# ----------------------------------------------------------------------


class TestConfig:
    def test_api_key_from_env(self, monkeypatch):
        monkeypatch.setenv("ARK_API_KEY", "ark-from-env")
        t = SeedanceVideo()
        assert t._get_api_key() == "ark-from-env"

    def test_api_key_missing(self):
        original = os.environ.pop("ARK_API_KEY", None)
        try:
            t = SeedanceVideo()
            assert t._get_api_key() is None
        finally:
            if original is not None:
                os.environ["ARK_API_KEY"] = original

    def test_endpoint_id_from_env(self, monkeypatch):
        monkeypatch.setenv("SEEDANCE_ENDPOINT_ID", "ep-custom")
        t = SeedanceVideo()
        assert t._get_endpoint_id() == "ep-custom"

    def test_endpoint_id_default_is_none(self):
        original = os.environ.pop("SEEDANCE_ENDPOINT_ID", None)
        try:
            t = SeedanceVideo()
            assert t._get_endpoint_id() is None
        finally:
            if original is not None:
                os.environ["SEEDANCE_ENDPOINT_ID"] = original

    def test_api_base_from_env(self, monkeypatch):
        monkeypatch.setenv("SEEDANCE_API_BASE", "https://ark-custom.example.com/api/v3")
        t = SeedanceVideo()
        assert os.environ.get("SEEDANCE_API_BASE") == "https://ark-custom.example.com/api/v3"

    def test_execute_fails_without_endpoint_id(self, monkeypatch):
        monkeypatch.setenv("ARK_API_KEY", "ark-test-key")
        monkeypatch.setenv("SEEDANCE_API_BASE", "https://ark.example.com/api/v3")
        original_eid = os.environ.pop("SEEDANCE_ENDPOINT_ID", None)
        try:
            t = SeedanceVideo()
            result = t.execute({"prompt": "test"})
            assert result.success is False
            assert "SEEDANCE_ENDPOINT_ID" in result.error
        finally:
            if original_eid is not None:
                os.environ["SEEDANCE_ENDPOINT_ID"] = original_eid

    def test_execute_fails_without_api_base(self, monkeypatch):
        monkeypatch.setenv("ARK_API_KEY", "ark-test-key")
        monkeypatch.setenv("SEEDANCE_ENDPOINT_ID", "ep-test")
        original_base = os.environ.pop("SEEDANCE_API_BASE", None)
        try:
            t = SeedanceVideo()
            result = t.execute({"prompt": "test"})
            assert result.success is False
            assert "SEEDANCE_API_BASE" in result.error
        finally:
            if original_base is not None:
                os.environ["SEEDANCE_API_BASE"] = original_base

    def test_status_available_when_key_set(self, monkeypatch):
        monkeypatch.setenv("ARK_API_KEY", "ark-any-key")
        t = SeedanceVideo()
        assert t.get_status().value == "available"

    def test_status_unavailable_when_key_missing(self):
        original = os.environ.pop("ARK_API_KEY", None)
        try:
            t = SeedanceVideo()
            assert t.get_status().value == "unavailable"
        finally:
            if original is not None:
                os.environ["ARK_API_KEY"] = original


# ----------------------------------------------------------------------
# Tool metadata
# ----------------------------------------------------------------------


class TestMetadata:
    def test_name(self, tool):
        assert tool.name == "seedance_video"

    def test_version(self, tool):
        assert tool.version == "0.4.0"

    def test_capabilities(self, tool):
        assert "text_to_video" in tool.capabilities
        assert "image_to_video" in tool.capabilities
        assert "reference_to_video" in tool.capabilities

    def test_quality_score(self, tool):
        assert tool.quality_score == 0.95

    def test_runtime(self, tool):
        assert tool.runtime.value == "api"

    def test_supports_native_audio(self, tool):
        assert tool.supports["native_audio"] is True

    def test_supports_reference_image(self, tool):
        assert tool.supports["reference_image"] is True

    def test_input_schema_requires_prompt(self, tool):
        assert "prompt" in tool.input_schema["required"]

    def test_input_schema_ratio_enum(self, tool):
        ratios = tool.input_schema["properties"]["ratio"]["enum"]
        assert "16:9" in ratios
        assert "9:16" in ratios

    def test_input_schema_resolution_includes_1080p(self, tool):
        resolutions = tool.input_schema["properties"]["resolution"]["enum"]
        assert "1080p" in resolutions

    def test_input_schema_duration_bounds(self, tool):
        props = tool.input_schema["properties"]["duration"]
        assert props["minimum"] == 4
        assert props["maximum"] == 15
        assert props["default"] == 5

    def test_install_instructions_mentions_ark(self, tool):
        assert "ARK_API_KEY" in tool.install_instructions

    def test_side_effects_mentions_ark(self, tool):
        assert any("Ark" in s or "ark" in s.lower() for s in tool.side_effects)

    def test_agent_skills(self, tool):
        assert "seedance-2-0" in tool.agent_skills
        assert "ai-video-gen" in tool.agent_skills

    def test_fallback_tools(self, tool):
        assert "wan_video" in tool.fallback_tools


# ----------------------------------------------------------------------
# Cost and runtime estimation
# ----------------------------------------------------------------------


class TestEstimation:
    def test_estimate_cost_default(self, tool):
        cost = tool.estimate_cost({"duration": 5, "resolution": "720p"})
        assert isinstance(cost, float)
        assert cost > 0

    def test_estimate_cost_1080p_higher_than_720p(self, tool):
        cost_720 = tool.estimate_cost({"duration": 5, "resolution": "720p"})
        cost_1080 = tool.estimate_cost({"duration": 5, "resolution": "1080p"})
        assert cost_1080 > cost_720

    def test_estimate_cost_longer_duration_higher(self, tool):
        cost_5s = tool.estimate_cost({"duration": 5, "resolution": "720p"})
        cost_10s = tool.estimate_cost({"duration": 10, "resolution": "720p"})
        assert cost_10s > cost_5s

    def test_estimate_runtime_default(self, tool):
        rt = tool.estimate_runtime({"duration": 5})
        assert isinstance(rt, float)
        assert rt > 0

    def test_estimate_runtime_scales_with_duration(self, tool):
        rt_5 = tool.estimate_runtime({"duration": 5})
        rt_10 = tool.estimate_runtime({"duration": 10})
        assert rt_10 > rt_5


# ----------------------------------------------------------------------
# Content array construction
# ----------------------------------------------------------------------


class TestBuildContentArray:
    def test_text_only(self, tool):
        content = tool._build_content_array({"prompt": "a cat"})
        assert len(content) == 1
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "a cat"

    def test_with_image_url(self, tool):
        content = tool._build_content_array({
            "prompt": "a cat",
            "image_url": "https://example.com/cat.jpg",
        })
        assert len(content) == 2
        assert content[0]["type"] == "text"
        assert content[1]["type"] == "image_url"
        assert content[1]["image_url"]["url"] == "https://example.com/cat.jpg"
        assert content[1]["role"] == "reference_image"

    def test_with_image_path(self, tool, sample_image):
        content = tool._build_content_array({
            "prompt": "a cat",
            "image_path": str(sample_image),
        })
        assert len(content) == 2
        assert content[1]["type"] == "image_url"
        assert content[1]["image_url"]["url"].startswith("data:image/png;base64,")

    def test_with_reference_images(self, tool):
        content = tool._build_content_array({
            "prompt": "a cat",
            "reference_image_urls": [
                "https://example.com/img1.jpg",
                "https://example.com/img2.jpg",
            ],
        })
        # text + 2 images
        assert len(content) == 3
        assert content[1]["role"] == "reference_image"
        assert content[2]["role"] == "reference_image"

    def test_with_reference_video(self, tool):
        content = tool._build_content_array({
            "prompt": "a cat",
            "reference_video_urls": ["https://example.com/vid.mp4"],
        })
        assert len(content) == 2
        assert content[1]["type"] == "video_url"
        assert content[1]["role"] == "reference_video"

    def test_with_reference_audio(self, tool):
        content = tool._build_content_array({
            "prompt": "a cat",
            "reference_audio_urls": ["https://example.com/audio.mp3"],
        })
        assert len(content) == 2
        assert content[1]["type"] == "audio_url"
        assert content[1]["role"] == "reference_audio"

    def test_full_multimodal(self, tool):
        content = tool._build_content_array({
            "prompt": "a commercial",
            "image_url": "https://example.com/start.jpg",
            "reference_image_urls": ["https://example.com/ref1.jpg"],
            "reference_video_urls": ["https://example.com/clip.mp4"],
            "reference_audio_urls": ["https://example.com/bgm.mp3"],
        })
        # text + 2 images + 1 video + 1 audio
        assert len(content) == 5

    def test_image_count_limit(self, tool):
        urls = [f"https://example.com/{i}.jpg" for i in range(10)]
        with pytest.raises(ValueError, match="最多接受 9 张参考图片"):
            tool._build_content_array({
                "prompt": "test",
                "reference_image_urls": urls,
            })

    def test_video_count_limit(self, tool):
        urls = [f"https://example.com/{i}.mp4" for i in range(4)]
        with pytest.raises(ValueError, match="最多接受 3 个参考视频"):
            tool._build_content_array({
                "prompt": "test",
                "reference_video_urls": urls,
            })

    def test_audio_count_limit(self, tool):
        urls = [f"https://example.com/{i}.mp3" for i in range(4)]
        with pytest.raises(ValueError, match="最多接受 3 个参考音频"):
            tool._build_content_array({
                "prompt": "test",
                "reference_audio_urls": urls,
            })

    def test_image_path_not_found(self, tool):
        with pytest.raises(FileNotFoundError, match="文件不存在"):
            tool._build_content_array({
                "prompt": "test",
                "image_path": "/nonexistent/path.png",
            })


# ----------------------------------------------------------------------
# Data URI conversion
# ----------------------------------------------------------------------


class TestFileToDataUri:
    def test_png_to_data_uri(self, tool, sample_image):
        uri = tool._file_to_data_uri(str(sample_image))
        assert uri.startswith("data:image/png;base64,")

    def test_jpg_to_data_uri(self, tool, tmp_path):
        p = tmp_path / "test.jpg"
        p.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 50)
        uri = tool._file_to_data_uri(str(p))
        assert uri.startswith("data:image/jpeg;base64,")

    def test_file_not_found(self, tool):
        with pytest.raises(FileNotFoundError):
            tool._file_to_data_uri("/not/a/real/file.mp4")


# ----------------------------------------------------------------------
# Execute path — no network
# ----------------------------------------------------------------------


class TestExecute:
    def test_execute_fails_without_api_key(self, tool):
        original = os.environ.pop("ARK_API_KEY", None)
        try:
            result = tool.execute({"prompt": "test"})
            assert result.success is False
            assert "ARK_API_KEY" in result.error
        finally:
            if original is not None:
                os.environ["ARK_API_KEY"] = original

    def test_execute_fails_with_bad_image_path(self, tool_with_key):
        inputs = valid_reference_contract()
        inputs["image_path"] = "/nonexistent/path.png"
        result = tool_with_key.execute(inputs)
        assert result.success is False
        assert "nonexistent/path.png" in result.error

    def test_execute_fails_with_too_many_images(self, tool_with_key):
        urls = [f"https://example.com/{i}.jpg" for i in range(10)]
        inputs = valid_reference_contract()
        inputs["reference_image_urls"] = urls
        inputs["reference_image_roles"] = [
            "character_turnaround", "scene_sketch", *(["style_reference"] * 8)
        ]
        inputs["prompt"] = "\n".join(
            [
                "@Image1 是角色四视图，the same character, no drift, no face morph。",
                "@Image2 是场景草图，保持该构图。",
                *[f"@Image{i} 是风格参考。" for i in range(3, 11)],
            ]
        )
        result = tool_with_key.execute(inputs)
        assert result.success is False
        assert "最多接受 9 张" in result.error

    def test_execute_rejects_text_to_video_even_when_bypass_flag_is_set(self, tool_with_key):
        result = tool_with_key.execute({
            "prompt": "纯文本生成",
            "operation": "text_to_video",
            "_confirm_skip_identity_lock": True,
        })

        assert result.success is False
        assert "reference_to_video" in result.error

    def test_execute_requires_turnaround_and_scene_sketch(self, tool_with_key):
        inputs = valid_reference_contract()
        inputs["reference_image_roles"] = ["character_turnaround", "style_reference"]

        result = tool_with_key.execute(inputs)

        assert result.success is False
        assert "scene_sketch" in result.error
