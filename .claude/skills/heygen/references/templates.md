---
name: templates
description: HeyGen 视频的模板列表和变量替换
---

# 视频模板

HeyGen 模板允许你创建带有变量占位符的可复用视频结构，实现大规模个性化视频生成。

## 列出模板

### curl

```bash
curl -X GET "https://api.heygen.com/v2/templates" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface Template {
  template_id: string;
  name: string;
  thumbnail_url: string;
  variables: TemplateVariable[];
}

interface TemplateVariable {
  name: string;
  type: "text" | "image" | "audio";
  properties?: {
    max_length?: number;
    default_value?: string;
  };
}

interface TemplatesResponse {
  error: null | string;
  data: {
    templates: Template[];
  };
}

async function listTemplates(): Promise<Template[]> {
  const response = await fetch("https://api.heygen.com/v2/templates", {
    headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
  });

  const json: TemplatesResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.templates;
}
```

### Python

```python
import requests
import os

def list_templates() -> list:
    response = requests.get(
        "https://api.heygen.com/v2/templates",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]}
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]["templates"]
```

## 响应格式

```json
{
  "error": null,
  "data": {
    "templates": [
      {
        "template_id": "template_abc123",
        "name": "Product Announcement",
        "thumbnail_url": "https://files.heygen.ai/...",
        "variables": [
          {
            "name": "product_name",
            "type": "text",
            "properties": {
              "max_length": 50
            }
          },
          {
            "name": "presenter_script",
            "type": "text",
            "properties": {
              "max_length": 500
            }
          },
          {
            "name": "product_image",
            "type": "image"
          }
        ]
      }
    ]
  }
}
```

## 获取模板详情

### curl

```bash
curl -X GET "https://api.heygen.com/v2/template/{template_id}" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
async function getTemplate(templateId: string): Promise<Template> {
  const response = await fetch(
    `https://api.heygen.com/v2/template/${templateId}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const json = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data;
}
```

## 从模板生成视频

### 请求字段

| 字段 | 类型 | 必需 | 描述 |
|-------|------|:---:|-------------|
| `variables` | object | ✓ | 匹配模板变量的键值对 |
| `test` | boolean | | 测试模式（带水印，不消耗积分） |
| `title` | string | | 用于组织的视频名称 |
| `callback_id` | string | | 用于 webhook 跟踪的自定义 ID |
| `callback_url` | string | | 完成通知的 URL |

**注意：** `variables` 对象的键必须与模板定义的变量名称匹配。查看模板详情以了解定义了哪些变量。

### curl

```bash
curl -X POST "https://api.heygen.com/v2/template/{template_id}/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "test": false,
    "variables": {
      "product_name": "SuperWidget Pro",
      "presenter_script": "Introducing our latest innovation!",
      "product_image": "https://example.com/product.jpg"
    }
  }'
```

### TypeScript

```typescript
interface TemplateGenerateRequest {
  variables: Record<string, string>;           // 必需
  test?: boolean;
  title?: string;
  callback_id?: string;
  callback_url?: string;
}

interface TemplateGenerateResponse {
  error: null | string;
  data: {
    video_id: string;
  };
}

async function generateFromTemplate(
  templateId: string,
  variables: Record<string, string>,
  test: boolean = false
): Promise<string> {
  const response = await fetch(
    `https://api.heygen.com/v2/template/${templateId}/generate`,
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ test, variables }),
    }
  );

  const json: TemplateGenerateResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.video_id;
}
```

### Python

```python
def generate_from_template(template_id: str, variables: dict, test: bool = False) -> str:
    response = requests.post(
        f"https://api.heygen.com/v2/template/{template_id}/generate",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json"
        },
        json={
            "test": test,
            "variables": variables
        }
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]["video_id"]
```

## 变量类型

### 文本变量

用于动态文本内容：

```typescript
const variables = {
  customer_name: "John Smith",
  product_name: "SuperWidget Pro",
  price: "$99.99",
  cta_text: "立即订购！",
};
```

### 图片变量

用于动态图片（背景、产品照片）：

```typescript
const variables = {
  product_image: "https://example.com/product.jpg",
  logo: "https://example.com/logo.png",
  background: "https://example.com/bg.jpg",
};
```

### 音频变量

用于自定义音频内容：

```typescript
const variables = {
  background_music: "https://example.com/music.mp3",
  custom_voiceover: "https://example.com/voiceover.mp3",
};
```

## 批量视频生成

从模板生成多个个性化视频：

```typescript
interface PersonalizationData {
  name: string;
  email: string;
  company: string;
  customMessage: string;
}

