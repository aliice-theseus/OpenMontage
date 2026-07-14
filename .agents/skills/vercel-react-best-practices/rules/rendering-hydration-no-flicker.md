---
title: 防止注水不匹配且不闪屏
impact: MEDIUM
impactDescription: 避免视觉闪烁和注水错误
tags: rendering, ssr, hydration, localStorage, flicker
---

## 防止注水不匹配且不闪屏

当渲染依赖于客户端存储（localStorage、cookies）的内容时，通过注入一个在 React 注水前同步更新 DOM 的脚本来避免 SSR 破坏和注水后闪烁。

**不正确（破坏 SSR）：**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  // localStorage 在服务端不可用 - 抛出错误
  const theme = localStorage.getItem('theme') || 'light'
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

服务端渲染会失败，因为 `localStorage` 未定义。

**不正确（视觉闪烁）：**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState('light')
  
  useEffect(() => {
    // 在注水后执行 - 导致可见闪烁
    const stored = localStorage.getItem('theme')
    if (stored) {
      setTheme(stored)
    }
  }, [])
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

组件首先使用默认值（`light`）渲染，然后在注水后更新，导致错误内容的可见闪烁。

**正确（无闪烁，无注水不匹配）：**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  return (
    <>
      <div id="theme-wrapper">
        {children}
      </div>
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              try {
                var theme = localStorage.getItem('theme') || 'light';
                var el = document.getElementById('theme-wrapper');
                if (el) el.className = theme;
              } catch (e) {}
            })();
          `,
        }}
      />
    </>
  )
}
```

内联脚本在显示元素之前同步执行，确保 DOM 已经具有正确的值。无闪烁，无注水不匹配。

这种模式对于主题切换、用户偏好、身份验证状态和任何应立即渲染而不闪烁默认值的仅客户端数据特别有用。
