---
name: voices
description: Listing voices, locales, speed/pitch configuration for HeyGen
---

# HeyGen 语音

HeyGen 提供了广泛的 AI 语音选择，适用于不同的语言、口音和风格。语音将您的文本脚本转换为自然的声音。

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

| Language | Code | Notes |
|----------|------|-------|
| English (US) | en-US | Multiple voice options |
| English (UK) | en-GB | British accent |
| Spanish | es-ES | Spain Spanish |
| Spanish (Latin) | es-MX | Mexican Spanish |
| French | fr-FR | France French |
| German | de-DE | Standard German |
| Portuguese | pt-BR | Brazilian Portuguese |
| Chinese (Mandarin) | zh-CN | Simplified Chinese |
| Japanese | ja-JP | Standard Japanese |
| Korean | ko-KR | Standard Korean |
| Italian | it-IT | Standard Italian |
| Dutch | nl-NL | Standard Dutch |
| Polish | pl-PL | Standard Polish |
| Arabic | ar-SA | Saudi Arabic |

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

### 调整语速

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
        speed: 1.2, // 1.0 is normal, range: 0.5 - 2.0
      },
    },
  ],
};
```

### 调整音调

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
        pitch: 10, // Range: -20 to 20
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

其中 `X` 是以秒为单位的时长（例如 `1s`、`1.5s`、`0.5s`）。

### 要求

| 规则 | 示例 |
|------|---------|
| 使用秒并带 "s" 后缀 | `<break time="1.5s"/>` ✓ |
| 标签前必须有空格 | `word <break time="1s"/>` ✓ |
| 标签后必须有空格 | `<break time="1s"/> word` ✓ |
| 自闭合标签 | `<break time="1s"/>` ✓ |

**错误：** `word<break time="1s"/>word`（无空格）
**正确：** `word <break time="1s"/> word`

### 示例

```typescript
// Single pause
const script1 = "Hello and welcome. <break time=\"1s\"/> Let me introduce our product.";

// Multiple pauses
const script2 = "First point. <break time=\"1.5s\"/> Second point. <break time=\"1s\"/> Third point.";

// Pause at start (dramatic opening)
const script3 = "<break time=\"0.5s\"/> Welcome to our presentation.";

// Longer pause for emphasis
const script4 = "And the winner is... <break time=\"2s\"/> You!";
```

### 完整示例

```typescript
const scriptWithPauses = `
Welcome to our product demo. <break time="1s"/>
Today I'll show you three key features. <break time="0.5s"/>
First, let's look at the dashboard. <break time="1.5s"/>
As you can see, it's incredibly intuitive.
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

多个连续的 break 标签会自动合并：

```typescript
// These two breaks:
"Hello <break time=\"1s\"/> <break time=\"0.5s\"/> world"

// Are treated as a single 1.5s pause
```

### 最佳实践

1. **用于强调** - 在重要点之前添加暂停
2. **保持暂停合理** - 0.5s 到 2s 是典型的；更长会感觉不自然
3. **匹配自然语音** - 在人类会呼吸或停顿的地方添加暂停
4. **测试输出** - 收听生成的音频以验证时间节奏

## 使用自定义音频代替 TTS

除了文本转语音，您还可以提供自己的音频：

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

### 按特性

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

## 语音选择辅助

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

// Usage
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

## 匹配语音与虚拟形象

### 推荐：使用虚拟形象的默认语音

许多虚拟形象都有预先匹配的 `default_voice_id`。**这是最佳方法。**

```typescript
// Using v2 API to get avatar with default voice
const response = await fetch(
  "https://api.heygen.com/v2/avatar_group.list?include_public=true",
  { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
);
const { data } = await response.json();

// Find avatar with a default voice
const avatar = data.avatar_group_list.find((a: any) => a.default_voice_id);

if (avatar) {
  const videoConfig = {
    video_inputs: [{
      character: { type: "avatar", avatar_id: avatar.id },
      voice: {
        type: "text",
        input_text: script,
        voice_id: avatar.default_voice_id, // Pre-matched voice
      },
    }],
  };
}
```

完整的示例请参见 [avatars.md](avatars.md)。

### 回退方案：手动匹配性别

如果虚拟形象没有默认语音，手动匹配性别：

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

  // Default to male if no preference
  const gender = preferredGender || "male";

  // Find avatar with matching gender
  const avatar = avatars.find((a) => a.gender === gender);
  if (!avatar) {
    throw new Error(`No ${gender} avatar available`);
  }

  // Find voice with matching gender AND language
  const voice = voices.find(
    (v) => v.gender === gender && v.language.toLowerCase().includes("english")
  );
  if (!voice) {
    throw new Error(`No ${gender} English voice available`);
  }

  return {
    avatarId: avatar.avatar_id,
    voiceId: voice.voice_id,
    gender,
  };
}
```

## 最佳实践

1. **匹配语音性别与虚拟形象** - 始终将男性语音与男性虚拟形象配对，女性与女性配对
2. **语音与内容匹配** - 为商务内容使用专业语音
3. **测试语音预览** - 在选择前收听预览音频
4. **考虑语言区域** - 将语音口音与目标受众匹配
5. **使用自然节奏** - 调整语速以保证清晰度，通常 0.9-1.1x
6. **添加暂停** - 使用 SSML breaks 使语音流更自然
7. **验证可用性** - 在使用前始终确认 voice_id 存在