async function batchGenerateVideos(
  templateId: string,
  recipients: PersonalizationData[]
): Promise<string[]> {
  const videoIds: string[] = [];

  for (const recipient of recipients) {
    const variables = {
      recipient_name: recipient.name,
      company_name: recipient.company,
      personalized_message: recipient.customMessage,
    };

    const videoId = await generateFromTemplate(templateId, variables);
    videoIds.push(videoId);

    // 速率限制：在请求之间添加延迟
    await new Promise((r) => setTimeout(r, 1000));
  }

  return videoIds;
}

// 使用示例
const recipients = [
  {
    name: "John Smith",
    email: "john@example.com",
    company: "Acme Inc",
    customMessage: "感谢您对我们产品的关注！",
  },
  {
    name: "Jane Doe",
    email: "jane@example.com",
    company: "Tech Corp",
    customMessage: "我们很乐意为您演示！",
  },
];

const videoIds = await batchGenerateVideos("template_abc123", recipients);
```

## 模板变量验证

在生成前验证变量：

```typescript
function validateTemplateVariables(
  template: Template,
  variables: Record<string, string>
): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  for (const templateVar of template.variables) {
    const value = variables[templateVar.name];

    // 检查是否提供了必需的变量
    if (!value) {
      errors.push(`缺少必需变量：${templateVar.name}`);
      continue;
    }

    // 检查文本长度限制
    if (templateVar.type === "text" && templateVar.properties?.max_length) {
      if (value.length > templateVar.properties.max_length) {
        errors.push(
          `变量 "${templateVar.name}" 超过最大长度 ${templateVar.properties.max_length}`
        );
      }
    }

    // 验证图片 URL
    if (templateVar.type === "image") {
      try {
        new URL(value);
      } catch {
        errors.push(`变量 "${templateVar.name}" 不是有效的 URL`);
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
```

## 完整模板工作流

```typescript
async function createPersonalizedVideo(
  templateId: string,
  personalization: Record<string, string>
): Promise<string> {
  // 1. 获取模板详情
  const template = await getTemplate(templateId);
  console.log(`使用模板：${template.name}`);

  // 2. 验证变量
  const validation = validateTemplateVariables(template, personalization);
  if (!validation.valid) {
    throw new Error(`验证错误：${validation.errors.join(", ")}`);
  }

  // 3. 生成视频
  console.log("正在生成视频...");
  const videoId = await generateFromTemplate(templateId, personalization);
  console.log(`视频 ID：${videoId}`);

  // 4. 等待完成
  const videoUrl = await waitForVideo(videoId);
  console.log(`视频就绪：${videoUrl}`);

  return videoUrl;
}

// 使用示例
const videoUrl = await createPersonalizedVideo("template_abc123", {
  customer_name: "John Smith",
  product_name: "SuperWidget Pro",
  offer_details: "首次订单享受 20% 折扣！",
});
```

## 最佳实践

1. **设计灵活性** - 使用通用占位符创建模板
2. **设置合理限制** - 为文本变量定义最大长度
3. **验证输入** - 在生成前检查变量值
4. **使用测试模式** - 在生产前使用 `test: true` 进行验证
5. **实施速率限制** - 批量生成时添加延迟
6. **缓存模板数据** - 通过缓存模板详情减少 API 调用
7. **错误处理** - 优雅地处理生成失败

## 使用场景

- **销售推广** - 个性化的潜在客户视频
- **客户 onboarding** - 带客户姓名的欢迎视频
- **产品更新** - 带有动态内容的公告
- **培训** - 定制化的培训模块
- **营销活动** - 针对性的促销视频
