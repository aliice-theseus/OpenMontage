# Widget 嵌入

使用 ElevenLabs 对话 widget 将语音 AI 代理添加到任何网站。

## 基本嵌入

```html
<elevenlabs-convai agent-id="your-agent-id"></elevenlabs-convai>
<script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
```

这将创建一个浮动按钮，用户可以点击开始语音对话。

> **注意：** Widget 目前需要禁用认证的公共代理。对于需要认证的流程，请使用 SDK。

## Widget 属性

### 必需

| 属性          | 描述                           |
|---------------|--------------------------------|
| `agent-id`    | 您的 ElevenLabs 代理 ID        |
| `signed-url`  | 使用有符号 URL 时替代 `agent-id` |

### 外观

| 属性                  | 描述                 | 默认值           |
|-----------------------|----------------------|------------------|
| `avatar-image-url`    | 代理头像图片 URL     | ElevenLabs 标志  |
| `avatar-orb-color-1`  | 主 orb 渐变颜色      | `#2792dc`        |
| `avatar-orb-color-2`  | 次 orb 渐变颜色      | `#9ce6e6`        |

### 文本标签

| 属性              | 描述             | 默认值             |
|-------------------|------------------|--------------------|
| `action-text`     | 悬停时工具提示   | "Talk to AI"       |
| `start-call-text` | 开始通话按钮     | "Start call"       |
| `end-call-text`   | 结束通话按钮     | "End call"         |
| `expand-text`     | 展开聊天按钮     | "Open"             |
| `collapse-text`   | 折叠聊天按钮     | "Close"            |
| `listening-text`  | 收听状态标签     | "Listening..."     |
| `speaking-text`   | 说话状态标签     | "Assistant speaking" |

### 行为

| 属性             | 描述                                        | 默认值     |
|------------------|---------------------------------------------|------------|
| `variant`        | Widget 样式：`compact` 或 `expanded`        | `compact`  |
| `server-location`| 服务器区域（`us`、`eu-residency`、`in-residency`、`global`）| `us`       |
| `dismissible`    | 允许用户最小化 widget                       | `false`    |
| `disable-banner` | 隐藏"Powered by ElevenLabs"                 | `false`    |

## 示例

### 自定义头像

```html
<elevenlabs-convai
  agent-id="your-agent-id"
  avatar-image-url="https://example.com/your-avatar.png"
></elevenlabs-convai>
```

### 自定义颜色

```html
<elevenlabs-convai
  agent-id="your-agent-id"
  avatar-orb-color-1="#ff6b6b"
  avatar-orb-color-2="#ffd93d"
></elevenlabs-convai>
```

### 自定义文本

```html
<elevenlabs-convai
  agent-id="your-agent-id"
  action-text="Chat with our AI assistant"
  start-call-text="Begin conversation"
  end-call-text="Hang up"
></elevenlabs-convai>
```

### 展开变体

```html
<elevenlabs-convai
  agent-id="your-agent-id"
  variant="expanded"
></elevenlabs-convai>
```

### 完全自定义

```html
<elevenlabs-convai
  agent-id="your-agent-id"
  avatar-image-url="https://example.com/support-agent.png"
  avatar-orb-color-1="#4f46e5"
  avatar-orb-color-2="#818cf8"
  action-text="Talk to Support"
  start-call-text="Start voice chat"
  end-call-text="End conversation"
  expand-text="Open assistant"
  collapse-text="Minimize"
></elevenlabs-convai>
```

## CSS 自定义

Widget 使用 Shadow DOM，但暴露了 CSS 自定义属性：

```css
elevenlabs-convai {
  --elevenlabs-convai-widget-width: 400px;
  --elevenlabs-convai-widget-height: 600px;
}
```

### 定位

默认情况下，widget 出现在右下角。使用 CSS 覆盖：

```css
elevenlabs-convai {
  position: fixed;
  bottom: 20px;
  right: 20px;
  /* 或不同定位 */
  left: 20px;
  right: auto;
}
```

### Z-Index

```css
elevenlabs-convai {
  z-index: 9999;
}
```

## JavaScript 控制

访问 widget 元素以通过编程方式控制它：

