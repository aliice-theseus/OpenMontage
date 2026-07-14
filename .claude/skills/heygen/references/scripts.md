---
name: scripts
description: 为 HeyGen AI 头像视频编写有效的脚本
---

# 编写 HeyGen 视频脚本

AI 头像视频的脚本与人类出镜的脚本有不同的要求。本指南涵盖如何编写听起来自然且渲染良好的脚本。

## 脚本基础

### 语速和时长

正常速度（1.0x）下，语速约为每分钟 **150 字**。以此作为规划脚本长度的粗略估算。

| 脚本长度 | 大致时长 |
|---------------|---------------------|
| 75 字 | 30 秒 |
| 150 字 | 1 分钟 |
| 300 字 | 2 分钟 |
| 450 字 | 3 分钟 |
| 750 字 | 5 分钟 |

```typescript
// 从脚本估算视频时长
function estimateDuration(script: string, speed: number = 1.0): number {
  const words = script.split(/\s+/).filter(w => w.length > 0).length;
  const wordsPerMinute = 150 * speed;
  return words / wordsPerMinute * 60; // 秒
}

// 为 Remotion 估算帧数
function estimateFrames(script: string, fps: number = 30, speed: number = 1.0): number {
  const durationSeconds = estimateDuration(script, speed);
  return Math.ceil(durationSeconds * fps);
}
```

### 句子结构

**保持句子简短。** AI 语音处理较短句子更自然。

| 指南 | 示例 |
|-----------|---------|
| **好**: 每句 10-20 字 | "我们的平台帮助团队协作。它可以在所有设备上实时同步。" |
| **避免**: 30 字以上的冗长句子 | "我们的平台通过在所有设备上提供实时同步，同时支持离线功能和自动冲突解决，来帮助团队更有效地协作。" |

### 标点符号影响表达

| 标点 | 效果 |
|-------------|--------|
| 句号 `.` | 完全停顿，自然呼吸 |
| 逗号 `,` | 短暂停顿 |
| 问号 `?` | 升调 |
| 感叹号 `!` | 强调（谨慎使用） |
| 省略号 `...` | 声音渐弱，轻微停顿 |

## 使用 Break 标签添加暂停

使用 SSML 风格的 `<break>` 标签实现精确的暂停控制：

```
<break time="Xs"/>
```

其中 `X` 是秒数（例如 `0.5s`, `1s`, `1.5s`, `2s`）。

### 格式化规则

| 规则 | 正确 | 错误 |
|------|---------|-----------|
| 标签前有空格 | `word <break time="1s"/>` | `word<break time="1s"/>` |
| 标签后有空格 | `<break time="1s"/> word` | `<break time="1s"/>word` |
| 使用带"秒"的秒数 | `<break time="1.5s"/>` | `<break time="1500ms"/>` |
| 自闭合标签 | `<break time="1s"/>` | `<break time="1s"></break>` |

### 何时使用暂停

| 场景 | 推荐暂停 | 示例 |
|-----------|-------------------|---------|
| 问候后 | 0.5-1s | `大家好！<break time="0.5s"/> 欢迎来到...` |
| 章节之间 | 1-1.5s | `...这是第一个功能。<break time="1.5s"/> 现在让我们看看...` |
| 关键点前 | 0.5s | `最重要的是 <break time="0.5s"/> 一致性。` |
| 戏剧效果 | 1.5-2s | `而获胜者是... <break time="2s"/> 你！` |
| 提问后 | 1s | `听起来不错？<break time="1s"/> 让我们开始吧。` |
| 列表项之间 | 0.5s | `第一，速度。<break time="0.5s"/> 第二，可靠性。` |

### 暂停时长指南

| 时长 | 感觉 | 用途 |
|----------|------|---------|
| 0.3-0.5s | 短暂呼吸 | 从句之间，轻微强调 |
| 0.5-1s | 自然停顿 | 句子间隔，过渡 |
| 1-1.5s | 刻意停顿 | 章节变化，关键点铺垫 |
| 1.5-2s | 戏剧性 | 揭晓，重要公告 |
| 2s以上 | 长暂停 | 谨慎使用，可能显得不自然 |

### 示例

```typescript
// 章节过渡
const script = `
欢迎来到我们的产品概述。<break time="1s"/>

今天我将介绍三个关键功能。<break time="0.5s"/>
首先，让我们看看仪表盘。<break time="1.5s"/>

正如你所看到的，它设计得非常简洁。<break time="0.5s"/>
每个操作只需点击一次。
`;

// 制造悬念
const announcement = `
我们一直在开发一些特别的东西。<break time="1s"/>
经过数月的开发... <break time="1.5s"/>
我很高兴地宣布 <break time="0.5s"/> 我们的新 AI 助手。
`;

// 有节奏的列表
const features = `
我们的平台提供三个核心优势。<break time="0.5s"/>
速度。<break time="0.5s"/>
可靠性。<break time="0.5s"/>
以及简洁性。<break time="1s"/>
让我为你逐一展示。
`;
```

### 连续暂停

多个连续暂停会被合并：

```typescript
// 这两个暂停：
"Hello <break time=\"1s\"/> <break time=\"0.5s\"/> world"

// 会被视为一个 1.5 秒的暂停
```

## 脚本结构模板

### 产品演示（60秒，约150字）

```typescript
const productDemo = `
嗨，我是[姓名]，很高兴向你展示[产品]。<break time="1s"/>

[产品]帮助你在[时间范围]内实现[主要好处]。<break time="0.5s"/>

