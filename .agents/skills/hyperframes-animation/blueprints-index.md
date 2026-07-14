# 蓝图（经过验证的形态）

> 蓝图层的入口点。阅读此文件以找到帧的形态；阅读 `blueprints/<id>.md` 以实例化它。步骤 4 方法（重现/适配/组合，每帧写什么）在 `visual-design.md` 中 — 此文件是菜单 + 选择器。

**蓝图**是与产品无关的、**时间编码的镜头模板** — `场景 N（a–b 秒）：…` 带 `[slots]` 和一个命名的**标志性动作** — 从 50 个黄金产品发布剪辑（加上 13 个反向翻译为相同简报格式的 hyperframes-animation 蓝图）逆向工程而来。它编码了整个镜头的完整时长 — 揭示节奏与台词同步，而非在 t=0 倾倒 — 因此实例化一个在结构上保持内容持续到达而非冻结。完整模板位于 `blueprints/<id>.md`。**步骤 4（视觉设计）每帧实例化一个蓝图**（当没有合适时从动词语汇组合）。

## 15 个蓝图

<blueprints>
<blueprint id="kinetic-type-beats" roles="Hook, Problem, Product_Intro, Benefits, CTA, Brand_Outro" duration="3.4–12s">
平面、居中、粗体排版镜头，其中**运动就是词语的变化** — 固定行通过硬切原位交换标记，或全屏节拍上的陈述构建（每个自己的动作）到弹簧弹出回报。主力（6 个角色）。每当文字承载镜头且无布景、表面或点击时使用。
</blueprint>
<blueprint id="typewriter-reveal" roles="Hook, Brand_Outro" duration="3.6–7s">
实时文本光标**像人一样输入（和编辑）一行**，然后折叠它并弹出品牌回报，或在持久标记下保持，同时子行输入到最终 CTA。当"有人在输入这个"应是驱动力时使用 — 一个可关联的输入痛苦→品牌，或站立的 logo + 输入的 CTA 轨道。
</blueprint>
<blueprint id="spatial-pan-stations" roles="Hook, Problem" duration="7–10s">
预先放置的标记**站点在一个超大 canvas 上，由单个虚拟摄像机遍历** — 重复的横向/对角平移，居中每个站点并揭示标注，最后着陆保持。用于里程碑时间线平移到"我们"，或连接痛苦站点网络结束于缠结结。
</blueprint>
<blueprint id="constellation-hub" roles="Hook, Social_Proof" duration="5–6s">
带图标的**节点弹簧进入围绕中心的环**，然后解析到核心 — 摄像机推进（景深塌缩到其上）或带卫星轨道运行的保持中心标记。用于"它连接一切/一个中心"或"位于你技术栈中心。"
</blueprint>
<blueprint id="grid-card-assemble" roles="Key_Feature, Benefits, Social_Proof" duration="3.0–10.5s">
N 个项目（方块/卡片/logo/列表行）**在错开级联中自组装**成网格或垂直列表并保持；可选摄像机拉远-ZOOM 揭示更大整体内的阵列。用于一次列举广度 — 功能网格、累积的利益列表或 logo 墙。
</blueprint>
<blueprint id="logo-assemble-lockup" roles="Product_Intro, CTA, Brand_Outro" duration="4.6–11s">
品牌标记/wordmark**由部件自建**（元素组装/轨道运行、字母级联、轮廓绘制、或摄像机穿过负空间推进）并解析为居中的组合，可选扩展到 URL/CTA。用于无词高级品牌开场，或引导到最终请求的 logo 构建。
</blueprint>
<blueprint id="cursor-ui-demo" roles="Product_Intro, Key_Feature" duration="4.0–9.3s">
可见的自定义**光标驱动重建的应用 UI**，通过点击/悬停/拖拽使屏幕状态逐镜头变化，同时摄像机追逐每次交互。用于首次光标引导的表面查看（Product_Intro）或一个端到端演示到操作按钮的工作流（Key_Feature）。
</blueprint>
<blueprint id="device-surface-showcase" roles="Key_Feature" duration="7.8–9.6s">
**设备模拟或浮动窗口作为主角**，其屏幕经历真实流程循环，由覆盖从静态保持到连续 3D 推进范围的摄像机呈现。角色窄（仅 Key_Feature）但机制丰富（静态巡览·浮动窗口推进滚动·3D 手演示）。
</blueprint>
<blueprint id="dataviz-countup" roles="Problem, Product_Intro" duration="6–12s">
数字和图表是主角 — **计数递增环/数字、趋势图、倾斜统计网格** — 由摄像机推进穿过（或滚动经过）它们遍历，着陆在一个主角度量上。当数据承载论证时使用：量化恶化问题，或自信地以"看结果"开场。
</blueprint>
<blueprint id="titlecard-reveal" roles="Benefits, Social_Proof" duration="3–5s">
平静的**呼吸/着陆节拍** — 一张干净的标题或单一品牌/证明卡片，以恰好一个克制动作揭示（上滑交叉淡入淡出、或擦拭揭示），然后静止保持。低运动是交付物，而非缺陷。用于两行价值标题，或繁忙开场擦拭到干净组合 +"受 N+ 团队喜爱"统计。
</blueprint>
<blueprint id="comparison-split" roles="Key_Feature" duration="4–6s">
两个同等权重的配对项目从对侧进入，带**镜像的 3D"书本打开"倾斜**并排保持，然后内侧边缘胶囊徽章弹簧弹出以标点。用于 A/B 或"X + Y 一起" — 两个同时权衡的互补能力（not >2 items, not sequential steps）。
</blueprint>
<blueprint id="overwhelm-surround" roles="Problem" duration="6–9s">
通过累积压倒 — 可识别的表面组装，密度标记图标散入，中心一个**变形为观看者自己的头像**，然后元素从所有方向聚拢（被包围，非被放大）。当痛点是"你被埋在工具中"时使用，结束于幽闭恐惧的人群。
</blueprint>
<blueprint id="ticker-takeover" roles="Hook, Brand_Outro" duration="5–7s">
输入引导 + 重音词循环通过选项，然后主角**从屏幕外猛冲进来并物理推开文本** — 碰撞而非淡入淡出 — 单独稳定。当"可以是很多东西"的构建应被暴力替换为"就是这个"时使用。
</blueprint>
<blueprint id="video-text-pivot" roles="Product_Intro, Key_Feature" duration="6–8s">
产品视频保持中心并呼吸，然后**滑向一侧将重量转移给主角统计数字**，然后两者清除，动感文本输入空出的中心，由渐变胶囊封口。用于"看功能→看影响"，其中视频必须保持可见（滑动，从不切断）。
</blueprint>
<blueprint id="cta-morph-press" roles="CTA" duration="4–6s">
休息品牌标记**在同一中心凝聚成更亮的 CTA**，然后光标到达并着陆瞄准人类的点击，带反馈。用于专注"点击这里"的签退，将眼睛从身份引导到动作 — 无空间设置，无多步骤 UI。
</blueprint>
</blueprints>

