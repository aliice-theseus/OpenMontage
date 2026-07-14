---
name: prompt-examples
description: Video Agent 的完整生产级提示词示例和即用模板
---

# Video Agent 提示词示例

## 完整示例：从需求到生产级提示词

### 输入需求

```
话题：SaaS 创业公司的月度公司报告
关键数据：141M 美元 ARR（从 54M 美元增长），185 万注册（+28%），300 万付费视频/月
客户故事：创作者构建了 AI 角色，250 万粉丝，每个视频 20 分钟
挑战：自然流量波动，上周 -16%
时长：约 90 秒
基调：CEO 自信，数据支撑
```

### 输出提示词

```
FORMAT: 彭博社风格公司报告。90秒。快节奏，数据密集。
破纪录的月份。自豪但分析性。

TONE: 自信、直接、数据支撑。亮点用数字重击。
客户故事是情感核心。挑战是诚实的——不粉饰。

AVATAR: 身着简洁黑色圆领T恤的男性，站在现代玻璃墙办公室中，
正值黄金时段。身后墙上显示器显示公司标志，散发柔和蓝光。
右侧显示器显示向上趋势的图表。旁边桌子：笔记本电脑、半杯
白咖啡、散落的便利贴。落地窗透入温暖午后光线，抛光混凝土上
投下长长阴影。极简、专注的创业公司总部。

STYLE — SWISS PULSE (Müller-Brockmann): 网格锁定构图。黑色 (#1a1a1a)、
白色、电蓝色 (#0066FF)、暖琥珀色 (#FF9500) 用于记录。Helvetica Bold
标题，Regular 标签。数字大号。动画计数器从 0 开始计数。
对角线构图用于重音时刻。网格擦除转场。无溶解。

CRITICAL ON-SCREEN TEXT (逐字显示):
- "185万 注册量 — +28% 月环比"
- "$212万 新订阅收入"
- "$5400万 → $1.41亿 ARR"
- "250万 粉丝" 和 "20 分钟/视频"
- 引语："利用技术服务信息，而非让信息被技术干扰。"
- "自然流量：65% 订阅量 — 波动"

MUSIC: 乐观电子乐，带强劲节拍。Tycho 遇上 Bloomberg 开场曲。
在亮点处推进，在客户故事处温暖，在挑战处柔和，在结尾处达到顶峰。

---

SCENE 1 — A-ROLL (8s)
[Avatar center-frame, energetic, leaning slightly forward]
VOICEOVER: "January was a record month. New highs across acquisition, revenue,
and product velocity. Here's the full picture."
Lower-third SLIDES in: "COMPANY NAME | JANUARY 2026" white on blue bar.
Grid wipe.

SCENE 2 — FULL SCREEN B-ROLL (12s)
[NO AVATAR — motion graphic only]
VOICEOVER: "One-point-eight-five million signups — twenty-eight percent month
over month. Two-point-one-two million in new subscription revenue. Both all-time
highs."
LAYER 1: Dark #1a1a1a background with thin grid lines pulsing at 8% opacity.
LAYER 2: "1.85M" SLAMS in from left, white Bold 140pt. "SIGNUPS" types on
          in electric blue 32pt uppercase. "+28% MoM" appears in amber.
LAYER 3: Three stat cards CASCADE from top-right, staggered 0.3s:
          "$2.12M New Revenue" — "$3.4M Business ARR" — "$3M Pro ARR."
          Each number COUNTS UP from 0.
LAYER 4: Bottom ticker scrolls: "Non-brand search +36% • Brand impressions 9.2M
          • Weekly subs +20.5%"
LAYER 5: Grid lines RIPPLE outward on "1.85M" slam. Diagonal amber bar behind
          stat cards.
Hard cut.

SCENE 3 — FULL SCREEN B-ROLL (12s)
[NO AVATAR — motion graphic only]
VOICEOVER: "Zoom out. Twelve months ago — fifty-four million ARR. Today —
one hundred forty-one million. Nearly three X in a single year."
LAYER 1: Dark background, subtle grid scrolling upward.
LAYER 2: Animated line chart DRAWS ITSELF left to right. Y-axis: $50M to $150M.
          Final point "$140.84M" glows amber and pulses.
LAYER 3: Milestone annotations float in at key data points.
LAYER 4: Second smaller chart below — "Paid Videos" 0.91M to 2.97M, same style.
LAYER 5: Thin grid lines converge toward final data point. Scan line sweeps.
Grid wipe.

SCENE 4 — A-ROLL (8s)
[Avatar center-frame, warm tone, genuine smile]
VOICEOVER: "But the numbers only tell half the story. The other half is the
people building on the platform."
Lower-third: "Customer Spotlight"

SCENE 5 — FULL SCREEN B-ROLL (12s)
[NO AVATAR — warm palette]
VOICEOVER: "An AI character built entirely on the platform. Twenty minutes
per video. Two-point-five million Instagram followers. The creator's principle:
use technology to serve the message, not distract from it."
LAYER 1: Dark background with warm amber grid lines at low opacity.
LAYER 2: "CHARACTER NAME" in large white, center-top, 80pt.
LAYER 3: Stats cascade from right: "2.5M Followers" COUNTS UP in amber —
          "20 min/video" — "7x Faster." Each a glowing node.
LAYER 4: Quote card SLIDES UP: "Use technology to serve the message, not
          distract from it." Types on word by word.
LAYER 5: Warm light bloom. Grid lines soften into curved arcs.
Grid wipe.

SCENE 6 — A-ROLL (10s)
[Avatar center-frame, serious/candid]
VOICEOVER: "Now the honest part. Organic drives sixty-five percent of
subscriptions and it's volatile. Non-brand traffic dropped sixteen percent
last week. We've rebuilt attribution and we're investing in SEO."
Lower-third: "Challenges"

SCENE 7 — A-ROLL (7s)
[Avatar center-frame, energy lifts, direct eye contact]
VOICEOVER: "Fifty-four million to one-forty-one in twelve months. Three million
paid videos a month. January set the bar — now we raise it."
End card: Logo centered, blue glow fade-in. Grid lines converge. Music peaks.

---

NARRATION STYLE: CEO energy — conviction backed by data. Fast on highlights.
Warm on customer stories. Candid on challenges. Close with forward momentum.
```

