---
name: voices
description: 列出语音、语言区域、为 HeyGen 配置语速/音高
---

# HeyGen 语音

HeyGen 提供多种多样的 AI 语音，适用于不同语言、口音和风格。语音将你的文字脚本转化为自然听感的声音。

## 列出可用语音

### curl

```bash
curl -X GET "https://api.heygen.com/v2/voices" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface Voice {
  voice_id: string;
  name: string;
  language: string;
  gender: "male" | "female";
  preview_audio: string;
  support_pause: boolean;
  emotion_support: boolean;
}

interface VoicesResponse {
  error: null | string;
  data: {
    voices: Voice[];
  };
}

async function listVoices(): Promise<Voice[]> {
  const response = await fetch("https://api.heygen.com/v2/voices", {
    headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
  });

  const json: VoicesResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.voices;
}
```

### Python

```python
import requests
import os

def list_voices() -> list:
    response = requests.get(
        "https://api.heygen.com/v2/voices",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]}
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]["voices"]
```

## 响应格式

```json
{
  "error": null,
  "data": {
    "voices": [
      {
        "voice_id": "1bd001e7e50f421d891986aad5158bc8",
        "name": "Sara",
        "language": "English",
        "gender": "female",
        "preview_audio": "https://files.heygen.ai/...",
        "support_pause": true,
        "emotion_support": true
      },
      {
        "voice_id": "de8b5d78f2e0485f88d1e9f5c8e7f9a6",
        "name": "Paul",
        "language": "English",
        "gender": "male",
        "preview_audio": "https://files.heygen.ai/...",
        "support_pause": true,
        "emotion_support": false
      }
    ]
  }
}
```

## 支持的语言

HeyGen 支持多种语言，包括：

| 语言 | 代码 | 备注 |
|----------|------|-------|
| 英语（美国） | en-US | 多种语音选项 |
| 英语（英国） | en-GB | 英式口音 |
| 西班牙语 | es-ES | 西班牙西班牙语 |
| 西班牙语（拉丁） | es-MX | 墨西哥西班牙语 |
| 法语 | fr-FR | 法国法语 |
| 德语 | de-DE | 标准德语 |
| 葡萄牙语 | pt-BR | 巴西葡萄牙语 |
| 中文（普通话） | zh-CN | 简体中文 |
| 日语 | ja-JP | 标准日语 |
| 韩语 | ko-KR | 标准韩语 |
| 意大利语 | it-IT | 标准意大利语 |
| 荷兰语 | nl-NL | 标准荷兰语 |
| 波兰语 | pl-PL | 标准波兰语 |
| 阿拉伯语 | ar-SA | 沙特阿拉伯语 |

## 在视频生成中使用语音

### 基本语音用法

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Hello! Welcome to our presentation.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
};
```

### 带速度调整的语音

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "This is spoken at a faster pace.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
        speed: 1.2, // 1.0 是正常速度，范围：0.5 - 2.0
      },
    },
  ],
};
```

### 带音高调整的语音

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "This has a higher pitch.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
        pitch: 10, // 范围：-20 到 20
      },
    },
  ],
};
```

## 使用 Break 标签添加暂停

HeyGen 支持 SSML 风格的 `<break>` 标签，用于在脚本中添加暂停。

### Break 标签格式

```
<break time="Xs"/>
```

其中 `X` 是秒数（例如 `1s`, `1.5s`, `0.5s`）。

### 要求

| 规则 | 示例 |
|------|---------|
| 使用带 "s" 后缀的秒数 | `<break time="1.5s"/>` ✓ |
| 标签前必须有空格 | `word <break time="1s"/>` ✓ |
| 标签后必须有空格 | `<break time="1s"/> word` ✓ |
| 自闭合标签 | `<break time="1s"/>` ✓ |

**错误：** `word<break time="1s"/>word`（没有空格）
**正确：** `word <break time="1s"/> word`

### 示例

```typescript
// 单次暂停
const script1 = "大家好，欢迎。<break time=\"1s\"/> 让我介绍我们的产品。";

// 多次暂停
const script2 = "第一点。<break time=\"1.5s\"/> 第二点。<break time=\"1s\"/> 第三点。";

// 开头的暂停（戏剧性开场）
const script3 = "<break time=\"0.5s\"/> 欢迎来到我们的演示。";

// 更长的暂停用于强调
const script4 = "而获胜者是... <break time=\"2s\"/> 你！";
```

### 完整示例

```typescript
const scriptWithPauses = `
欢迎来到我们的产品演示。<break time="1s"/>
今天我将展示三个关键功能。<break time="0.5s"/>
首先，让我们看看仪表盘。<break time="1.5s"/>
正如你所看到的，它非常直观。
`;

const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: scriptWithPauses,
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
};
```

### 连续暂停

多个连续的 break 标签会被自动合并：

```typescript
// 这两个暂停：
"Hello <break time=\"1s\"/> <break time=\"0.5s\"/> world"

