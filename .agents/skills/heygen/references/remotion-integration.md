---
name: remotion-integration
description: 在 Remotion 合成中使用 HeyGen 虚拟角色视频
---

# HeyGen + Remotion 集成

本指南涵盖生成 HeyGen 虚拟角色视频并在 Remotion 合成中使用的工作流。

## 快速入门

```typescript
// 1. 获取带默认声音的虚拟角色
const avatar = await getAvatarDetails(avatarId);

// 2. 生成视频（带背景的 MP4——最常见）
const videoId = await generateVideo({
  video_inputs: [{
    character: { type: "avatar", avatar_id: avatar.id, avatar_style: "normal" },
    voice: { type: "text", input_text: script, voice_id: avatar.default_voice_id },
    background: { type: "color", value: "#1a1a2e" },
  }],
  dimension: { width: 1920, height: 1080 },
});

// 3. 轮询完成（10-15+ 分钟）
// 4. 在 Remotion 中使用，并在上方叠加动态图形
```

## 概述

典型工作流：
1. 使用 HeyGen 生成虚拟角色视频
2. 等待完成并获取视频 URL
3. 下载或直接在 Remotion 中使用 URL
4. 与其他元素组合（背景、叠加、动画）

## 选择正确的输出格式

| 您的合成 | 推荐 | 原因 |
|------------------|-------------|-----|
| 虚拟角色作为演示者带叠加 | MP4 + 背景 | 更简单，叠加在上方 |
| Loom 风格（虚拟角色叠加在屏幕录制上） | WebM + `closeUp`，在 Remotion 中遮罩 | 需要透明度，在 CSS 中应用圆形遮罩 |
| 虚拟角色叠加在其他视频/内容上 | WebM（透明） | 需要看到后面的内容 |
| 全屏虚拟角色 | MP4 + 背景 | 标准方法 |

**大多数情况下使用带背景的 MP4。** 当您需要看到虚拟角色*后面*的内容时使用 WebM。

**注意：** WebM 仅支持 `normal` 和 `closeUp` 样式。对于圆形取景，在 Remotion 中使用 CSS `border-radius: 50%`。

## 推荐：并行开发工作流

HeyGen 视频生成需要 **10-15+ 分钟**。不要等待——并行工作：

1. **启动 HeyGen 生成** - 保存 `video_id` 到文件，立即退出
2. **构建 Remotion 合成** - 使用占位符或虚拟角色的 `preview_video_url`（短循环）
3. **定期检查 HeyGen 状态** 或在构建完成后检查
4. **将占位符替换为** 真实视频 URL（一旦准备好）

**从脚本估算时长**：语速约 150 字/分钟，所以 `wordCount / 150 * 60 * fps` 给出大致帧数。

**合成技巧**：设计组件无论有无虚拟角色视频都能工作，以便动态图形可独立测试。

## 尺寸对齐

**关键：** 将 HeyGen 输出尺寸与您的 Remotion 合成匹配。

### 常用尺寸预设

```typescript
// HeyGen 和 Remotion 共享的尺寸常量
const DIMENSIONS = {
  landscape_1080p: { width: 1920, height: 1080 },
  landscape_720p: { width: 1280, height: 720 },
  portrait_1080p: { width: 1080, height: 1920 },
  portrait_720p: { width: 720, height: 1280 },
  square_1080p: { width: 1080, height: 1080 },
  square_720p: { width: 720, height: 720 },
} as const;

type DimensionPreset = keyof typeof DIMENSIONS;
```

### HeyGen 视频生成

```typescript
// 使用特定尺寸生成 HeyGen 视频
async function generateHeyGenVideo(
  script: string,
  avatarId: string,
  voiceId: string,
  preset: DimensionPreset
): Promise<string> {
  const dimension = DIMENSIONS[preset];

  const response = await fetch("https://api.heygen.com/v2/video/generate", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      video_inputs: [
        {
          character: {
            type: "avatar",
            avatar_id: avatarId,
            avatar_style: "normal",
          },
          voice: {
            type: "text",
            input_text: script,
            voice_id: voiceId,
          },
          background: {
            type: "color",
            value: "#00FF00", // 用于合成的绿幕
          },
        },
      ],
      dimension,
    }),
  });

  const { data } = await response.json();
  return data.video_id;
}
```

### Remotion 合成设置

```tsx
// remotion/src/Root.tsx
import { Composition } from "remotion";
import { AvatarComposition } from "./AvatarComposition";

const DIMENSIONS = {
  landscape_1080p: { width: 1920, height: 1080 },
  // ... 同上
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="AvatarVideo"
        component={AvatarComposition}
        durationInFrames={300} // 将动态设置
        fps={30}
        width={DIMENSIONS.landscape_1080p.width}
        height={DIMENSIONS.landscape_1080p.height}
        defaultProps={{
          avatarVideoUrl: "",
        }}
      />
    </>
  );
};
```