## 即用模板

### 科技新闻简报
```
FORMAT: 75秒高能科技简报。想象：Bloomberg 遇上 Vice。

AVATAR: [科技休闲装扮的主持人，在多屏幕工作站前。
描述服装、显示器内容、桌上物品、灯光。]

STYLE — DECONSTRUCTED (Brody): 深灰色 #1a1a1a，锈橙色 #D4501E。
倾斜重叠的文字。粗糙纹理。猛切转场。

CRITICAL ON-SCREEN TEXT:
- [列出必须出现的每个统计、引用、账号]

SCENE 1 — A-ROLL (8s): 带能量钩子。陈述正在发生什么。
SCENE 2 — B-ROLL (12s): 第一个故事，分层视觉（L1-L5）。
SCENE 3 — A-ROLL + OVERLAY (10s): 第二个故事，分屏。
SCENE 4 — B-ROLL (10s): 第三个故事或戏剧性数据点。
SCENE 5 — A-ROLL (8s): 总结和展望。
```

### 产品对比
```
FORMAT: 60秒对比。[产品A] vs [产品B]。数据驱动。

AVATAR: [评测工作室中的主持人。桌上两款产品都可见。]

STYLE — DIGITAL GRID (Crouwel): 深黑 #0a0a0a，青色 #00D4FF 和琥珀色 #FFB800。
双色编码：青色 = 产品A，琥珀色 = 产品B。等宽字体。

CRITICAL ON-SCREEN TEXT:
- [每个产品的关键统计]
- [价格、功能、差异点]

使用分屏 B-roll：左侧产品A，右侧产品B。
```

### 战略演示
```
FORMAT: 90秒战略简报。Bloomberg 遇上董事会会议。

AVATAR: [穿西装外套内搭T恤的高管。带白板框架的会议室。]

STYLE — SWISS PULSE (Müller-Brockmann): 黑/白 + 蓝色 #0066FF。
网格锁定。Helvetica。动画计数器。网格擦除转场。

CRITICAL ON-SCREEN TEXT:
- [框架标签、象限标签、关键引用]

视觉化构建框架：绘制坐标轴、标记位置、动画标签。
```

### 社交广告（30秒）
```
FORMAT: 30秒社交广告。最大能量。竖屏9:16。

AVATAR: [创作者风格主持人。环形灯，彩色背景。]

STYLE — CARNIVAL SURGE (Lins): 热粉色、黄色、青色。拼贴分层。
文字巨大且倾斜。五彩纸屑。猛切。

三个场景：钩子（8s）→ 价值主张（12s）→ CTA（10s）。
文字占据每帧的50-80%。数字重击。
```

### 高端报告
```
FORMAT: 120秒投资者级报告。低调权威感。

AVATAR: [量身定制的美利奴毛衣。建筑感空间，柔和的自然光。]

STYLE — VELVET STANDARD (Vignelli): 黑色、白色、金色 #c9a84c。
细体全大写，宽字距。大量留白。
慢速交叉溶解。数字带重量淡入。
```
