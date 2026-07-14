---
name: d3-viz
description: 使用 d3.js 创建交互式数据可视化。适用于创建自定义图表、图形、网络图、地理可视化或任何需要精细控制视觉元素、过渡或交互的复杂基于 SVG 的数据可视化。无论是 React、Vue、Svelte、原生 JavaScript 还是其他环境，当需要超越标准图表库的定制可视化时使用此技能。
---

# D3.js 可视化

## 概述

本技能提供使用 d3.js 创建复杂交互式数据可视化的指南。D3.js（数据驱动文档）擅长将数据绑定到 DOM 元素并应用数据驱动的转换，以创建对每个视觉元素具有精确控制的自定义、出版级可视化。这些技术适用于任何 JavaScript 环境，包括原生 JavaScript、React、Vue、Svelte 和其他框架。

## 何时使用 d3.js

**使用 d3.js 的场景：**
- 需要独特视觉编码或布局的自定义可视化
- 具有复杂平移、缩放或刷选行为的交互式探索
- 网络/图形可视化（力导向布局、树形图、层次结构、弦图）
- 具有自定义投影的地理可视化
- 需要平滑编排过渡的可视化
- 需要精细样式控制的出版级图形
- 标准库中不可用的新颖图表类型

**考虑替代方案的场景：**
- 3D 可视化 - 改用 Three.js

## 核心工作流程

### 1. 设置 d3.js

在脚本顶部导入 d3：

```javascript
import * as d3 from 'd3';
```

或使用 CDN 版本（7.x）：

```html
<script src="https://d3js.org/d3.v7.min.js"></script>
```

所有模块（比例尺、坐标轴、形状、过渡等）都可通过 `d3` 命名空间访问。

### 2. 选择集成模式

**模式 A：直接 DOM 操作（推荐大多数情况）**
使用 d3 选择 DOM 元素并进行命令式操作。适用于任何 JavaScript 环境：

```javascript
function drawChart(data) {
  if (!data || data.length === 0) return;

  const svg = d3.select('#chart'); // 通过 ID、class 或 DOM 元素选择

  // 清除之前的内容
  svg.selectAll("*").remove();

  // 设置尺寸
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };

  // 创建比例尺、坐标轴并绘制可视化
  // ... d3 代码 ...
}

// 数据变化时调用
drawChart(myData);
```

**模式 B：声明式渲染（适用于带模板的框架）**
使用 d3 进行数据计算（比例尺、布局），但通过框架渲染元素：

```javascript
function getChartElements(data) {
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([0, 400]);

  return data.map((d, i) => ({
    x: 50,
    y: i * 30,
    width: xScale(d.value),
    height: 25
  }));
}

// 在 React 中：{getChartElements(data).map((d, i) => <rect key={i} {...d} fill="steelblue" />)}
// 在 Vue 中：对返回数组使用 v-for 指令
// 在原生 JS 中：从返回数据手动创建元素
```

对于具有过渡、交互或需要充分利用 d3 功能的复杂可视化，使用模式 A。对于更简单的可视化或框架偏好声明式渲染时，使用模式 B。

### 3. 结构化可视化代码

在绘图函数中遵循以下标准结构：

```javascript
function drawVisualization(data) {
  if (!data || data.length === 0) return;

  const svg = d3.select('#chart'); // 或传入选择器/元素
  svg.selectAll("*").remove(); // 清除之前的渲染

  // 1. 定义尺寸
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // 2. 创建带边距的主组
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // 3. 创建比例尺
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]); // 注意：SVG 坐标反转

  // 4. 创建并添加坐标轴
  const xAxis = d3.axisBottom(xScale);
  const yAxis = d3.axisLeft(yScale);

  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(xAxis);

  g.append("g")
    .call(yAxis);

  // 5. 绑定数据并创建视觉元素
  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 5)
    .attr("fill", "steelblue");
}

// 数据变化时调用
drawVisualization(myData);
```

### 4. 实现响应式尺寸

使可视化适应容器大小：

```javascript
function setupResponsiveChart(containerId, data) {
  const container = document.getElementById(containerId);
  const svg = d3.select(`#${containerId}`).append('svg');

  function updateChart() {
    const { width, height } = container.getBoundingClientRect();
    svg.attr('width', width).attr('height', height);

    // 使用新尺寸重新绘制可视化
    drawChart(data, svg, width, height);
  }

  // 初始加载时更新
  updateChart();

  // 窗口大小变化时更新
  window.addEventListener('resize', updateChart);

  // 返回清理函数
  return () => window.removeEventListener('resize', updateChart);
}

