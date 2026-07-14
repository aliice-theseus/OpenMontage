---
name: scripts
description: 为 HeyGen AI 虚拟角色视频编写有效脚本
---

# 为 HeyGen 视频编写脚本

AI 虚拟角色视频的脚本与真人演示者的脚本有不同的要求。本指南涵盖编写自然流畅且渲染效果好的脚本的最佳实践。

## 脚本基础

### 语速和时长

正常速度（1.0倍速）下，典型语音约为每分钟 **150 字**。将此作为规划脚本长度的粗略估算。

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

**保持句子简短。** AI 声音处理较短的句子更自然。

| 指南 | 示例 |
|-----------|---------|
| **好**：每句 10-20 字 | "Our platform helps teams collaborate. It syncs in real-time across all devices." |
| **避免**：30 字以上的冗长句子 | "Our platform helps teams collaborate more effectively by providing real-time synchronization across all devices while also offering offline support and automatic conflict resolution." |

### 标点影响表达

| 标点 | 效果 |
|-------------|--------|
| 句号 `.` | 完整停顿，自然暂停 |
| 逗号 `,` | 短暂停顿 |
| 问号 `?` | 升调 |
| 感叹号 `!` | 强调（谨慎使用） |
| 省略号 `...` | 声音逐渐消失，轻微暂停 |

## 使用暂停标签添加暂停

使用 SSML 风格的 `<break>` 标签进行精确暂停控制：

```
<break time="Xs"/>
```

其中 `X` 是秒数（例如 `0.5s`、`1s`、`1.5s`、`2s`）。

### 格式化规则

| 规则 | 正确 | 错误 |
|------|---------|-----------|
| 标签前有空格 | `word <break time="1s"/>` | `word<break time="1s"/>` |
| 标签后有空格 | `<break time="1s"/> word` | `<break time="1s"/>word` |
| 使用带"s"的秒数 | `<break time="1.5s"/>` | `<break time="1500ms"/>` |
| 自闭合标签 | `<break time="1s"/>` | `<break time="1s"></break>` |

### 何时使用暂停

| 场景 | 推荐暂停 | 示例 |
|-----------|-------------------|---------|
| 问候之后 | 0.5-1秒 | `Hello! <break time="0.5s"/> Welcome to...` |
| 章节之间 | 1-1.5秒 | `...that's feature one. <break time="1.5s"/> Now let's look at...` |
| 要点之前 | 0.5秒 | `The most important thing is <break time="0.5s"/> consistency.` |
| 戏剧效果 | 1.5-2秒 | `And the winner is... <break time="2s"/> you!` |
| 问题之后 | 1秒 | `Sound good? <break time="1s"/> Let's get started.` |
| 列表项 | 0.5秒 | `First, speed. <break time="0.5s"/> Second, reliability.` |

### 暂停时长指南

| 时长 | 感觉 | 用途 |
|----------|------|---------|
| 0.3-0.5秒 | 短暂呼吸 | 从句之间，轻微强调 |
| 0.5-1秒 | 自然暂停 | 句子分隔，过渡 |
| 1-1.5秒 | 刻意暂停 | 段落变化，要点铺垫 |
| 1.5-2秒 | 戏剧性 | 揭示、重要公告 |
| 2秒以上 | 长暂停 | 谨慎使用，可能感觉不自然 |

### 示例

```typescript
// 段落过渡
const script = `
Welcome to our product overview. <break time="1s"/>

Today I'll cover three key features. <break time="0.5s"/>
First, let's look at the dashboard. <break time="1.5s"/>

As you can see, it's designed for simplicity. <break time="0.5s"/>
Every action is just one click away.
`;

// 营造悬念
const announcement = `
We've been working on something special. <break time="1s"/>
After months of development... <break time="1.5s"/>
I'm excited to announce <break time="0.5s"/> our new AI assistant.
`;

// 有节奏的列表
const features = `
Our platform offers three core benefits. <break time="0.5s"/>
Speed. <break time="0.5s"/>
Reliability. <break time="0.5s"/>
And simplicity. <break time="1s"/>
Let me show you each one.
`;
```

### 连续暂停

多个连续的暂停标签会被合并：

```typescript
// 这两个暂停：
"Hello <break time=\"1s\"/> <break time=\"0.5s\"/> world"

// 会被视为一个 1.5 秒的暂停
```

## 脚本结构模板

### 产品演示（60秒，约150字）

```typescript
const productDemo = `
Hi, I'm [Name], and I'm excited to show you [Product]. <break time="1s"/>

[Product] helps you [main benefit] in just [timeframe]. <break time="0.5s"/>

Here's how it works. <break time="1s"/>

First, [step 1]. <break time="0.5s"/>
Then, [step 2]. <break time="0.5s"/>
And finally, [step 3]. <break time="1s"/>

What used to take [old time] now takes [new time]. <break time="0.5s"/>

