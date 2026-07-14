# `SCRIPT.md` — 锁定解说词（可选）

项目的**锁定解说词**：最终的台词 + 声音 + 表达方式。这是一个_可选的_计划层文件——仅 bgm、无声叠加的视频没有解说词文件。故事板每帧的 `voiceover` 是较轻松、可编辑的_指南_；`SCRIPT.md` 是_提交版本_。（故事板格式 → `references/storyboard-format.md`。）

本文件仅定义 SCRIPT.md **形状**。将台词合成为音频是 `hyperframes-media` → `references/tts.md` 拥有的能力。

自由格式的 markdown — 没有严格的解析器；Studio 在故事板旁边以只读方式渲染它，TTS 步骤提取缩进的台词。

## 形状

一个头部块，然后每个台词一个章节。

| 部分                           | 包含                                                                 |
| ------------------------------ | -------------------------------------------------------------------- |
| 头部                           | `**Voice:**`（提供商 + 声音）、`**Voice settings:**`（例如 stability / similarity / style）、`**Voice direction:**`（整体表达方式） |
| `## Line N — <label> (Frame N)` | 一条台词，关联到其故事板帧                                           |
| `**Time:**`                    | 大致的窗口时间——一个_指南_，非权威来源（实际时间来自 TTS 词级时间戳） |
| `**Delivery:**`                | 每行表达注释                                                         |
| 缩进块                          | **台词文本**——唯一送入 TTS 的部分                                     |

## 示例

```markdown
# SCRIPT — acme-launch

**Voice:** Rachel (ElevenLabs)
**Voice settings:** stability 0.35 · similarity 0.75 · style 0.20
**Voice direction:** 自信、温暖、略带俏皮。

---

## Line 1 — Hook (Frame 1)

**Time:** 0.0 – 3.0s
**Delivery:** 在节拍上落地承诺。

    Ship a launch video in an afternoon.

## Line 2 — The problem (Frame 2)

**Time:** 3.0 – 7.0s
**Delivery:** 苦笑，略带疲惫。

    The old way? Prompt, wait twenty minutes, get something that misses.
```

## 到 TTS

将每行的台词文本送入 `npx hyperframes tts`（使用头部的 `--voice` / `--provider`；捕获词级时间戳用于字幕）。实际的逐词时间戳替换 `**Time:**` 指南。CLI 约定 → `hyperframes-media/references/tts.md`。
