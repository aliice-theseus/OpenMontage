# LTX-2 — 提示指南

> 来源：[LTX 官方提示指南](https://docs.ltx.video/api-documentation/prompting-guide)
> 通用词汇表请参见：`skills/creative/video-gen-prompting.md`

## LTX 特定的 6 元素结构

LTX-2 使用清晰、专注的提示结构：

1. **建立镜头** — 匹配你流派的电影摄影术语
2. **设置场景** — 光照、调色板、纹理、氛围
3. **描述动作** — 从开始到结束的自然序列
4. **定义角色** — 物理线索（年龄、头发、衣服），非抽象标签
5. **相机运动** — 指定方式和时机；描述运动后出现的内容。（LTX 遵循平移/旋转/镜头的区分：`dolly` ≠ `zoom`、`pan` ≠ `truck`。选择正确的家族 — 平移移动支架、旋转转动支架、纯镜头在不移动相机的情况下改变焦距或焦平面。）
6. **描述音频** — 环境音、音乐、语音或歌唱

### 严格静态镜头规则

如果你写"static camera"，镜头必须没有运动、没有对焦变化、没有变焦。LTX 字面理解"static" — 稍后提示中添加任何运动动词要么被忽略，要么产生相机自相矛盾的故障。选择一个：静态，或一个单一命名的运动。

## LTX 特定技巧

### 运动后描述
当你描述结果时，LTX 渲染相机运动更准确：
- 替代："Camera pans left"
- 改为："Camera pans left to reveal a bustling market square"

### 音频提示（LTX-2 独有）
LTX-2 生成同步音频。使用特定描述词：

| 类别 | 示例 |
|------|------|
| **环境音** | "coffeeshop noise", "wind and rain", "forest with birdsong" |
| **语音风格** | "energetic announcer", "resonant voice with gravitas", "childlike curiosity" |
| **音量** | "whisper", "mutter", "shout", "scream" |
| **音乐** | "soft acoustic guitar", "electronic beat building" |

对话放在引号中：`The narrator says: "Welcome to the future."`
指定语言/口音：`speaks in British English with a warm tone`

### 风格类别
LTX 将风格组织为三个家族：

**动画**：定格动画、2D动画、3D动画、黏土动画、手绘
**风格化**：漫画书、赛博朋克、8-bit 像素、超现实、极简、绘画风格
**电影感**：历史剧、黑色电影、奇幻、惊悚片、纪录片、艺术片

## 应避免的内容（LTX 特定）

| 避免 | 原因 |
|------|------|
| 内在情感状态（"sad", "confused"） | 使用视觉线索：眼泪、耷拉的姿势、皱眉 |
| 可读文字和标志 | 不可靠渲染 |
| 复杂物理（爆炸、飞溅） | 导致伪影；简单运动没问题 |
| 过载场景 | 许多角色/动作降低连贯性 |
| 冲突的光照描述 | 选择一个设置，坚持 |
| 从复杂开始 | 逐步构建：先简单提示，再添加层 |
| 超过约80词的提示 | LTX-2 超过后质量下降。选择最重要的5-6个元素。 |

## LTX 技术说明

- **时长**：每次生成约5-8秒
- **音频**：自动生成；描述你想听到的内容
- **约30%的输出有伪影** — 用不同种子重新运行
- **无法渲染可读文字** — 不要包含标志或标题
- **帧数必须满足** `(n-1) % 8 == 0`：有效帧数为 25, 49, 73, 97, 121, 161, 193

## 示例

```
A wide establishing shot captures a misty morning harbor.
Weathered fishing boats bob gently, their paint peeling in
patches of red and blue. A grey-haired fisherman in a dark
wool peacoat steps onto the dock, carrying a heavy net over
one shoulder. He pauses, looks out at the fog bank, then
walks toward the nearest boat with steady, deliberate steps.
The camera tracks alongside him at waist height, slowly
pushing in as he reaches the boat and tosses the net aboard.
Soft overcast light with a warm break in the clouds near
the horizon. Ambient sound of water lapping, rope creaking,
and distant foghorn.
```