Ready to get started? <break time="0.5s"/>
Visit [website] today.
`;
```

### 教程介绍（90秒，约225字）

```typescript
const tutorial = `
Welcome to this tutorial on [topic]. <break time="0.5s"/>
I'm [Name], and I'll guide you through everything you need to know. <break time="1s"/>

By the end of this video, you'll be able to [outcome 1], [outcome 2], and [outcome 3]. <break time="1s"/>

Let's start with the basics. <break time="1.5s"/>

[Section 1 content - 2-3 sentences] <break time="1s"/>

Now that you understand [concept], let's move on to [next topic]. <break time="1.5s"/>

[Section 2 content - 2-3 sentences] <break time="1s"/>

And finally, let's cover [last topic]. <break time="1.5s"/>

[Section 3 content - 2-3 sentences] <break time="1s"/>

That's everything you need to get started. <break time="0.5s"/>
If you have questions, leave a comment below. <break time="0.5s"/>
Thanks for watching!
`;
```

### 公告（30秒，约75字）

```typescript
const announcement = `
Big news! <break time="0.5s"/>

We're thrilled to announce [announcement]. <break time="1s"/>

This means [benefit 1] and [benefit 2] for all our users. <break time="0.5s"/>

Starting [date], you'll be able to [new capability]. <break time="1s"/>

Head to [location] to learn more. <break time="0.5s"/>
We can't wait to hear what you think!
`;
```

## AI 声音的写作技巧

### 应该做

- **写得口语化** - 大声朗读检查流畅度
- **使用缩写** - 用"We're"不用"We are"，用"It's"不用"It is"
- **拆分长句** - 在自然停顿点断开
- **拼写缩写** - "API"可能听起来像"啊屁爱"
- **添加暂停强调** - 引导听众注意力
- **清晰结束段落** - 不要半途而废

### 避免

- **无上下文的行话** - 解释技术术语
- **长插入语** - 移至单独句子
- **模棱两可的发音** - "read（读，现在时）"vs"read（读，过去时）"
- **过多感叹号** - 每个脚本一个通常就够了
- **冗长句子** - 拆分为易消化的片段
- **密集信息** - 用暂停隔开事实

### 发音提示

对于可能发音错误的词，使用注音或添加提示：

```typescript
// 技术术语
const script1 = "Our API (A-P-I) handles authentication...";

// 模棱两可的词
const script2 = "I read (red) the documentation yesterday...";

// 品牌名称
const script3 = "Welcome to HeyGen (hey-jen)...";
```

## 多场景脚本

在场景之间拆分脚本时（不同背景或虚拟角色）：

```typescript
const multiSceneVideo = {
  video_inputs: [
    {
      // 场景 1：介绍
      character: { type: "avatar", avatar_id: "josh_lite3_20230714", avatar_style: "normal" },
      voice: {
        type: "text",
        input_text: "Welcome to our quarterly update. <break time=\"1s\"/> I'm Josh, and I'll walk you through the highlights.",
        voice_id: "voice_id_here",
      },
      background: { type: "color", value: "#1a1a2e" },
    },
    {
      // 场景 2：主要内容（不同背景）
      character: { type: "avatar", avatar_id: "josh_lite3_20230714", avatar_style: "normal" },
      voice: {
        type: "text",
        input_text: "Let's start with revenue. <break time=\"0.5s\"/> We grew 25 percent quarter over quarter. <break time=\"1s\"/> Here's what drove that growth.",
        voice_id: "voice_id_here",
      },
      background: { type: "image", url: "https://..." },
    },
    // ... 更多场景
  ],
};
```

### 场景过渡技巧

- 每场景以完整思想结束
- 新场景以简短上下文开始
- 场景间保持一致的基调
- 在场景开头使用暂停让视觉效果有时间呈现

## 测试您的脚本

在生成完整视频之前：

1. **大声朗读** - 计时，检查措辞是否别扭
2. **计算字数** - 验证预期时长
3. **检查暂停标签** - 确保正确的空格和语法
4. **预览短片** - 如不确定发音，生成一个10秒测试

```typescript
// 先测试小部分
const testScript = script.split('.').slice(0, 2).join('.') + '.';
const testVideoId = await generateVideo({
  video_inputs: [{
    character: { type: "avatar", avatar_id: avatarId, avatar_style: "normal" },
    voice: { type: "text", input_text: testScript, voice_id: voiceId },
  }],
  dimension: { width: 1280, height: 720 }, // 测试用较低分辨率
});
```

## 语速调整

在语音配置中调整表达速度：

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
| 0.8-0.9 | 较慢，刻意 | 复杂主题，年长观众 |
| 1.0 | 正常 | 一般使用 |
| 1.1-1.2 | 稍快 | 有活力内容，年轻观众 |
| 1.3+ | 快速 | 谨慎使用，可能降低清晰度 |

详见 [voices.md](voices.md) 了解完整语音配置选项。