// 用法：
// const cleanup = setupResponsiveChart('chart-container', myData);
// cleanup(); // 组件卸载或元素移除时调用
```

或使用 ResizeObserver 进行更直接的容器监控：

```javascript
function setupResponsiveChartWithObserver(svgElement, data) {
  const observer = new ResizeObserver(() => {
    const { width, height } = svgElement.getBoundingClientRect();
    d3.select(svgElement)
      .attr('width', width)
      .attr('height', height);

    // 重新绘制可视化
    drawChart(data, d3.select(svgElement), width, height);
  });

  observer.observe(svgElement.parentElement);
  return () => observer.disconnect();
}
```

## 常见可视化模式

### 柱状图

```javascript
function drawBarChart(data, svgElement) {
  if (!data || data.length === 0) return;

  const svg = d3.select(svgElement);
  svg.selectAll("*").remove();

  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleBand()
    .domain(data.map(d => d.category))
    .range([0, innerWidth])
    .padding(0.1);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([innerHeight, 0]);

  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));

  g.append("g")
    .call(d3.axisLeft(yScale));

  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.category))
    .attr("y", d => yScale(d.value))
    .attr("width", xScale.bandwidth())
    .attr("height", d => innerHeight - yScale(d.value))
    .attr("fill", "steelblue");
}

// 用法：
// drawBarChart(myData, document.getElementById('chart'));
```

### 折线图

```javascript
const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value))
  .curve(d3.curveMonotoneX); // 平滑曲线

g.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", "steelblue")
  .attr("stroke-width", 2)
  .attr("d", line);
```

### 散点图

```javascript
g.selectAll("circle")
  .data(data)
  .join("circle")
  .attr("cx", d => xScale(d.x))
  .attr("cy", d => yScale(d.y))
  .attr("r", d => sizeScale(d.size)) // 可选：尺寸编码
  .attr("fill", d => colourScale(d.category)) // 可选：颜色编码
  .attr("opacity", 0.7);
```

### 弦图

弦图以圆形布局展示实体之间的关系，用色带表示它们之间的流动：

```javascript
function drawChordDiagram(data) {
  // data format: array of objects with source, target, and value
  // Example: [{ source: 'A', target: 'B', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 600;
  const height = 600;
  const innerRadius = Math.min(width, height) * 0.3;
  const outerRadius = innerRadius + 30;

  // Create matrix from data
  const nodes = Array.from(new Set(data.flatMap(d => [d.source, d.target])));
  const matrix = Array.from({ length: nodes.length }, () => Array(nodes.length).fill(0));

  data.forEach(d => {
    const i = nodes.indexOf(d.source);
    const j = nodes.indexOf(d.target);
    matrix[i][j] += d.value;
    matrix[j][i] += d.value;
  });

  // Create chord layout
  const chord = d3.chord()
    .padAngle(0.05)
    .sortSubgroups(d3.descending);

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

  const ribbon = d3.ribbon()
    .source(d => d.source)
    .target(d => d.target);

  const colourScale = d3.scaleOrdinal(d3.schemeCategory10)
    .domain(nodes);

  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);

  const chords = chord(matrix);

  // Draw ribbons
  g.append("g")
    .attr("fill-opacity", 0.67)
    .selectAll("path")
    .data(chords)
    .join("path")
    .attr("d", ribbon)
    .attr("fill", d => colourScale(nodes[d.source.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.source.index])).darker());

  // Draw groups (arcs)
  const group = g.append("g")
    .selectAll("g")
    .data(chords.groups)
    .join("g");

  group.append("path")
    .attr("d", arc)
    .attr("fill", d => colourScale(nodes[d.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.index])).darker());

  // Add labels
  group.append("text")
    .each(d => { d.angle = (d.startAngle + d.endAngle) / 2; })
    .attr("dy", "0.31em")
    .attr("transform", d => `rotate(${(d.angle * 180 / Math.PI) - 90})translate(${outerRadius + 30})${d.angle > Math.PI ? "rotate(180)" : ""}`)
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
    .text((d, i) => nodes[i])
    .style("font-size", "12px");
}
```

### Heatmap

热力图使用颜色在二维网格中编码数值，有助于展示跨类别的模式：

```javascript
function drawHeatmap(data) {
  // data format: array of objects with row, column, and value
  // Example: [{ row: 'A', column: 'X', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 800;
  const height = 600;
  const margin = { top: 100, right: 30, bottom: 30, left: 100 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // Get unique rows and columns
  const rows = Array.from(new Set(data.map(d => d.row)));
  const columns = Array.from(new Set(data.map(d => d.column)));

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Create scales
  const xScale = d3.scaleBand()
    .domain(columns)
    .range([0, innerWidth])
    .padding(0.01);

  const yScale = d3.scaleBand()
    .domain(rows)
    .range([0, innerHeight])
    .padding(0.01);

  // Colour scale for values
  const colourScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, d3.max(data, d => d.value)]);

  // Draw rectangles
  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.column))
    .attr("y", d => yScale(d.row))
    .attr("width", xScale.bandwidth())
    .attr("height", yScale.bandwidth())
    .attr("fill", d => colourScale(d.value));

  // Add x-axis labels
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(columns)
    .join("text")
    .attr("x", d => xScale(d) + xScale.bandwidth() / 2)
    .attr("y", -10)
    .attr("text-anchor", "middle")
    .text(d => d)
    .style("font-size", "12px");

  // Add y-axis labels
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(rows)
    .join("text")
    .attr("x", -10)
    .attr("y", d => yScale(d) + yScale.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", "end")
    .text(d => d)
    .style("font-size", "12px");

  // Add colour legend
  const legendWidth = 20;
  const legendHeight = 200;
  const legend = svg.append("g")
    .attr("transform", `translate(${width - 60},${margin.top})`);

  const legendScale = d3.scaleLinear()
    .domain(colourScale.domain())
    .range([legendHeight, 0]);

  const legendAxis = d3.axisRight(legendScale)
    .ticks(5);

  // Draw colour gradient in legend
  for (let i = 0; i < legendHeight; i++) {
    legend.append("rect")
      .attr("y", i)
      .attr("width", legendWidth)
      .attr("height", 1)
      .attr("fill", colourScale(legendScale.invert(i)));
  }

  legend.append("g")
    .attr("transform", `translate(${legendWidth},0)`)
    .call(legendAxis);
}
```

### 饼图

```javascript
const pie = d3.pie()
  .value(d => d.value)
  .sort(null);