## 为 Remotion 生成虚拟角色视频

### 标准：带背景的 MP4

大多数 Remotion 合成使用带背景的 MP4 效果最好。叠加和动态图形放在上方：

```typescript
async function generateAvatarForRemotion(
  script: string,
  avatarId: string,
  voiceId: string,
  options: {
    style?: "normal" | "closeUp" | "circle";
    backgroundColor?: string;
  } = {}
): Promise<string> {
  const { style = "normal", backgroundColor = "#1a1a2e" } = options;

  const response = await fetch("https://api.heygen.com/v2/video/generate", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      video_inputs: [{
        character: {
          type: "avatar",
          avatar_id: avatarId,
          avatar_style: style,
        },
        voice: {
          type: "text",
          input_text: script,
          voice_id: voiceId,
        },
        background: {
          type: "color",
          value: backgroundColor,
        },
      }],
      dimension: { width: 1920, height: 1080 },
    }),
  });

  const { data } = await response.json();
  return data.video_id;
}
```

### 透明背景 (WebM)

仅当您需要看到虚拟角色*后面*的内容时才使用（例如，虚拟角色叠加在屏幕录制上）：

```typescript
// 使用 /v1/video.webm 端点实现透明背景
// 注意：结构与 /v2/video/generate 不同
const response = await fetch("https://api.heygen.com/v1/video.webm", {
  method: "POST",
  headers: {
    "X-Api-Key": process.env.HEYGEN_API_KEY!,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    avatar_pose_id: avatarPoseId,  // 必需：虚拟角色姿势 ID
    avatar_style: "normal",        // 必需：仅 "normal" 或 "closeUp"
    input_text: script,            // 必需（与 voice_id 一起）
    voice_id: voiceId,             // 必需（与 input_text 一起）
    dimension: { width: 1920, height: 1080 },
  }),
});
```

## 在 Remotion 中使用 HeyGen 视频

### 重要：使用 OffthreadVideo 实现帧精确渲染

**始终使用 `OffthreadVideo` 而不是 `Video`** 来处理 HeyGen 虚拟角色视频。基本的 `Video` 组件使用浏览器的视频解码器，它不是帧精确的，在渲染时会导致抖动。`OffthreadVideo` 通过 FFmpeg 提取帧，实现平滑、准确的播放。

`OffthreadVideo` 包含在核心 `remotion` 包中——无需额外安装。

### 基本用法

```tsx
// remotion/src/AvatarComposition.tsx
import { OffthreadVideo, useVideoConfig } from "remotion";

interface AvatarCompositionProps {
  avatarVideoUrl: string;
}

export const AvatarComposition: React.FC<AvatarCompositionProps> = ({
  avatarVideoUrl,
}) => {
  return (
    <div style={{ flex: 1, backgroundColor: "#1a1a2e" }}>
      <OffthreadVideo
        src={avatarVideoUrl}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "contain",
        }}
      />
    </div>
  );
};
```

### 带透明背景的 WebM（推荐）

使用来自 `/v1/video.webm` 的 WebM——无需色键：

```tsx
import { OffthreadVideo, AbsoluteFill, Sequence } from "remotion";

export const AvatarWithMotionGraphics: React.FC<{
  avatarWebmUrl: string
}> = ({ avatarWebmUrl }) => {
  return (
    <AbsoluteFill>
      {/* 图层 1：您的背景/内容 */}
      <AbsoluteFill style={{ backgroundColor: "#1a1a2e" }}>
        <YourMotionGraphics />
      </AbsoluteFill>

      {/* 图层 2：带透明背景的虚拟角色 - 使用 OffthreadVideo 实现帧精确渲染 */}
      <OffthreadVideo
        src={avatarWebmUrl}
        transparent
        style={{
          position: "absolute",
          bottom: 0,
          right: 0,
          width: "50%",
          height: "auto",
        }}
      />

      {/* 图层 3：虚拟角色上方的叠加 */}
      <Sequence from={30}>
        <AnimatedTitle text="Welcome!" />
      </Sequence>
    </AbsoluteFill>
  );
};
```

### Loom 风格：圆形虚拟角色叠加在屏幕录制上

使用 `closeUp` 风格 + WebM，然后在 Remotion 中应用圆形遮罩：