// 会被视为一个 1.5 秒的暂停
```

### 最佳实践

1. **用于强调** - 在重要点之前添加暂停
2. **保持暂停合理** - 0.5s 到 2s 是典型范围；过长会显得不自然
3. **匹配自然语音** - 在人类会呼吸或停顿的地方添加暂停
4. **测试输出** - 听取生成的音频以验证时机的舒适度

## 使用自定义音频替代 TTS

除了文字转语音，你也可以提供自己的音频：

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "audio",
        audio_url: "https://example.com/my-audio.mp3",
      },
    },
  ],
};
```

## 筛选语音

### 按语言

```typescript
function filterByLanguage(voices: Voice[], language: string): Voice[] {
  return voices.filter((v) =>
    v.language.toLowerCase().includes(language.toLowerCase())
  );
}

const englishVoices = filterByLanguage(voices, "english");
const spanishVoices = filterByLanguage(voices, "spanish");
```

### 按性别

```typescript
function filterByGender(voices: Voice[], gender: "male" | "female"): Voice[] {
  return voices.filter((v) => v.gender === gender);
}

const femaleVoices = filterByGender(voices, "female");
```

### 按功能

```typescript
function filterByFeatures(
  voices: Voice[],
  options: { supportPause?: boolean; emotionSupport?: boolean }
): Voice[] {
  return voices.filter((v) => {
    if (options.supportPause !== undefined && v.support_pause !== options.supportPause) {
      return false;
    }
    if (options.emotionSupport !== undefined && v.emotion_support !== options.emotionSupport) {
      return false;
    }
    return true;
  });
}

const expressiveVoices = filterByFeatures(voices, { emotionSupport: true });
```

## 语音选择辅助函数

```typescript
interface VoiceSelectionCriteria {
  language?: string;
  gender?: "male" | "female";
  supportPause?: boolean;
  emotionSupport?: boolean;
}

async function findVoice(criteria: VoiceSelectionCriteria): Promise<Voice | null> {
  const voices = await listVoices();

  const filtered = voices.filter((v) => {
    if (criteria.language && !v.language.toLowerCase().includes(criteria.language.toLowerCase())) {
      return false;
    }
    if (criteria.gender && v.gender !== criteria.gender) {
      return false;
    }
    if (criteria.supportPause !== undefined && v.support_pause !== criteria.supportPause) {
      return false;
    }
    if (criteria.emotionSupport !== undefined && v.emotion_support !== criteria.emotionSupport) {
      return false;
    }
    return true;
  });

  return filtered[0] || null;
}

// 使用示例
const voice = await findVoice({
  language: "english",
  gender: "female",
  emotionSupport: true,
});
```

## 多语言视频

为每个场景创建不同语言的视频：

```typescript
const multiLanguageConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Hello! Welcome to our global product launch.",
        voice_id: "english_voice_id",
      },
    },
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Hola! Bienvenidos al lanzamiento global de nuestro producto.",
        voice_id: "spanish_voice_id",
      },
    },
  ],
};
```

## 匹配语音到头像

### 推荐：使用头像的默认语音

许多头像有一个预先匹配好的 `default_voice_id`。**这是最佳方法。**

```typescript
// 使用 v2 API 获取带默认语音的头像
const response = await fetch(
  "https://api.heygen.com/v2/avatar_group.list?include_public=true",
  { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
);
const { data } = await response.json();

// 查找有默认语音的头像
const avatar = data.avatar_group_list.find((a: any) => a.default_voice_id);

if (avatar) {
  const videoConfig = {
    video_inputs: [{
      character: { type: "avatar", avatar_id: avatar.id },
      voice: {
        type: "text",
        input_text: script,
        voice_id: avatar.default_voice_id, // 预先匹配的语音
      },
    }],
  };
}
```

参见 [avatars.md](avatars.md) 获取完整示例。

### 备用方案：手动匹配性别

如果头像没有默认语音，手动匹配性别：

```typescript
interface AvatarVoicePair {
  avatarId: string;
  voiceId: string;
  gender: "male" | "female";
}

async function findMatchingAvatarAndVoice(
  preferredGender?: "male" | "female"
): Promise<AvatarVoicePair> {
  const [avatars, voices] = await Promise.all([
    listAvatars(),
    listVoices(),
  ]);

  // 无偏好时默认为男性
  const gender = preferredGender || "male";

  // 查找匹配性别的头像
  const avatar = avatars.find((a) => a.gender === gender);
  if (!avatar) {
    throw new Error(`没有可用的 ${gender} 头像`);
  }

  // 查找匹配性别和语言的语音
  const voice = voices.find(
    (v) => v.gender === gender && v.language.toLowerCase().includes("english")
  );
  if (!voice) {
    throw new Error(`没有可用的 ${gender} 英语语音`);
  }

  return {
    avatarId: avatar.avatar_id,
    voiceId: voice.voice_id,
    gender,
  };
}
```

## 最佳实践

1. **匹配语音性别到头像** - 始终将男性语音与男性头像配对，女性与女性配对
2. **匹配语音到内容** - 商务内容使用专业语音
3. **测试语音预览** - 在选择前收听预览音频
4. **考虑区域** - 匹配语音口音到目标受众
5. **使用自然的节奏** - 调整速度以确保清晰度，通常 0.9-1.1x
6. **添加暂停** - 使用 SSML 中断标签使语音更自然流畅
7. **验证可用性** - 在使用前始终确认 voice_id 存在
