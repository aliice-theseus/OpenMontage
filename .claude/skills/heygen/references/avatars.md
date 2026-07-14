---
name: avatars
description: 列出头像、头像样式和为 HeyGen 选择 avatar_id
---

# HeyGen 头像

头像是在 HeyGen 视频中作为 AI 生成的出镜人物。你可以使用 HeyGen 提供的公共头像，也可以创建自定义头像。

## 在生成前预览头像

在生成视频前始终预览头像，以确保它们符合用户偏好。每个头像都有预览 URL，可以直接在浏览器中打开——无需下载。

### 列出头像并显示预览

```typescript
async function listAndPreviewAvatars(openInBrowser = true): Promise<void> {
  const response = await fetch("https://api.heygen.com/v2/avatars", {
    headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
  });
  const { data } = await response.json();

  for (const avatar of data.avatars.slice(0, 5)) {
    console.log(`\n${avatar.avatar_name} (${avatar.gender})`);
    console.log(`  ID: ${avatar.avatar_id}`);
    console.log(`  Preview: ${avatar.preview_image_url}`);
  }

  // 预览 URL 可以直接在任何浏览器中打开
  for (const avatar of data.avatars.slice(0, 3)) {
    console.log(`Open in browser: ${avatar.preview_image_url}`);
  }
}
```

### 工作流：生成前预览

1. **列出可用头像** - 获取名称、性别和预览 URL
2. **向用户展示预览 URL** - 分享 `preview_image_url` 供视觉检查
3. **用户选择** 偏好的头像（按名称或 ID）
4. **获取头像详情** 获取 `default_voice_id`
5. **使用所选头像生成视频**

### API 响应中的预览字段

| 字段 | 描述 |
|-------|-------------|
| `preview_image_url` | 头像静态图片（JPG）- 可公开访问的 URL |
| `preview_video_url` | 显示头像动画的短视频片段 |

这两个 URL 都是公开可访问的——无需身份验证即可查看。

## 列出可用头像

### curl

```bash
curl -X GET "https://api.heygen.com/v2/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface Avatar {
  avatar_id: string;
  avatar_name: string;
  gender: "male" | "female";
  preview_image_url: string;
  preview_video_url: string;
}

interface AvatarsResponse {
  error: null | string;
  data: {
    avatars: Avatar[];
    talking_photos: TalkingPhoto[];
  };
}

async function listAvatars(): Promise<Avatar[]> {
  const response = await fetch("https://api.heygen.com/v2/avatars", {
    headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
  });

  const json: AvatarsResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.avatars;
}
```

### Python

```python
import requests
import os

def list_avatars() -> list:
    response = requests.get(
        "https://api.heygen.com/v2/avatars",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]}
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]["avatars"]
```

## 响应格式

```json
{
  "error": null,
  "data": {
    "avatars": [
      {
        "avatar_id": "josh_lite3_20230714",
        "avatar_name": "Josh",
        "gender": "male",
        "preview_image_url": "https://files.heygen.ai/...",
        "preview_video_url": "https://files.heygen.ai/..."
      },
      {
        "avatar_id": "angela_expressive_20231010",
        "avatar_name": "Angela",
        "gender": "female",
        "preview_image_url": "https://files.heygen.ai/...",
        "preview_video_url": "https://files.heygen.ai/..."
      }
    ],
    "talking_photos": []
  }
}
```

## 头像类型

### 公共头像

HeyGen 提供了一系列公共头像库，任何人都可以使用：

```typescript
// 仅列出公共头像
const avatars = await listAvatars();
const publicAvatars = avatars.filter((a) => !a.avatar_id.startsWith("custom_"));
```

### 私有/自定义头像

从你自己的训练素材创建的自定义头像：

```typescript
const customAvatars = avatars.filter((a) => a.avatar_id.startsWith("custom_"));
```

## 头像样式

头像支持不同的渲染样式：

| 样式 | 描述 |
|-------|-------------|
| `normal` | 全身镜头，标准构图 |
| `closeUp` | 面部特写，更具表现力 |
| `circle` | 圆形框架中的头像（说话人头像） |
| `voice_only` | 仅音频，不渲染视频 |

### 每种样式的使用场景

| 使用场景 | 推荐样式 |
|----------|-------------------|
| 全屏出镜视频 | `normal` |
| 个人/亲密内容 | `closeUp` |
| 画中画叠加 | `circle` |
| 小角落小部件 | `circle` |
| 播客/音频内容 | `voice_only` |
| 动态图形叠加头像 | `normal` 或 `closeUp` + 透明背景 |

