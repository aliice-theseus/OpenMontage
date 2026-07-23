# 剪辑导演 — 解说片流水线

## 使用时机

你是生成式解说视频的剪辑师。你有一个包含所有生成文件的 `asset_manifest`、一个带有视觉结构的 `scene_plan`、以及一个带有时间安排的 `script`。你的工作是组装编辑决策列表（EDL）：何时播放什么、元素如何分层、字幕去哪里、音乐和旁白如何交互。

这是原始资产变成连贯视频的地方。好的剪辑能让平庸的资产发光；差的剪辑会浪费出色的资产。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/edit_decisions.schema.json` | 工件验证 |
| 前置工件 | `state.artifacts["assets"]["asset_manifest"]`、`state.artifacts["scene_plan"]["scene_plan"]`、`state.artifacts["script"]["script"]` | 资产、视觉计划、时序 |
| 剧本 | 活动风格剧本 | 过渡、节奏规则、叠加样式 |

## 流程

### 步骤 1a：识别音频类型 — 旁白 vs 对话原生音频

**关键区分：** 脚本中有两种音频来源：

| 类型 | section_type | 音频来源 | 说明 |
|------|-------------|----------|------|
| **旁白（TTS）** | `"narration"` | `tts_selector` 生成的独立音频文件 | 传统画外音，assets 阶段生成 |
| **对话（原生）** | `"dialogue"` | Seedance 视频片段内嵌的音频 | 角色对话附带口型同步，无独立音频文件 |

遍历脚本的 `sections`，按 `section_type` 分类。对话章节对应的视频片段在 `asset_manifest` 中标记为 `has_native_audio: true`，这些片段在合成时不应叠加 TTS。

### 步骤 1b：将资产映射到时间线

对于场景计划中的每个场景：
1. 从资产清单中找到匹配的资产（按 `scene_id`）
2. 检查脚本章节的 `section_type`：
   - `"narration"` → 找到匹配的旁白音频（按脚本章节）
   - `"dialogue"` → 无旁白音频，视频片段自带对话音频
3. 注意场景的时序（`start_seconds`、`end_seconds`）

构建时间线映射（使用 `audio_source` 标注音频类型）：
```
0s-10s：场景-1（talking_head） | 旁白(TTS) s1    | img-intro.png
10s-18s：场景-2（diagram）      | 旁白(TTS) s2    | diagram-flow.svg
18s-25s：场景-3（dialogue）     | 对话(原生) s3   | seedance_dialogue_s3.mp4 [has_native_audio]
25s-35s：场景-4（animation）    | 旁白(TTS) s4    | img-animation.png
...
```

### 步骤 2：定义剪辑

每个剪辑定义显示什么视觉以及何时显示：

```json
{
  "id": "cut-1",
  "source": "img-scene-1",
  "in_seconds": 0,
  "out_seconds": 10,
  "layer": "primary",
  "transform": {
    "scale": 1.0,
    "position": "center",
    "animation": "ken-burns-slow-zoom"
  },
  "transition_in": "fade",
  "transition_out": "dissolve",
  "transition_duration": 0.4
}
```

**分层规则：**
- `primary` — 主要视觉（一次一个）
- `overlay` — 文字卡片、统计卡片、关键术语（在主视觉之上）
- `background` — 所有内容后面的纯色或纹理

### 步骤 3：配置字幕

所有解说内容必须包含字幕：

```json
{
  "subtitles": {
    "enabled": true,
    "style": "word-by-word",
    "font": "Inter",
    "font_size": 48,
    "color": "#FFFFFF",
    "background": "#00000088",
    "position": "bottom-center",
    "max_words_per_line": 8
  }
}
```

**字幕计时**：从旁白音频时间戳推导。每个词应在被说出时高亮（逐词风格）或以短语块显示（短语风格）。

使用剧本的排版字体选择。

### 步骤 4：配置音频层

**规则：对话片段不叠加 TTS。** 如果视频片段标记为 `has_native_audio: true`（即对话章节），其音频已在 Seedance 生成时嵌入。在编辑时间线中，该片段的时段不安排任何旁白音频。

```json
{
  "audio": {
    "narration": {
      "segments": [
        { "asset_id": "narration-s1", "start_seconds": 0, "end_seconds": 10 },
        { "asset_id": "narration-s2", "start_seconds": 10, "end_seconds": 18 },
        // 18-25s 是 dialogue 章节，无旁白
        { "asset_id": "narration-s4", "start_seconds": 25, "end_seconds": 35 }
      ]
    },
    "music": {
      "asset_id": "music-bg",
      "volume": 0.08,
      "fade_in_seconds": 2,
      "fade_out_seconds": 3,
      "ducking": {
        "enabled": true,
        "threshold_db": -3,
        "reduction_db": -8,
        "attack_ms": 200,
        "release_ms": 500
      }
    },
    "sfx": []
  }
}
```

**旁白时段**：narration 章节使用 TTS 生成的独立音频。dialogue 章节对应的时段在 `narration.segments` 中**跳过**。

**音乐闪避**：旁白播放时音乐音量降低，停顿期间升高。使用剧本的 `audio.ducking_threshold_db`。
- 对话片段播放时（18-25s）音乐应保持低位或静音，避免与 Seedance 原生对话音频冲突
- 建议对话时音乐闪避更积极：`reduction_db: -12`，`threshold_db: -6`

### 步骤 5：应用节奏规则

检查剧本的 `motion.pacing_rules`：
- 没有剪辑短于 `min_scene_hold_seconds`
- 没有剪辑长于 `max_scene_hold_seconds`
- 文字卡片保持 `text_card_hold_seconds`
- 过渡使用 `transition_duration_seconds`

如果有任何违反这些规则的情况，调整剪辑计时。

### 步骤 6：验证剪辑完整性

**时间线覆盖：**
- [ ] 剪辑覆盖完整视频时长（无黑帧）
- [ ] 没有重叠的主要剪辑
- [ ] scene_plan 中的每个场景至少有一个对应的剪辑

**资产引用：**
- [ ] 每个剪辑的 `source` 引用清单中的有效 asset_id
- [ ] 每个旁白段落引用有效的音频资产
- [ ] 音乐资产存在

**音频同步：**
- [ ] 旁白段落有序且不重叠
- [ ] dialogue 章节对应的时段无旁白音频
- [ ] 对话视频片段（`has_native_audio: true`）的音频未与 TTS 混叠
- [ ] 旁白计时与对应的视觉剪辑对齐
- [ ] 音乐闪避已配置，对话期间闪避更积极

**字幕：**
- [ ] 字幕已启用
- [ ] 字幕样式使用与剧本兼容的字体和颜色

### 步骤 7：自我评估

评分（1-5）：

| 标准 | 问题 |
|-----------|----------|
| **连续性** | 视频的每一秒都有视觉吗？ |
| **节奏** | 剪辑是否遵循剧本的计时规则？ |
| **音视频同步** | 每个时刻你看到的和听到的是否匹配？ |
| **字幕质量** | 字幕是否可读且计时正确？ |
| **过渡连贯性** | 过渡是否遵循剧本的允许集合？ |

如果任何维度得分低于 3，修订。

### 步骤 8：提交

对照模式验证 edit_decisions 工件并通过检查点持久化。

## 常见陷阱

- **忘记空白**：如果场景-1 在 10 秒结束而场景-2 在 10.5 秒开始，就有 0.5 秒的黑帧。检查空白。
- **音频漂移**：旁白音频可能比计划稍长/稍短。调整视觉剪辑以匹配实际旁白时长，而不是计划时长。
- **没有闪避**：旁白下音乐满音量播放使视频无法观看。始终配置闪避。
- **到处相同的过渡**：变化过渡创造节奏。使用剧本的允许集合，但不要对每个剪辑使用相同的过渡。
- **字幕字体不匹配**：字幕应使用剧本的正文字体，而不是随机的默认字体。
