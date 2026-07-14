---
title: 提取到 Memo 化组件中
impact: MEDIUM
impactDescription: 启用提前返回
tags: rerender, memo, useMemo, optimization
---

## 提取到 Memo 化组件中

将昂贵的工作提取到 memo 化组件中，以便在计算之前提前返回。

**不正确（即使在加载时也计算头像）：**

```tsx
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => {
    const id = computeAvatarId(user)
    return <Avatar id={id} />
  }, [user])

  if (loading) return <Skeleton />
  return <div>{avatar}</div>
}
```

**正确（加载时跳过计算）：**

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user])
  return <Avatar id={id} />
})

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return (
    <div>
      <UserAvatar user={user} />
    </div>
  )
}
```

**注意：** 如果你的项目启用了 [React Compiler](https://react.dev/learn/react-compiler)，则不需要手动使用 `memo()` 和 `useMemo()` 进行 memo 化。编译器会自动优化重渲染。