### 使用头像样式

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal", // "normal" | "closeUp" | "circle" | "voice_only"
      },
      voice: {
        type: "text",
        input_text: "Hello, world!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
};
```

### Circle 样式用于说话人头像

Circle 样式非常适合叠加合成：

```typescript
// 画中画圆形头像
{
  character: {
    type: "avatar",
    avatar_id: "josh_lite3_20230714",
    avatar_style: "circle",
  },
  voice: { ... },
  background: {
    type: "color",
    value: "#00FF00", // 绿色用作色度键，或使用 webm 端点
  },
}
```

## 搜索和筛选头像

### 按性别

```typescript
function filterByGender(avatars: Avatar[], gender: "male" | "female"): Avatar[] {
  return avatars.filter((a) => a.gender === gender);
}

const maleAvatars = filterByGender(avatars, "male");
const femaleAvatars = filterByGender(avatars, "female");
```

### 按名称

```typescript
function searchByName(avatars: Avatar[], query: string): Avatar[] {
  const lowerQuery = query.toLowerCase();
  return avatars.filter((a) =>
    a.avatar_name.toLowerCase().includes(lowerQuery)
  );
}

const results = searchByName(avatars, "josh");
```

## 头像分组

头像被组织成组以便更好地管理。

### 列出头像组

```bash
curl -X GET "https://api.heygen.com/v2/avatar_group.list?include_public=true" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

#### 查询参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `include_public` | bool | false | 在结果中包括公共头像 |

#### TypeScript

```typescript
interface AvatarGroupItem {
  id: string;
  name: string;
  created_at: number;
  num_looks: number;
  preview_image: string;
  group_type: string;
  train_status: string;
  default_voice_id: string | null;
}

interface AvatarGroupListResponse {
  error: null | string;
  data: {
    avatar_group_list: AvatarGroupItem[];
  };
}

async function listAvatarGroups(
  includePublic = true
): Promise<AvatarGroupListResponse["data"]> {
  const params = new URLSearchParams({
    include_public: includePublic.toString(),
  });

  const response = await fetch(
    `https://api.heygen.com/v2/avatar_group.list?${params}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const json: AvatarGroupListResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data;
}
```

### 获取组中的头像

```bash
curl -X GET "https://api.heygen.com/v2/avatar_group/{group_id}/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## 在视频生成中使用头像

### 基本头像用法

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
        input_text: "Welcome to our product demo!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
  dimension: { width: 1920, height: 1080 },
};
```

### 使用不同头像的多场景

```typescript
const multiSceneConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Hi, I'm Josh. Let me introduce my colleague.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
    {
      character: {
        type: "avatar",
        avatar_id: "angela_expressive_20231010",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Hello! I'm Angela. Nice to meet you!",
        voice_id: "2d5b0e6a8c3f47d9a1b2c3d4e5f60718",
      },
    },
  ],
};
```

## 使用头像的默认语音

许多头像都有一个预先匹配好的 `default_voice_id`，可以获得自然的效果。**这是推荐的做法**，而不是手动选择语音。

### 推荐流程

```
1. GET /v2/avatars           → 获取 avatar_id 列表
2. GET /v2/avatar/{id}/details → 获取所选头像的 default_voice_id
3. POST /v2/video/generate   → 使用 avatar_id + default_voice_id
```

### 获取头像详情（v2 API）

给定一个 `avatar_id`，获取其详情，包括默认语音：

```bash
curl -X GET "https://api.heygen.com/v2/avatar/{avatar_id}/details" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

#### 响应格式

```json
{
  "error": null,
  "data": {
    "type": "avatar",
    "id": "josh_lite3_20230714",
    "name": "Josh",
    "gender": "male",
    "preview_image_url": "https://files.heygen.ai/...",
    "preview_video_url": "https://files.heygen.ai/...",
    "premium": false,
    "is_public": true,
    "default_voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "tags": ["AVATAR_IV"]
  }
}
```

#### TypeScript

```typescript
interface AvatarDetails {
  type: "avatar";
  id: string;
  name: string;
  gender: "male" | "female";
  preview_image_url: string;
  preview_video_url: string;
  premium: boolean;
  is_public: boolean;
  default_voice_id: string | null;
  tags: string[];
}

async function getAvatarDetails(avatarId: string): Promise<AvatarDetails> {
  const response = await fetch(
    `https://api.heygen.com/v2/avatar/${avatarId}/details`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const json = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data;
}

