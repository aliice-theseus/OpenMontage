---
name: avatars
description: 列出 HeyGen 的虚拟角色、虚拟角色风格和 avatar_id 选择
---

# HeyGen 虚拟角色

虚拟角色是 HeyGen 视频中的 AI 生成主持人。您可以使用 HeyGen 提供的公共虚拟角色或创建自定义虚拟角色。

## 在生成前预览虚拟角色

在生成视频前始终预览虚拟角色，以确保它们符合用户偏好。每个虚拟角色都有预览 URL，可直接在浏览器中打开 — 无需下载。

### 列出虚拟角色并显示预览

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

  // 预览 URL 可直接在任何浏览器中打开
  for (const avatar of data.avatars.slice(0, 3)) {
    console.log(`Open in browser: ${avatar.preview_image_url}`);
  }
}
```

### 工作流：先预览后生成

1. **列出可用虚拟角色** — 获取名称、性别和预览 URL
2. **向用户显示预览 URL** — 分享 `preview_image_url` 进行视觉检查
3. **用户选择**偏好的虚拟角色（按名称或 ID）
4. **获取虚拟角色详情**以获取 `default_voice_id`
5. **使用选定的虚拟角色生成视频**

### API 响应中的预览字段

| 字段 | 描述 |
|-------|-------------|
| `preview_image_url` | 虚拟角色的静态图片（JPG）— 公开可访问的 URL |
| `preview_video_url` | 显示虚拟角色动画的短视频片段 |

两个 URL 都是公开可访问的 — 查看无需身份验证。

## 列出可用虚拟角色

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

## 虚拟角色类型

### 公共虚拟角色

HeyGen 提供了一个公共虚拟角色库，任何人都可以使用：

```typescript
// 仅列出公共虚拟角色
const avatars = await listAvatars();
const publicAvatars = avatars.filter((a) => !a.avatar_id.startsWith("custom_"));
```

### 私有/自定义虚拟角色

从您自己的训练素材创建的自定义虚拟角色：

```typescript
const customAvatars = avatars.filter((a) => a.avatar_id.startsWith("custom_"));
```

## 虚拟角色风格

虚拟角色支持不同的渲染风格：

| 风格 | 描述 |
|-------|-------------|
| `normal` | 全身镜头，标准构图 |
| `closeUp` | 面部特写，更具表现力 |
| `circle` | 圆形画面中的虚拟角色（说话头像） |
| `voice_only` | 仅音频，无视频渲染 |

### 何时使用每种风格

| 使用场景 | 推荐风格 |
|----------|-------------------|
| 全屏主持人视频 | `normal` |
| 个人/亲密内容 | `closeUp` |
| 画中画覆盖层 | `circle` |
| 小角落小部件 | `circle` |
| 播客/音频内容 | `voice_only` |
| 带虚拟角色覆盖层的动态图形 | `normal` 或 `closeUp` + 透明背景 |

### 使用虚拟角色风格

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

### 用于说话头像的圆形风格

圆形风格非常适合覆盖层合成：

```typescript
// 用于画中画的圆形虚拟角色
{
  character: {
    type: "avatar",
    avatar_id: "josh_lite3_20230714",
    avatar_style: "circle",
  },
  voice: { ... },
  background: {
    type: "color",
    value: "#00FF00", // 绿色用于色度键，或使用 webm 端点
  },
}
```

## 搜索和过滤虚拟角色

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

## 虚拟角色分组

虚拟角色被组织成组以便更好地管理。

### 列出虚拟角色组

```bash
curl -X GET "https://api.heygen.com/v2/avatar_group.list?include_public=true" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

#### 查询参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `include_public` | bool | false | 在结果中包括公共虚拟角色 |

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

### 获取组中的虚拟角色