const arc = d3.arc()
  .innerRadius(0)
  .outerRadius(Math.min(width, height) / 2 - 20);

const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

const g = svg.append("g")
  .attr("transform", `translate(${width / 2},${height / 2})`);

g.selectAll("path")
  .data(pie(data))
  .join("path")
  .attr("d", arc)
  .attr("fill", (d, i) => colourScale(i))
  .attr("stroke", "white")
  .attr("stroke-width", 2);
```

### 力导向网络图

```javascript
const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id).distance(100))
  .force("charge", d3.forceManyBody().strength(-300))
  .force("center", d3.forceCenter(width / 2, height / 2));

const link = g.selectAll("line")
  .data(links)
  .join("line")
  .attr("stroke", "#999")
  .attr("stroke-width", 1);

const node = g.selectAll("circle")
  .data(nodes)
  .join("circle")
  .attr("r", 8)
  .attr("fill", "steelblue")
  .call(d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended));

simulation.on("tick", () => {
  link
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);
  
  node
    .attr("cx", d => d.x)
    .attr("cy", d => d.y);
});

function dragstarted(event) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  event.subject.fx = event.subject.x;
  event.subject.fy = event.subject.y;
}

function dragged(event) {
  event.subject.fx = event.x;
  event.subject.fy = event.y;
}

function dragended(event) {
  if (!event.active) simulation.alphaTarget(0);
  event.subject.fx = null;
  event.subject.fy = null;
}
```

## 添加交互

### 工具提示

```javascript
// 创建工具提示 div（在 SVG 外部）
const tooltip = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("position", "absolute")
  .style("visibility", "hidden")
  .style("background-color", "white")
  .style("border", "1px solid #ddd")
  .style("padding", "10px")
  .style("border-radius", "4px")
  .style("pointer-events", "none");

// 添加到元素
circles
  .on("mouseover", function(event, d) {
    d3.select(this).attr("opacity", 1);
    tooltip
      .style("visibility", "visible")
      .html(`<strong>${d.label}</strong><br/>Value: ${d.value}`);
  })
  .on("mousemove", function(event) {
    tooltip
      .style("top", (event.pageY - 10) + "px")
      .style("left", (event.pageX + 10) + "px");
  })
  .on("mouseout", function() {
    d3.select(this).attr("opacity", 0.7);
    tooltip.style("visibility", "hidden");
  });
```

### 缩放和平移

```javascript
const zoom = d3.zoom()
  .scaleExtent([0.5, 10])
  .on("zoom", (event) => {
    g.attr("transform", event.transform);
  });

svg.call(zoom);
```

### 点击交互

```javascript
circles
  .on("click", function(event, d) {
    // 处理点击（派发事件、更新应用状态等）
    console.log("Clicked:", d);

    // 视觉反馈
    d3.selectAll("circle").attr("fill", "steelblue");
    d3.select(this).attr("fill", "orange");

    // 可选：为框架/应用派发自定义事件
    // window.dispatchEvent(new CustomEvent('chartClick', { detail: d }));
  });
```

## 过渡和动画

为视觉变化添加平滑过渡：

```javascript
// 基础过渡
circles
  .transition()
  .duration(750)
  .attr("r", 10);

