# 实际操作示例：添加组件

## 场景

用户想要为其标题文本添加闪光扫光效果。

## 步骤

### 1. 安装组件

```bash
hyperframes add shimmer-sweep
```

### 2. 阅读片段

打开 `compositions/components/shimmer-sweep.html` 并阅读注释标题。

### 3. 接入到你的作品

**HTML**——包装目标元素：

```html
<div class="shimmer-sweep-target" style="--shimmer-color: rgba(255, 255, 255, 0.5)">
  <h1 class="title">AI 驱动视频</h1>
</div>
```

**CSS**——从片段粘贴 `.shimmer-sweep-target` 和 `.shimmer-mask` 规则。

**JS**——粘贴自动注入脚本（在时间线代码之前）：

```js
document.querySelectorAll(".shimmer-sweep-target").forEach((el) => {
  if (!el.querySelector(".shimmer-mask")) {
    const mask = document.createElement("div");
    mask.className = "shimmer-mask";
    el.appendChild(mask);
  }
});
```

**时间线**——添加扫光效果：

```js
tl.fromTo(
  ".shimmer-sweep-target",
  {
    "--shimmer-pos": "-20%",
  },
  {
    "--shimmer-pos": "120%",
    duration: 1.2,
    ease: "power2.inOut",
    stagger: 0.15,
  },
  1.5,
);
```

### 4. Lint 和预览

```bash
hyperframes lint
hyperframes preview
```

### 5. 自定义

- `--shimmer-color`：每个元素的高亮颜色
- `--shimmer-width`：光带宽度（默认 20%）
- `--shimmer-angle`：扫光方向（默认 120deg）
- 时间线 `duration`、`ease`、`stagger`：控制速度和感觉
