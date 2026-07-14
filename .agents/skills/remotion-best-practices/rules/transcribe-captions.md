---
name: transcribe-captions
description: 转写音频以在 Remotion 中生成字幕
metadata:
  tags: captions, transcribe, whisper, audio, speech-to-text
---

# 转写音频

要在 Remotion 中转写音频以生成字幕，你可以使用 [`@remotion/install-whisper-cpp`](https://www.remotion.dev/docs/install-whisper-cpp) 包中的 [`transcribe()`](https://www.remotion.dev/docs/install-whisper-cpp/transcribe) 函数。

## 前置条件

首先，需要安装 @remotion/install-whisper-cpp 包。
如果尚未安装，请使用以下命令：

```bash
npx remotion add @remotion/install-whisper-cpp
```

## 转写

创建一个 Node.js 脚本来下载 Whisper.cpp 和模型，并转写音频。

```ts
import path from "path";
import {
  downloadWhisperModel,
  installWhisperCpp,
  transcribe,
  toCaptions,
} from "@remotion/install-whisper-cpp";
import fs from "fs";

const to = path.join(process.cwd(), "whisper.cpp");

await installWhisperCpp({
  to,
  version: "1.5.5",
});

await downloadWhisperModel({
  model: "medium.en",
  folder: to,
});

// 如有需要，首先将音频转换为 16KHz wav 文件：
// import {execSync} from 'child_process';
// execSync('ffmpeg -i /path/to/audio.mp4 -ar 16000 /path/to/audio.wav -y');

const whisperCppOutput = await transcribe({
  model: "medium.en",
  whisperPath: to,
  whisperCppVersion: "1.5.5",
  inputPath: "/path/to/audio123.wav",
  tokenLevelTimestamps: true,
});

// 可选：应用我们推荐的后处理
const { captions } = toCaptions({
  whisperCppOutput,
});

// 写入 public/ 文件夹，以便可以从 Remotion 获取
fs.writeFileSync("captions123.json", JSON.stringify(captions, null, 2));
```

分别转写每个片段并创建多个 JSON 文件。

参见[显示字幕](display-captions.md)了解如何在 Remotion 中显示字幕。