// 链式过渡
circles
  .transition()
  .duration(500)
  .attr("fill", "orange")
  .transition()
  .duration(500)
  .attr("r", 15);

// 交错过渡
circles
  .transition()
  .delay((d, i) => i * 50)
  .duration(500)
  .attr("cy", d => yScale(d.value));

// 自定义缓动
circles
  .transition()
  .duration(1000)
  .ease(d3.easeBounceOut)
  .attr("r", 10);
```

## 比例尺参考

### 定量比例尺

```javascript
// Linear scale
const xScale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

// Log scale (for exponential data)
const logScale = d3.scaleLog()
  .domain([1, 1000])
  .range([0, 500]);

// Power scale
const powScale = d3.scalePow()
  .exponent(2)
  .domain([0, 100])
  .range([0, 500]);

// Time scale
const timeScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2024, 0, 1)])
  .range([0, 500]);
```

### 序数比例尺

```javascript
// Band scale (for bar charts)
const bandScale = d3.scaleBand()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400])
  .padding(0.1);

// Point scale (for line/scatter categories)
const pointScale = d3.scalePoint()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400]);

// Ordinal scale (for colours)
const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
```

### 顺序比例尺

```javascript
// Sequential colour scale
const colourScale = d3.scaleSequential(d3.interpolateBlues)
  .domain([0, 100]);

// Diverging colour scale
const divScale = d3.scaleDiverging(d3.interpolateRdBu)
  .domain([-10, 0, 10]);
```

## 最佳实践

### 数据准备

在可视化之前始终验证和准备数据：

```javascript
// Filter invalid values
const cleanData = data.filter(d => d.value != null && !isNaN(d.value));

// Sort data if order matters
const sortedData = [...data].sort((a, b) => b.value - a.value);

// Parse dates
const parsedData = data.map(d => ({
  ...d,
  date: d3.timeParse("%Y-%m-%d")(d.date)
}));
```

### 性能优化

对于大数据集（超过1000个元素）：

```javascript
// Use canvas instead of SVG for many elements
// Use quadtree for collision detection
// Simplify paths with d3.line().curve(d3.curveStep)
// Implement virtual scrolling for large lists
// Use requestAnimationFrame for custom animations
```

### 无障碍访问

让可视化具有无障碍性：

```javascript
// Add ARIA labels
svg.attr("role", "img")
   .attr("aria-label", "Bar chart showing quarterly revenue");

// Add title and description
svg.append("title").text("Quarterly Revenue 2024");
svg.append("desc").text("Bar chart showing revenue growth across four quarters");

// Ensure sufficient colour contrast
// Provide keyboard navigation for interactive elements
// Include data table alternative
```

### 样式设计

使用一致、专业的样式：

```javascript
// Define colour palettes upfront
const colours = {
  primary: '#4A90E2',
  secondary: '#7B68EE',
  background: '#F5F7FA',
  text: '#333333',
  gridLines: '#E0E0E0'
};

// Apply consistent typography
svg.selectAll("text")
  .style("font-family", "Inter, sans-serif")
  .style("font-size", "12px");

// Use subtle grid lines
g.selectAll(".tick line")
  .attr("stroke", colours.gridLines)
  .attr("stroke-dasharray", "2,2");
```

## 常见问题与解决方案

**问题**：坐标轴不显示
- 确保比例尺有有效的定义域（检查 NaN 值）
- 确认坐标轴已添加到正确的组
- 检查 transform 平移是否正确

**问题**：过渡动画不工作
- 在属性变化前调用 `.transition()`
- 确保元素具有唯一键以实现正确的数据绑定
- 检查 useEffect 的依赖项是否包含所有变化的数据

**问题**：响应式尺寸无效
- 使用 ResizeObserver 或窗口 resize 监听器
- 更新状态中的尺寸以触发重新渲染
- 确保 SVG 具有 width/height 属性或 viewBox

**问题**：性能问题
- 限制 DOM 元素数量（超过1000个项考虑使用 canvas）
- 对 resize 处理函数进行防抖
- 使用 `.join()` 替代独立的 enter/update/exit 选择
- 通过检查依赖避免不必要的重新渲染

## 资源

### references/
包含详细的参考资料：
- `d3-patterns.md` - 可视化模式和代码示例的全面集合
- `scale-reference.md` - D3 比例尺完整指南及示例
- `colour-schemes.md` - D3 配色方案和调色板推荐

### assets/

包含样板模板：

- `chart-template.js` - 基础图表的起始模板
- `interactive-template.js` - 带工具提示、缩放和交互的模板
- `sample-data.json` - 用于测试的示例数据集

这些模板适用于原生 JavaScript、React、Vue、Svelte 或任何其他 JavaScript 环境。根据您的特定框架需要进行调整。

要使用这些资源，在需要特定可视化类型或模式的详细指导时，请阅读相关文件。
