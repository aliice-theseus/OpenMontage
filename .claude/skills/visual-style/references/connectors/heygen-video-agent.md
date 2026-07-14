# HeyGen 视频代理连接器

将 `visual-style.md` 应用于 HeyGen 视频代理以生成 AI 视频。

## 概述

HeyGen 视频代理接受一个文本提示，其中可以包含视觉风格指令。`style_prompt_full` 字段直接映射到该提示。

## 字段映射

| visual-style.md 字段 | HeyGen 使用方式 |
|----------------------|----------------|
| `style_prompt_full` | 逐字附加到生成提示 |
| `motion.transitions` | 场景过渡指令 |
| `motion.animation_style` | 动画行为 |
| `motion.pacing` | 节奏指导 |
| `typography.caption` | 字幕样式（如启用字幕） |
| `layout.aspect_ratio` | 方向设置（16:9 = 横屏，9:16 = 竖屏） |
| `mood.avoid` | 负面提示/排除指令 |
| `assets.gsep_elements` | 叠加资源（如支持） |
| `x_heygen.orientation` | 显式方向覆盖 |
| `x_heygen.video_id` | 现有 HeyGen 视频的引用 |

## 提示模板

```
Create a video about [TOPIC].

Script:
[USER'S SCRIPT]

Visual style:
[PASTE style_prompt_full HERE]

Additional constraints:
- [ITEMS FROM mood.avoid]

Motion:
- Transitions: [motion.transitions]
- Pacing: [motion.pacing]
- Animation: [motion.animation_style]

Format: [layout.aspect_ratio OR x_heygen.orientation]
```

## 示例：无虚拟形象动态图形

适用于没有虚拟形象的纯动态图形：

```
Create a video about our Q4 results.

Script:
Revenue grew 40% year over year. We shipped 12 new features.
Customer satisfaction hit an all-time high of 94%.

Visual style:
Josef Müller-Brockmann Swiss International Style. Grid-locked layouts
with mathematical precision. Black and white base with ONE accent color
(electric blue #0066FF). Strong diagonal compositions. Helvetica
typography only. Data visualizations are the hero — animated charts,
counters, grids. Every frame snaps to a grid. Transitions are horizontal
grid wipes. No organic shapes. No gradients. No stock photography.
Everything is geometric, systematic, precise.

Additional constraints:
- No avatar
- No b-roll footage
- No stock photography
- Pure motion graphics only

Motion:
- Transitions: horizontal grid wipes, clean hard cuts
- Pacing: Measured, confident, unhurried
- Animation: Elements snap to grid positions, charts animate systematically

Format: landscape (16:9)
```

## 工作流程

1. **加载风格** — 读取 `visual-style.md` 文件
2. **提取关键字段：**
   - `style_prompt_full`（必填）
   - `motion.*` 字段（推荐）
   - `mood.avoid`（推荐）
   - `layout.aspect_ratio` 或 `x_heygen.orientation`
3. **构建提示** — 使用上述模板
4. **调用 HeyGen 视频代理** — 使用 HeyGen MCP 工具或 API
5. **存储引用** — 如需，将视频 ID 保存到 `x_heygen.video_id`

## 提示

- **明确说明你不想要什么** — HeyGen 对负面约束响应良好
- **动态图形模式** — 对抽象风格添加"无虚拟形象。无 B 卷。纯动态图形。"
- **数据可视化** — 对数字密集型内容提及"动画图表、计数器、数据可视化"
- **过渡很重要** — 明确指定过渡风格；默认值可能与你的风格不匹配

## 支持的风格

这些图库风格特别适合 HeyGen 视频代理：

- `mueller-brockmann-swiss.visual-style.md` — 数据驱动，网格锁定
- `neville-brody-industrial.visual-style.md` — 大胆排版，工业风格
- `saul-bass-cinematic.visual-style.md` — 电影片头，大胆形状
- `game-boy-color.visual-style.md` — 像素艺术，复古游戏
- `heygen-ai-video.visual-style.md` — 现代 AI/SaaS 美学
