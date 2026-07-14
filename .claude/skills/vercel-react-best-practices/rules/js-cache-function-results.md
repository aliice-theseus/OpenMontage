---
title: 缓存重复的函数调用
impact: MEDIUM
impactDescription: 避免冗余计算
tags: javascript, cache, memoization, performance
---

## 缓存重复的函数调用

当渲染期间反复使用相同输入调用同一函数时，使用模块级 Map 来缓存函数结果。

**错误做法（冗余计算）：**

```typescript
function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // slugify() 对相同项目名被调用 100+ 次
        const slug = slugify(project.name)
        
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**正确做法（缓存结果）：**

```typescript
// 模块级缓存
const slugifyCache = new Map<string, string>()

function cachedSlugify(text: string): string {
  if (slugifyCache.has(text)) {
    return slugifyCache.get(text)!
  }
  const result = slugify(text)
  slugifyCache.set(text, result)
  return result
}

function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // 每个唯一项目名仅计算一次
        const slug = cachedSlugify(project.name)
        
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**单值函数的更简单模式：**

```typescript
let isLoggedInCache: boolean | null = null

function isLoggedIn(): boolean {
  if (isLoggedInCache !== null) {
    return isLoggedInCache
  }
  
  isLoggedInCache = document.cookie.includes('auth=')
  return isLoggedInCache
}

// 认证变化时清除缓存
function onAuthChange() {
  isLoggedInCache = null
}
```

使用 Map（而非 hook），使其在任何地方都能工作：工具函数、事件处理函数，不仅限于 React 组件。

参考：[How we made the Vercel Dashboard twice as fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)
