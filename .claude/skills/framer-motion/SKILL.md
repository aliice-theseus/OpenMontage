---
name: framer-motion
description: 在 React 应用中使用 Framer Motion 实现迪士尼 12 项动画原则时使用
---

# Framer Motion 动画原则

使用 Framer Motion 的声明式 React API 实现所有 12 项迪士尼动画原则。

## 1. 挤压与拉伸（Squash and Stretch）

```jsx
<motion.div
  animate={{ scaleX: [1, 1.2, 1], scaleY: [1, 0.8, 1] }}
  transition={{ duration: 0.3, times: [0, 0.5, 1] }}
/>
```

## 2. 预备动作（Anticipation）

```jsx
<motion.div
  variants={{
    idle: { y: 0, scaleY: 1 },
    anticipate: { y: 10, scaleY: 0.9 },
    jump: { y: -200 }
  }}
  initial="idle"
  animate={["anticipate", "jump"]}
  transition={{ duration: 0.5, times: [0, 0.2, 1] }}
/>
```

## 3. 演出布局（Staging）

```jsx
<motion.div animate={{ filter: "blur(3px)", opacity: 0.6 }} /> {/* 背景 */}
<motion.div animate={{ scale: 1.1, zIndex: 10 }} /> {/* 主角 */}
```

## 4. 连续动作与关键姿势（Straight Ahead / Pose to Pose）

```jsx
<motion.div
  animate={{
    x: [0, 100, 200, 300],
    y: [0, -50, 0, -30]
  }}
  transition={{ duration: 1, ease: "easeInOut" }}
/>
```

## 5. 跟随与重叠动作（Follow Through and Overlapping Action）

```jsx
<motion.div animate={{ x: 200 }} transition={{ duration: 0.5 }}>
  <motion.span
    animate={{ x: 200 }}
    transition={{ duration: 0.5, delay: 0.05 }} // 头发
  />
  <motion.span
    animate={{ x: 200 }}
    transition={{ duration: 0.6, delay: 0.1 }} // 披风
  />
</motion.div>
```

## 6. 慢入慢出（Slow In and Slow Out）

```jsx
<motion.div
  animate={{ x: 300 }}
  transition={{
    duration: 0.6,
    ease: [0.42, 0, 0.58, 1] // easeInOut cubic-bezier
  }}
/>
// 或使用: "easeIn", "easeOut", "easeInOut"
```

## 7. 弧线运动（Arc）

```jsx
<motion.div
  animate={{
    x: [0, 100, 200],
    y: [0, -100, 0]
  }}
  transition={{ duration: 1, ease: "easeInOut" }}
/>
```

## 8. 次要动作（Secondary Action）

```jsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
  <motion.span
    animate={{ rotate: [0, 10, -10, 0] }}
    transition={{ duration: 0.3 }}
  >
    图标
  </motion.span>
</motion.button>
```

## 9. 时间节奏（Timing）

```jsx
const timings = {
  fast: { duration: 0.15 },
  normal: { duration: 0.3 },
  slow: { duration: 0.6 },
  spring: { type: "spring", stiffness: 300, damping: 20 }
};
```

## 10. 夸张表现（Exaggeration）

```jsx
<motion.div
  animate={{ scale: 1.5, rotate: 720 }}
  transition={{
    type: "spring",
    stiffness: 200,
    damping: 10 // 低阻尼 = 过量冲
  }}
/>
```

## 11. 扎实绘画（Solid Drawing）

```jsx
<motion.div
  style={{ perspective: 1000 }}
  animate={{ rotateX: 45, rotateY: 30 }}
  transition={{ duration: 0.5 }}
/>
```

## 12. 吸引力（Appeal）

```jsx
<motion.div
  whileHover={{
    scale: 1.02,
    boxShadow: "0 20px 40px rgba(0,0,0,0.2)"
  }}
  transition={{ duration: 0.3 }}
/>
```

## 子元素交错（Stagger Children）

```jsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(item => <motion.li variants={itemVariant} />)}
</motion.ul>
```

## 关键 Framer Motion 功能

- `animate` - 目标状态
- `variants` - 命名动画状态
- `whileHover` / `whileTap` - 手势动画
- `transition` - 时间和缓动
- `AnimatePresence` - 退出动画
- `useAnimation` - 编程控制
- `layout` - 自动动画布局变化