```bash
curl -X GET "https://api.heygen.com/v2/avatar_group/{group_id}/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## 在视频生成中使用虚拟角色

### 基本虚拟角色使用

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

### 使用不同虚拟角色的多场景

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

## 使用虚拟角色的默认声音

许多虚拟角色有一个预先匹配的 `default_voice_id`，以获得自然效果。**这是推荐的方法**，而不是手动选择声音。

### 推荐流程

```
1. GET /v2/avatars           → 获取 avatar_ids 列表
2. GET /v2/avatar/{id}/details → 获取所选虚拟角色的 default_voice_id
3. POST /v2/video/generate   → 使用 avatar_id + default_voice_id
```

### 获取虚拟角色详情（v2 API）

给定一个 `avatar_id`，获取其详情，包括默认声音：

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

// 使用：获取已知虚拟角色的默认声音
const details = await getAvatarDetails("josh_lite3_20230714");
if (details.default_voice_id) {
  console.log(`Using ${details.name} with default voice: ${details.default_voice_id}`);
} else {
  console.log(`${details.name} has no default voice, select manually`);
}
```

#### 完整示例：使用任意虚拟角色的默认声音生成视频

```typescript
async function generateWithAvatarDefaultVoice(
  avatarId: string,
  script: string
): Promise<string> {
  // 1. 获取虚拟角色详情以找到默认声音
  const avatar = await getAvatarDetails(avatarId);

  if (!avatar.default_voice_id) {
    throw new Error(`Avatar ${avatar.name} has no default voice`);
  }

  // 2. 使用虚拟角色的默认声音生成视频
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

### 为什么要使用默认声音？

1. **保证性别匹配** — 虚拟角色和声音预先配对
2. **自然的唇形同步** — 默认声音针对虚拟角色进行了优化
3. **更简单的代码** — 无需分别获取和匹配声音
4. **更好的质量** — HeyGen 已经测试过此组合

## 选择正确的虚拟角色

### 虚拟角色类别

HeyGen 虚拟角色分为不同的类别。将类别与您的使用场景匹配：

| 类别 | 示例 | 最适合 |
|----------|----------|----------|
| **商务/专业** | Josh, Angela, Wayne | 企业视频、产品演示、培训 |
| **休闲/友好** | Lily, 各种生活方式虚拟角色 | 社交媒体、非正式内容 |
| **主题/季节性** | 节日主题、服装虚拟角色 | 特定活动、季节性内容 |
| **表现力丰富** | 名称中带有"expressive"的虚拟角色 | 引人入胜的故事讲述、动态内容 |

### 选择指南

**对于商务/专业内容：**
- 选择着装中性的虚拟角色（商务休闲或正式）
- 避免主题或季节性虚拟角色（节日服装、休闲装）
- 预览虚拟角色以验证专业外观
- 选择性别和外貌时考虑您的受众人口统计

**对于休闲/社交内容：**
- 虚拟角色选择更灵活
- 主题虚拟角色可用于特定活动
- 匹配虚拟角色的能量与内容基调

### 常见错误避免

1. **在商务内容中使用主题虚拟角色** — 节日主题虚拟角色在产品演示中看起来不专业
2. **生成前不预览** — 始终检查预览 URL 以验证外观
3. **忽略虚拟角色风格** — `circle` 风格虚拟角色可能不适合全屏演示
4. **声音性别不匹配** — 始终使用虚拟角色的 `default_voice_id` 或手动匹配性别

### 选择清单

在生成视频之前：
- [ ] 在浏览器中预览了虚拟角色图片/视频
- [ ] 虚拟角色外观与内容基调匹配（专业 vs 休闲）
- [ ] 虚拟角色风格（`normal`、`closeUp`、`circle`）适合视频格式
- [ ] 声音性别与虚拟角色性别匹配
- [ ] 尽可能使用 `default_voice_id`

## 辅助函数

### 按 ID 获取虚拟角色

```typescript
async function getAvatarById(avatarId: string): Promise<Avatar | null> {
  const avatars = await listAvatars();
  return avatars.find((a) => a.avatar_id === avatarId) || null;
}
```

### 验证虚拟角色 ID

```typescript
async function isValidAvatarId(avatarId: string): Promise<boolean> {
  const avatar = await getAvatarById(avatarId);
  return avatar !== null;
}
```

### 获取随机虚拟角色

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

## 常用虚拟角色 ID

一些常用的公共虚拟角色 ID（可用性可能有所不同）：

| 虚拟角色 ID | 名称 | 性别 |
|-----------|------|--------|
| `josh_lite3_20230714` | Josh | 男性 |
| `angela_expressive_20231010` | Angela | 女性 |
| `wayne_20240422` | Wayne | 男性 |
| `lily_20230614` | Lily | 女性 |

在使用前始终通过调用列表端点来验证虚拟角色可用性。