// 使用：获取已知头像的默认语音
const details = await getAvatarDetails("josh_lite3_20230714");
if (details.default_voice_id) {
  console.log(`Using ${details.name} with default voice: ${details.default_voice_id}`);
} else {
  console.log(`${details.name} has no default voice, select manually`);
}
```

#### 完整示例：使用任何头像的默认语音生成视频

```typescript
async function generateWithAvatarDefaultVoice(
  avatarId: string,
  script: string
): Promise<string> {
  // 1. 获取头像详情以找到默认语音
  const avatar = await getAvatarDetails(avatarId);

  if (!avatar.default_voice_id) {
    throw new Error(`Avatar ${avatar.name} has no default voice`);
  }

  // 2. 使用头像的默认语音生成视频
  const videoId = await generateVideo({
    video_inputs: [{
      character: {
        type: "avatar",
        avatar_id: avatar.id,
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: script,
        voice_id: avatar.default_voice_id,
      },
    }],
    dimension: { width: 1920, height: 1080 },
  });

  return videoId;
}
```

### 为什么使用默认语音？

1. **保证性别匹配** - 头像和语音已预先配对
2. **自然的唇形同步** - 默认语音已针对头像优化
3. **代码更简单** - 无需分别获取和匹配语音
4. **更高质量** - HeyGen 已测试过此组合

## 选择正确的头像

### 头像类别

HeyGen 头像分为不同的类别。根据你的使用场景匹配类别：

| 类别 | 示例 | 最适合 |
|----------|----------|----------|
| **商务/专业** | Josh, Angela, Wayne | 企业视频、产品演示、培训 |
| **休闲/友好** | Lily, 各种生活方式头像 | 社交媒体、非正式内容 |
| **主题/季节性** | 节日主题、角色扮演头像 | 特定活动、季节性内容 |
| **表现力丰富** | 名称中带有"expressive"的头像 | 引人入胜的故事讲述、动态内容 |

### 选择指南

**对于商务/专业内容：**
- 选择着装中性的头像（商务休闲或正式）
- 避免主题或季节性头像（节日服装、休闲装）
- 预览头像以确认专业外观
- 在选择性别和外貌时考虑受众群体

**对于休闲/社交内容：**
- 头像选择更灵活
- 主题头像可用于特定活动
- 匹配头像能量与内容基调

### 常见错误避免

1. **在商务内容中使用主题头像** - 节日主题的头像在产品演示中显得不专业
2. **生成前不预览** - 始终检查预览 URL 以确认外观
3. **忽略头像样式** - `circle` 样式可能不适用于全屏演示
4. **语音性别不匹配** - 始终使用头像的 `default_voice_id` 或手动匹配性别

### 选择清单

在生成视频之前：
- [ ] 在浏览器中预览过头像图片/视频
- [ ] 头像外观与内容基调匹配（专业 vs 休闲）
- [ ] 头像样式（`normal`, `closeUp`, `circle`）适合视频格式
- [ ] 语音性别与头像性别匹配
- [ ] 尽可能使用 `default_voice_id`

## 辅助函数

### 按 ID 获取头像

```typescript
async function getAvatarById(avatarId: string): Promise<Avatar | null> {
  const avatars = await listAvatars();
  return avatars.find((a) => a.avatar_id === avatarId) || null;
}
```

### 验证头像 ID

```typescript
async function isValidAvatarId(avatarId: string): Promise<boolean> {
  const avatar = await getAvatarById(avatarId);
  return avatar !== null;
}
```

### 获取随机头像

```typescript
async function getRandomAvatar(gender?: "male" | "female"): Promise<Avatar> {
  let avatars = await listAvatars();

  if (gender) {
    avatars = avatars.filter((a) => a.gender === gender);
  }

  const randomIndex = Math.floor(Math.random() * avatars.length);
  return avatars[randomIndex];
}
```

## 常用头像 ID

一些常用的公共头像 ID（可用性可能有所不同）：

| 头像 ID | 名称 | 性别 |
|-----------|------|--------|
| `josh_lite3_20230714` | Josh | 男 |
| `angela_expressive_20231010` | Angela | 女 |
| `wayne_20240422` | Wayne | 男 |
| `lily_20230614` | Lily | 女 |

在使用前始终通过调用列表端点来验证头像的可用性。
