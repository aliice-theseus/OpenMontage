# HunyuanVideo 1.5 — 提示指南

> 来源：[Tencent 提示手册](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/assets/HunyuanVideo_1_5_Prompt_Handbook_EN.md)
> 通用词汇表请参见：`skills/creative/video-gen-prompting.md`

**字数：** Hunyuan 1.5 在 80–200 词表现良好；不奖励 400 词的作文。

## HunyuanVideo 提示公式

### 文生视频
```
主体 + 动作 + 场景 + [镜头类型] + [相机运动] + [光照] + [风格] + [氛围]
```

### 图生视频
```
主体运动动态 + 场景运动动态 + [相机运动]
```

对于 I2V，重点描述**运动**，而非外观（图像提供了外观）。

## HunyuanVideo 特有优势

### 光照即氛围
腾讯强调：**"光是氛围的灵魂。"**

从多个维度描述光照：
- **风格**：柔和、硬朗、霓虹、环境
- **方向**：侧光、逆光、顶光、底光
- **品质**：强聚光、漫射光晕
- **阴影**：长戏剧性阴影、柔和阴影边缘
- **色温**：黄金时刻温暖、冷色日光蓝
- **反射**：湿面反射、金属闪光

### 相机运动库

| 运动 | 类型 | HunyuanVideo 提示 |
|------|------|-------------------|
| 升降/升降架 | 平移（垂直） | "camera rises vertically" |
| 横移/跟拍 | 平移（水平） | "camera tracks left alongside subject" |
| 推轨进 | 平移（推） | "camera pushes forward toward subject" |
| 推轨出 | 平移（拉） | "camera pulls back from subject" |
| 摇摄 | 旋转（偏航） | "camera pans right across the scene" |
| 俯仰 | 旋转（俯仰） | "camera tilts upward to follow the rocket" |
| 滚动 | 旋转（Z轴/斜角） | "camera rolls clockwise into a Dutch tilt" |
| 环绕 | 圆形 | "camera orbits around subject" |
| 跟随 | 锁定 | "camera follows subject from behind" |
| 变焦 | 纯镜头（焦距） | "camera slowly zooms in on the figure" |
| 焦距切换 | 纯镜头（焦平面，快速） | "rack focus from the foreground bottle to the figure in the background" |
| 焦距推移 | 纯镜头（焦平面，渐进） | "camera shifts focus from foreground X to background Y" |
| 静态 | 固定 | "static camera, no movement" |

### 动态景深镜头的开始和结束焦平面标签

Hunyuan 在焦点变化镜头的两个端点都被说明时受益。说明焦点从哪里开始和落位到哪里 — 不要只留一个隐含的。

示例："shallow DoF; focus on the foreground bottle at start; focus pulls to the figure in the background by end."

没有两个端点，Hunyuan 常默认为深焦或停留在错误的平面。

### 风格关键词

**照片级真实感/电影感**：
- Film noir, hard sci-fi, cinematic photography
- Period drama, war documentary, nature documentary

**动画/插图**：
- 2D animation, Japanese anime
- Watercolor painting, Chinese ink wash
- Low-poly 3D, pixel art

## I2V 最佳实践

使用图生视频时，输入图像定义外观。你的提示应仅描述：
1. 主体如何运动
2. 环境如何变化
3. 相机运动

**好的 I2V 提示：** "The woman's hair blows in the wind as she turns to face the camera. Leaves scatter across the path. Camera slowly dollies in."

**差的 I2V 提示：** "A beautiful woman in a red dress standing in a forest" — 这重复了图像已展示的内容。

### 按时间顺序排列运动

按时间顺序描述运动；如果有多个运动，分开它们（"first the camera pans right, then tilts upward"）。Hunyuan 按照提示中出现的顺序执行运动 — 将两个运动捆绑到一个从句中会导致其中一个被丢弃或混合。

## 示例（T2V）

```
A young woman in a flowing white dress walks barefoot along
a deserted beach at golden hour. She trails her hand through
the shallow surf, leaving ripples. Her hair catches the warm
side-light from the setting sun. Medium tracking shot, camera
follows alongside at knee height. Soft golden lighting with
long shadows stretching toward the camera. Cinematic
photography style, shallow depth of field. Peaceful,
contemplative atmosphere.
```

## 示例（I2V）

```
The cat stretches lazily, then leaps from the windowsill
to the floor. Dust motes scatter in the shaft of light.
Camera remains static, slight rack focus from window to
landing spot.
```