## 角色→蓝图菜单

一个**软**菜单：故事真相优先。故事设计在产品的节拍本身呼唤那种形态时 — 它建议经过验证的形态，它从不决定哪些节拍存在。每个角色有 2-4 个选项；如果没有适合节拍，自由组合（菜单不是清单）。每行是应让你使用该蓝图的**触发器**。

（角色到蓝图映射关系与原文一致，已全部中文化。）

## 选择指南

1. 在上方菜单中找到帧的**角色**；选择**形态适合此节拍**的蓝图（故事可能已命名候选 id — 确认或覆盖）。如果两个适合，偏好运动更接近你计划的那个。
2. 打开 `blueprints/<id>.md` — 阅读其时间编码模板、`[slots]` 和命名的**标志性动作**。
3. 选择姿态 — **重现**（槽位干净映射）、**适配**（结构适合，内容/表面不同；保留标志性动作）或**组合**（无适合 → 从动词语汇构建）。
4. 如果菜单中无适合节拍，从 `motion-language.md` 的动词语汇**组合** — 仍然将揭示节奏同步到 VO 贯穿镜头。不要强行使用错误的蓝图。

## 运动覆盖

黄金语汇中的每个重复动作由本技能的本地 `rules/` 支持 — 包括五个新增到语料库的：`depth-of-field-blur`、`motion-blur-streak`、`depth-scatter-assemble`、`spring-pop-entrance`（规范入场弹出，与点击/按下的 `press-release-spring` 不同）和 `ambient-glow-bloom`。每个蓝图的 `规则映射` 引用真实规则。

一个真正的范围外特例仍然存在：`device-surface-showcase` 的 **3D 手势输入 + WebGL 绽放/传送门**需要 R3F/Three.js + WebGL — 比规则库更重的能力。谨慎使用，或选择更简单的 `device-surface-showcase` 变体。