```tsx
import { OffthreadVideo, AbsoluteFill } from "remotion";

export const LoomStyleComposition: React.FC<{
  screenRecordingUrl: string;
  avatarWebmUrl: string; // 使用 avatar_style: "closeUp" 通过 /v1/video.webm 生成
}> = ({ screenRecordingUrl, avatarWebmUrl }) => {
  return (
    <AbsoluteFill>
      {/* 屏幕录制填充画面 */}
      <OffthreadVideo src={screenRecordingUrl} style={{ width: "100%", height: "100%" }} />

      {/* 带圆形遮罩的虚拟角色 - 透明背景显示后面的屏幕 */}
      <OffthreadVideo
        src={avatarWebmUrl}
        transparent
        style={{
          position: "absolute",
          bottom: 40,
          left: 40,
          width: 180,
          height: 180,
          borderRadius: "50%", // 在 CSS 中应用圆形遮罩
          overflow: "hidden",
          objectFit: "cover",
        }}
      />
    </AbsoluteFill>
  );
};
```

**注意：** WebM 不支持 `circle` 样式——请使用 `normal` 或 `closeUp` 并通过 CSS 应用圆形遮罩。

### 传统：带色键的绿幕

如果使用带绿色背景的 MP4（不推荐——请改用 WebM）：

```tsx
// 注意：真正的色键需要 WebGL 或后期处理
// WebM 透明背景要简单得多
<OffthreadVideo
  src={avatarVideoUrl}
  style={{
    mixBlendMode: "multiply", // 仅基本合成
  }}
/>
```

### 分层合成

```tsx
import { OffthreadVideo, Sequence, useVideoConfig, Img } from "remotion";

interface LayeredAvatarProps {
  avatarVideoUrl: string;
  backgroundUrl: string;
  logoUrl: string;
  title: string;
}

export const LayeredAvatarComposition: React.FC<LayeredAvatarProps> = ({
  avatarVideoUrl,
  backgroundUrl,
  logoUrl,
  title,
}) => {
  const { fps } = useVideoConfig();

  return (
    <div style={{ position: "relative", width: "100%", height: "100%" }}>
      {/* 图层 1：背景 */}
      <Img
        src={backgroundUrl}
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />

      {/* 图层 2：虚拟角色视频 - 使用 OffthreadVideo 防止抖动 */}
      <OffthreadVideo
        src={avatarVideoUrl}
        style={{
          position: "absolute",
          bottom: 0,
          right: 0,
          width: "40%",
          height: "auto",
        }}
      />

      {/* 图层 3：标题（1秒后出现） */}
      <Sequence from={fps}>
        <div
          style={{
            position: "absolute",
            top: 50,
            left: 50,
            color: "white",
            fontSize: 48,
            fontWeight: "bold",
          }}
        >
          {title}
        </div>
      </Sequence>

      {/* 图层 4：标志 */}
      <Img
        src={logoUrl}
        style={{
          position: "absolute",
          top: 20,
          right: 20,
          width: 100,
          height: "auto",
        }}
      />
    </div>
  );
};
```

## 完整工作流

### 生成和合成

```typescript
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";

async function generateAvatarVideoForRemotion(
  script: string,
  outputPath: string
) {
  // 1. 生成 HeyGen 视频
  console.log("Generating HeyGen avatar video...");
  const videoId = await generateHeyGenVideo(
    script,
    "josh_lite3_20230714",
    "1bd001e7e50f421d891986aad5158bc8",
    "landscape_1080p"
  );

  // 2. 等待完成
  console.log("Waiting for HeyGen video...");
  const avatarVideoUrl = await waitForVideo(videoId);
  console.log(`HeyGen video ready: ${avatarVideoUrl}`);

  // 3. 获取视频时长用于 Remotion
  const avatarDuration = await getVideoDuration(avatarVideoUrl);
  const durationInFrames = Math.ceil(avatarDuration * 30); // 30 fps

  // 4. 打包 Remotion 项目
  console.log("Bundling Remotion project...");
  const bundleLocation = await bundle({
    entryPoint: "./remotion/src/index.ts",
  });

  // 5. 选择合成
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: "AvatarVideo",
    inputProps: {
      avatarVideoUrl,
    },
  });

  // 6. 渲染最终视频
  console.log("Rendering final composition...");
  await renderMedia({
    composition: {
      ...composition,
      durationInFrames,
    },
    serveUrl: bundleLocation,
    codec: "h264",
    outputLocation: outputPath,
    inputProps: {
      avatarVideoUrl,
    },
  });

  console.log(`Final video rendered: ${outputPath}`);
  return outputPath;
}
```

### 使用 calculateMetadata 的动态时长

```tsx
// remotion/src/AvatarComposition.tsx
import { CalculateMetadataFunction } from "remotion";

export const calculateAvatarMetadata: CalculateMetadataFunction<
  AvatarCompositionProps
> = async ({ props }) => {
  // 从 HeyGen 视频获取视频时长
  const duration = await getVideoDurationInSeconds(props.avatarVideoUrl);

  return {
    durationInFrames: Math.ceil(duration * 30),
    fps: 30,
    width: 1920,
    height: 1080,
  };
};

// 在 Root.tsx 中
<Composition
  id="AvatarVideo"
  component={AvatarComposition}
  calculateMetadata={calculateAvatarMetadata}
  defaultProps={{
    avatarVideoUrl: "",
  }}
/>
```

