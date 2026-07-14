---
title: 不要在组件内部定义组件
impact: HIGH
impactDescription: 防止每次渲染都重新挂载
tags: rerender, components, remount, performance
---

## 不要在组件内部定义组件

**影响：高（HIGH）（防止每次渲染都重新挂载）**

在另一个组件内部定义组件会在每次渲染时创建一个新的组件类型。React 每次都会看到一个不同的组件并完全重新挂载它，销毁所有状态和 DOM。

开发者这样做的一个常见原因是为了在不传递 props 的情况下访问父组件变量。始终改为传递 props。

**不正确（每次渲染都重新挂载）：**

```tsx
function UserProfile({ user, theme }) {
  // 在内部定义以访问 `theme` - 不良做法
  const Avatar = () => (
    <img
      src={user.avatarUrl}
      className={theme === 'dark' ? 'avatar-dark' : 'avatar-light'}
    />
  )

  // 在内部定义以访问 `user` - 不良做法
  const Stats = () => (
    <div>
      <span>{user.followers} 关注者</span>
      <span>{user.posts} 帖子</span>
    </div>
  )

  return (
    <div>
      <Avatar />
      <Stats />
    </div>
  )
}
```

每次 `UserProfile` 渲染时，`Avatar` 和 `Stats` 都是新的组件类型。React 卸载旧实例并挂载新实例，丢失任何内部状态、重新运行 effects 并重建 DOM 节点。

**正确（改为传递 props）：**

```tsx
function Avatar({ src, theme }: { src: string; theme: string }) {
  return (
    <img
      src={src}
      className={theme === 'dark' ? 'avatar-dark' : 'avatar-light'}
    />
  )
}

function Stats({ followers, posts }: { followers: number; posts: number }) {
  return (
    <div>
      <span>{followers} 关注者</span>
      <span>{posts} 帖子</span>
    </div>
  )
}

function UserProfile({ user, theme }) {
  return (
    <div>
      <Avatar src={user.avatarUrl} theme={theme} />
      <Stats followers={user.followers} posts={user.posts} />
    </div>
  )
}
```

**此错误的症状：**
- 输入框每次按键都失去焦点
- 动画意外重新开始
- `useEffect` 清理/设置在每次父渲染时执行
- 组件内的滚动位置重置
