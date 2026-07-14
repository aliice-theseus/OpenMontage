# HeyGen Video Agent 连接器

将 `visual-style.md` 应用于 HeyGen Video Agent，用于 AI 生成的视频。

## 概述

HeyGen Video Agent 接受可包含视觉风格指令的文本提示。`style_prompt_full` 字段直接映射到此。

## 字段映射

| visual-style.md 字段 | HeyGen 使用方式 |
|-----------------------|--------------|
| `style_prompt_full` | 逐字追加到生成提示中 |
| `motion.transitions` | 场景过渡指令 |
| `motion.animation_style` | 动画行为 |
| `motion.pacing` | 时间指导 |
| `typography.caption` | 字幕样式（如已启用字幕）|
| `layout.aspect_ratio` | 方向设置（16:9 = 横向，9:16 = 竖向）|
| `mood.avoid` | 反向提示 / 排除指令 |
| `assets.gsep_elements` | 覆盖层资产（如支持）|
| `x_heygen.orientation` | 显式的方向覆盖 |
| `x_heygen.video_id` | 对现有 HeyGen 视频的引用 |

## 提示模板

```
创建一个关于 [主题] 的视频。

脚本：
[用户的脚本]

视觉风格：
[粘贴 style_prompt_full 此处]

额外约束：
- [来自 mood.avoid 的项目]

动效：
- 过渡：[motion.transitions]
- 节奏：[motion.pacing]
- 动画：[motion.animation_style]

格式：[layout.aspect_ratio 或 x_heygen.orientation]
```

## 示例：无虚拟角色动态图形

对于没有虚拟角色的纯动态图形：

```
创建一个关于我们 Q4 业绩的视频。

脚本：
收入同比增长 40%。我们发布了 12 项新功能。
客户满意度达到历史最高点 94%。

视觉风格：
Josef Müller-Brockmann 瑞士国际风格。网格锁定布局
具有数学精度。黑白基调配一种强调色
（电光蓝 #0066FF）。强烈的对角线构图。仅 Helvetica
排版。数据可视化是主角 — 动画图表、
计数器、网格。每一帧都对齐网格。过渡是水平
网格擦拭。无有机形状。无渐变。无图库摄影。
一切都是几何的、系统的、精确的。

额外约束：
- 无虚拟角色
- 无 B 卷素材
- 无图库摄影
- 纯动态图形

动效：
- 过渡：水平网格擦拭，干净硬切
- 节奏：沉稳、自信、不慌不忙
- 动画：元素对齐到网格位置，图表系统化地动画

格式：横向（16:9）
```

## 工作流

1. **加载风格** — 读取 `visual-style.md` 文件
2. **提取关键字段：**
   - `style_prompt_full`（必填）
   - `motion.*` 字段（推荐）
   - `mood.avoid`（推荐）
   - `layout.aspect_ratio` 或 `x_heygen.orientation`
3. **构建提示** — 使用上方的模板
4. **调用 HeyGen Video Agent** — 使用 HeyGen MCP 工具或 API
5. **存储引用** — 如果需要，将视频 ID 保存到 `x_heygen.video_id`

## 技巧

- **明确说明您不想要的内容** — HeyGen 对负面约束反应良好
- **动态图形模式** — 对于抽象风格，添加"无虚拟角色。无 B 卷。纯动态图形。"
- **数据可视化** — 对于数字密集型内容，提及"动画图表、计数器、数据可视化"
- **过渡很重要** — 明确指定过渡风格；默认可能不匹配您的风格

## 支持的风格

这些图库风格特别适合 HeyGen Video Agent：

- `mueller-brockmann-swiss.visual-style.md` — 数据驱动，网格锁定
- `neville-brody-industrial.visual-style.md` — 大胆排版，工业感
- `saul-bass-cinematic.visual-style.md` — 电影标题，大胆形状
- `game-boy-color.visual-style.md` — 像素艺术，复古游戏
- `heygen-ai-video.visual-style.md` — 现代 AI/SaaS 美学
