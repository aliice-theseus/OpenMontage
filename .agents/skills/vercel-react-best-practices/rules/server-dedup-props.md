---
title: 避免 RSC 属性中的重复序列化
impact: LOW
impactDescription: 通过避免重复序列化减少网络传输
tags: server, rsc, serialization, props, client-components
---

## 避免 RSC 属性中的重复序列化

**影响：低（LOW）（通过避免重复序列化减少网络传输）**

RSC→client 序列化按对象引用去重，而非按值。相同引用 = 序列化一次；新引用 = 再次序列化。在客户端而非服务端进行转换操作（`.toSorted()`、`.filter()`、`.map()`）。

**不正确（重复数组）：**

```tsx
// RSC：发送 6 个字符串（2 个数组 × 3 项）
<ClientList usernames={usernames} usernamesOrdered={usernames.toSorted()} />
```

**正确（发送 3 个字符串）：**

```tsx
// RSC：发送一次
<ClientList usernames={usernames} />

// 客户端：在那里转换
'use client'
const sorted = useMemo(() => [...usernames].sort(), [usernames])
```

**嵌套去重行为：**

去重是递归工作的。影响因数据类型而异：

- `string[]`、`number[]`、`boolean[]`：**高影响** - 数组 + 所有原始类型完全重复
- `object[]`：**低影响** - 数组被重复，但嵌套对象按引用去重

```tsx
// string[] - 重复所有内容
usernames={['a','b']} sorted={usernames.toSorted()} // 发送 4 个字符串

// object[] - 仅重复数组结构
users={[{id:1},{id:2}]} sorted={users.toSorted()} // 发送 2 个数组 + 2 个唯一对象（不是 4）
```

**破坏去重的操作（创建新引用）：**

- 数组：`.toSorted()`、`.filter()`、`.map()`、`.slice()`、`[...arr]`
- 对象：`{...obj}`、`Object.assign()`、`structuredClone()`、`JSON.parse(JSON.stringify())`

**更多示例：**

```tsx
// ❌ 不良
<C users={users} active={users.filter(u => u.active)} />
<C product={product} productName={product.name} />

// ✅ 良好
<C users={users} />
<C product={product} />
// 在客户端进行过滤/解构
```

**例外：** 当转换成本很高或客户端不需要原始数据时，传递派生数据。
