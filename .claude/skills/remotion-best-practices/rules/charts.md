---
name: charts
description: Remotion 图表和数据可视化模式。用于创建柱状图、饼图、折线图、股票图或任何数据驱动动画。
metadata:
  tags: charts, data, visualization, bar-chart, pie-chart, line-chart, stock-chart, svg-paths, graphs
---

# Remotion 中的图表

使用 React 代码创建图表——HTML、SVG 和 D3.js 均受支持。

禁用第三方库的所有动画——它们会导致闪烁。  
所有动画都通过 `useCurrentFrame()` 驱动。

## 柱状图

```tsx
const STAGGER_DELAY = 5;
const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const bars = data.map((item, i) => {
  const height = spring({
    frame,
    fps,
    delay: i * STAGGER_DELAY,
    config: { damping: 200 },
  });
  return <div style={{ height: height * item.value }} />;
});
```

## 饼图

使用 stroke-dashoffset 从12点钟方向开始动画化扇区：

```tsx
const progress = interpolate(frame, [0, 100], [0, 1]);
const circumference = 2 * Math.PI * radius;
const segmentLength = (value / total) * circumference;
const offset = interpolate(progress, [0, 1], [segmentLength, 0]);

<circle
  r={radius}
  cx={center}
  cy={center}
  fill="none"
  stroke={color}
  strokeWidth={strokeWidth}
  strokeDasharray={`${segmentLength} ${circumference}`}
  strokeDashoffset={offset}
  transform={`rotate(-90 ${center} ${center})`}
/>;
```

## 折线图 / 路径动画

使用 `@remotion/paths` 动画化 SVG 路径（折线图、股票图、签名）。

安装：`npx remotion add @remotion/paths`  
文档：https://remotion.dev/docs/paths.md

### 将数据点转换为 SVG 路径

```tsx
type Point = { x: number; y: number };

const generateLinePath = (points: Point[]): string => {
  if (points.length < 2) return "";
  return points.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`).join(" ");
};
```

### 带动画绘制路径

```tsx
import { evolvePath } from "@remotion/paths";

const path = "M 100 200 L 200 150 L 300 180 L 400 100";
const progress = interpolate(frame, [0, 2 * fps], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
  easing: Easing.out(Easing.quad),
});

const { strokeDasharray, strokeDashoffset } = evolvePath(progress, path);

<path
  d={path}
  fill="none"
  stroke="#FF3232"
  strokeWidth={4}
  strokeDasharray={strokeDasharray}
  strokeDashoffset={strokeDashoffset}
/>;
```

### 使用标记/箭头跟随路径

```tsx
import {
  getLength,
  getPointAtLength,
  getTangentAtLength,
} from "@remotion/paths";

const pathLength = getLength(path);
const point = getPointAtLength(path, progress * pathLength);
const tangent = getTangentAtLength(path, progress * pathLength);
const angle = Math.atan2(tangent.y, tangent.x);

<g
  style={{
    transform: `translate(${point.x}px, ${point.y}px) rotate(${angle}rad)`,
    transformOrigin: "0 0",
  }}
>
  <polygon points="0,0 -20,-10 -20,10" fill="#FF3232" />
</g>;
```