以下是它的工作方式。<break time="1s"/>

首先，[步骤1]。<break time="0.5s"/>
然后，[步骤2]。<break time="0.5s"/>
最后，[步骤3]。<break time="1s"/>

以前需要[旧时间]的事情，现在只需要[新时间]。<break time="0.5s"/>

准备好了吗？<break time="0.5s"/>
今天访问[网站]。
`;
```

### 教程介绍（90秒，约225字）

```typescript
const tutorial = `
欢迎来到关于[主题]的教程。<break time="0.5s"/>
我是[姓名]，将指导你了解你需要知道的一切。<break time="1s"/>

在本视频结束时，你将能够[结果1]、[结果2]和[结果3]。<break time="1s"/>

让我们从基础开始。<break time="1.5s"/>

[第1部分内容 - 2-3句话] <break time="1s"/>

现在你已经理解了[概念]，让我们继续[下一个主题]。<break time="1.5s"/>

[第2部分内容 - 2-3句话] <break time="1s"/>

最后，让我们覆盖[最后一个主题]。<break time="1.5s"/>

[第3部分内容 - 2-3句话] <break time="1s"/>

以上就是你需要入门的所有内容。<break time="0.5s"/>
如有问题，请在下方留言。<break time="0.5s"/>
感谢观看！
`;
```

### 公告（30秒，约75字）

```typescript
const announcement = `
重大消息！<break time="0.5s"/>

我们非常激动地宣布[公告内容]。<break time="1s"/>

这意味着为所有用户带来[好处1]和[好处2]。<break time="0.5s"/>

从[日期]开始，你将能够[新功能]。<break time="1s"/>

前往[位置]了解更多。<break time="0.5s"/>
我们迫不及待想知道你的想法！
`;
```

## AI 语音写作技巧

### 应该做的

- **写得口语化** - 大声朗读检查流畅度
- **使用缩略形式** - "We're" 而不是 "We are"，"It's" 而不是 "It is"
- **拆分长句** - 在自然停顿点分割
- **拼写缩写** - "API" 听起来可能是 "a pee eye"
- **添加暂停进行强调** - 引导听众的注意力
- **清晰地结束段落** - 不要说到一半就消失了

### 避免

- **无上下文的行话** - 解释技术术语
- **长插入语** - 移入单独的句子
- **有歧义的发音** - "read"（现在时）vs "read"（过去时）
- **过多感叹号** - 通常一个脚本一个就够了
- **冗长句子** - 分成可消化的部分
- **密集信息** - 用暂停间隔事实

### 发音提示

对于可能被读错的单词，用拼音拼写或添加提示：

```typescript
// 技术术语
const script1 = "Our API (A-P-I) handles authentication...";

// 有歧义的单词
const script2 = "I read (red) the documentation yesterday...";

// 品牌名称
const script3 = "Welcome to HeyGen (hey-jen)...";
```

## 多场景脚本

当跨场景（不同背景或头像）拆分脚本时：

```typescript
const multiSceneVideo = {
  video_inputs: [
    {
      // 场景 1：介绍
      character: { type: "avatar", avatar_id: "josh_lite3_20230714", avatar_style: "normal" },
      voice: {
        type: "text",
        input_text: "欢迎来到我们的季度更新。<break time=\"1s\"/> 我是 Josh，我将带你了解重点内容。",
        voice_id: "voice_id_here",
      },
      background: { type: "color", value: "#1a1a2e" },
    },
    {
      // 场景 2：主要内容（不同背景）
      character: { type: "avatar", avatar_id: "josh_lite3_20230714", avatar_style: "normal" },
      voice: {
        type: "text",
        input_text: "让我们从收入开始。<break time=\"0.5s\"/> 我们环比增长了 25%。<break time=\"1s\"/> 以下是推动增长的因素。",
        voice_id: "voice_id_here",
      },
      background: { type: "image", url: "https://..." },
    },
    // ... 更多场景
  ],
};
```

### 场景过渡技巧

- 每个场景以完整的思想结束
- 新场景以简短上下文中开始
- 在整个场景中保持一致的基调
- 在场景开头使用暂停让画面有缓冲时间

## 测试你的脚本

在生成完整视频之前：

1. **大声朗读** - 计时，检查措辞是否别扭
2. **统计字数** - 验证预计时长
3. **检查打断标签** - 确保正确的间距和语法
4. **用短视频预览** - 如果不确定发音，生成 10 秒测试

```typescript
// 先测试一小部分
const testScript = script.split('.').slice(0, 2).join('.') + '.';
const testVideoId = await generateVideo({
  video_inputs: [{
    character: { type: "avatar", avatar_id: avatarId, avatar_style: "normal" },
    voice: { type: "text", input_text: testScript, voice_id: voiceId },
  }],
  dimension: { width: 1280, height: 720 }, // 测试使用较低分辨率
});
```

## 语音速度调整

在语音配置中调整语速：

```typescript
voice: {
  type: "text",
  input_text: script,
  voice_id: "voice_id",
  speed: 1.1,  // 稍快（范围：0.5 - 2.0）
}
```

| 速度 | 效果 | 使用场景 |
|-------|--------|----------|
| 0.8-0.9 | 较慢，沉稳 | 复杂话题，年长受众 |
| 1.0 | 正常 | 一般使用 |
| 1.1-1.2 | 稍快 | 充满活力的内容，年轻受众 |
| 1.3以上 | 快 | 谨慎使用，可能降低清晰度 |

参见 [voices.md](voices.md) 获取完整的语音配置选项。