## 最佳实践

### 1. 使用绿幕增加灵活性

当您想要合成时，使用绿幕背景生成 HeyGen 视频：

```typescript
background: {
  type: "color",
  value: "#00FF00", // 纯绿用于色键
}
```

### 2. 匹配帧率

HeyGen 默认为 25 fps。在设置 Remotion fps 时考虑这一点：

```typescript
// 选项 1：匹配 HeyGen 的 25 fps
fps: 25

// 选项 2：使用 30 fps 并调整播放速率
<OffthreadVideo
  src={avatarVideoUrl}
  playbackRate={25/30} // 稍微减慢以匹配
/>
```

### 3. URL vs 下载：何时使用

**直接使用 URL 当：**
- 在 Remotion Studio 中预览时（`npm run dev`）
- URL 在渲染完成前不会过期
- 希望在开发期间更快迭代

```tsx
// 直接 URL 使用——更简单，开发更快
<OffthreadVideo src={avatarVideoUrl} />
```

**先下载当：**
- URL 有过期时间（HeyGen URL 约 24 小时后过期）
- 渲染将在稍后或重复进行
- 网络可靠性是问题
- 需要离线渲染

```typescript
// 带重试的下载，确保可靠性
async function downloadVideoWithRetry(
  url: string,
  outputPath: string,
  maxRetries = 5
): Promise<string> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const buffer = await response.arrayBuffer();
      await fs.promises.writeFile(outputPath, Buffer.from(buffer));
      return outputPath;
    } catch (error) {
      const delay = 2000 * Math.pow(2, attempt);
      console.log(`Retry ${attempt + 1}/${maxRetries} in ${delay}ms...`);
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  throw new Error("Download failed after retries");
}

// 在 Remotion 中使用本地文件
const localPath = await downloadVideoWithRetry(avatarVideoUrl, "./public/avatar.mp4");
```

**混合方法**（生产推荐）：
```typescript
// 在元数据中保存 URL 和本地路径
const metadata = {
  videoUrl: result.video_url,           // 用于快速预览
  localPath: "./public/avatar.mp4",     // 用于可靠渲染
  expiresAt: Date.now() + 24 * 60 * 60 * 1000, // URL 过期时间
};

// 在 Remotion 组件中，优先使用本地文件（如果可用）
const videoSrc = fs.existsSync(localPath) ? staticFile("avatar.mp4") : avatarVideoUrl;
```

### 4. 处理虚拟角色定位

合成中常见的虚拟角色位置：

```typescript
const AVATAR_POSITIONS = {
  fullscreen: { width: "100%", height: "100%", position: "center" },
  bottomRight: { width: "40%", bottom: 0, right: 0 },
  bottomLeft: { width: "40%", bottom: 0, left: 0 },
  pictureInPicture: { width: "25%", bottom: 20, right: 20 },
  leftThird: { width: "33%", left: 0, height: "100%" },
};
```

## 输出格式

### HeyGen 输出
- 格式：MP4 (H.264)
- 音频：AAC
- 分辨率：由请求指定

### Remotion 输出
- 编码器：H.264（默认）、VP8、VP9、ProRes
- 匹配或超过 HeyGen 质量设置

```typescript
await renderMedia({
  codec: "h264",
  crf: 18, // 高质量
  // ...
});
```

## 故障排除

### 视频在 Remotion 中不播放

1. 检查 URL 可访问性（CORS 问题）
2. 验证视频格式兼容性
3. 尝试先本地下载

### 尺寸不匹配

确保 HeyGen 和 Remotion 使用相同的尺寸：

```typescript
// 共享配置
const VIDEO_CONFIG = {
  width: 1920,
  height: 1080,
  fps: 30,
};

// HeyGen
dimension: { width: VIDEO_CONFIG.width, height: VIDEO_CONFIG.height }

// Remotion
<Composition width={VIDEO_CONFIG.width} height={VIDEO_CONFIG.height} />
```

### 渲染时视频抖动

如果虚拟角色视频在渲染输出中出现抖动或卡顿：

1. **使用 `OffthreadVideo` 而不是 `Video`** - 基本的 `Video` 组件使用浏览器的视频解码器，不是帧精确的
2. 更新导入（无需额外安装——在核心 `remotion` 中）：
   ```tsx
   // 之前（导致抖动）
   import { Video } from "remotion";

   // 之后（帧精确）
   import { OffthreadVideo } from "remotion";
   ```
3. 对于带透明的 WebM，添加 `transparent` 属性：
   ```tsx
   <OffthreadVideo src={avatarWebmUrl} transparent />
   ```

### 音频同步问题

如果虚拟角色音频漂移：
- 验证源视频帧率
- 检查编码问题
- 考虑使用一致设置重新编码