```html
<elevenlabs-convai id="my-widget" agent-id="your-agent-id"></elevenlabs-convai>

<script>
  const widget = document.getElementById("my-widget");

  // 开始对话
  widget.startConversation();

  // 结束对话
  widget.endConversation();

  // 监听事件
  widget.addEventListener("conversationStarted", () => {
    console.log("Conversation started");
  });

  widget.addEventListener("conversationEnded", () => {
    console.log("Conversation ended");
  });
</script>
```

### 自定义触发按钮

隐藏默认 widget 并使用自己的按钮：

```html
<style>
  elevenlabs-convai {
    display: none;
  }
</style>

<button onclick="document.getElementById('widget').startConversation()">
  Talk to AI
</button>

<elevenlabs-convai id="widget" agent-id="your-agent-id"></elevenlabs-convai>
```

## 认证

对于启用认证的代理，传递有符号 URL：

```html
<elevenlabs-convai id="widget" agent-id="your-agent-id"></elevenlabs-convai>

<script>
  async function startAuthenticatedConversation() {
    // 从后端获取有符号 URL
    const response = await fetch("/api/get-signed-url");
    const { signedUrl } = await response.json();

    const widget = document.getElementById("widget");
    widget.setAttribute("signed-url", signedUrl);
    widget.startConversation();
  }
</script>
```

您的后端：

```python
@app.get("/api/get-signed-url")
def get_signed_url():
    signed_url = client.conversational_ai.conversations.get_signed_url(
        agent_id="your-agent-id"
    )
    return {"signedUrl": signed_url.signed_url}
```

## 移动端考虑

### 响应式定位

```css
/* 桌面端：右下角 */
elevenlabs-convai {
  position: fixed;
  bottom: 20px;
  right: 20px;
}

/* 移动端：底部全宽 */
@media (max-width: 768px) {
  elevenlabs-convai {
    bottom: 0;
    right: 0;
    left: 0;
    --elevenlabs-convai-widget-width: 100%;
  }
}
```

### 触控友好

Widget 默认已优化触控。为更好的移动端体验：

```css
@media (max-width: 768px) {
  elevenlabs-convai {
    /* 更大的触控目标 */
    transform: scale(1.1);
    transform-origin: bottom right;
  }
}
```

## 多个 Widget

您可以为不同代理设置多个 widget：

```html
<elevenlabs-convai
  agent-id="support-agent-id"
  action-text="Support"
  style="right: 20px"
></elevenlabs-convai>

<elevenlabs-convai
  agent-id="sales-agent-id"
  action-text="Sales"
  style="right: 100px"
></elevenlabs-convai>
```

## 框架集成

### React

```jsx
function App() {
  useEffect(() => {
    // 加载 widget 脚本
    const script = document.createElement("script");
    script.src = "https://unpkg.com/@elevenlabs/convai-widget-embed";
    script.async = true;
    document.body.appendChild(script);

    return () => document.body.removeChild(script);
  }, []);

  return (
    <div>
      <elevenlabs-convai agent-id="your-agent-id"></elevenlabs-convai>
    </div>
  );
}
```

### Vue

```vue
<template>
  <div>
    <elevenlabs-convai agent-id="your-agent-id"></elevenlabs-convai>
  </div>
</template>

<script setup>
import { onMounted } from "vue";

onMounted(() => {
  const script = document.createElement("script");
  script.src = "https://unpkg.com/@elevenlabs/convai-widget-embed";
  script.async = true;
  document.body.appendChild(script);
});
</script>
```

### Next.js

```jsx
import Script from "next/script";

export default function Page() {
  return (
    <>
      <Script
        src="https://unpkg.com/@elevenlabs/convai-widget-embed"
        strategy="lazyOnload"
      />
      <elevenlabs-convai agent-id="your-agent-id"></elevenlabs-convai>
    </>
  );
}
```

## 故障排除

### Widget 不显示

1. 检查代理 ID 是否正确
2. 验证脚本是否已加载（检查 Network 标签页）
3. 检查控制台中是否有 JavaScript 错误
4. 确保没有 CSS 隐藏了 widget

### 音频问题

1. 确保使用 HTTPS（麦克风需要安全上下文）
2. 检查浏览器的麦克风权限
3. 在支持的浏览器中测试（Chrome、Firefox、Safari、Edge）

### CORS 错误

如果使用认证，请确保您的域名在代理的允许列表中：

```python
platform_settings={
    "auth": {
        "enable_auth": True,
        "allowlist": ["https://yourdomain.com"]
    }
}
```
