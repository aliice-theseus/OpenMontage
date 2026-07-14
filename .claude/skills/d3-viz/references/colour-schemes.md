# D3.js 配色方案与调色板推荐

使用 d3.js 进行数据可视化时颜色选择的全面指南。

## 内置分类配色方案

### Category10（默认）

```javascript
d3.schemeCategory10
// ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
//  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
```

**特点：**
- 10 种不同颜色
- 良好的色盲无障碍性
- 大多数分类数据的默认选择
- 饱和度和亮度均衡

**适用场景：** 通用分类编码、图例项、多数据系列

### Tableau10

```javascript
d3.schemeTableau10
```

**特点：**
- 10 种针对数据可视化优化的颜色
- 专业外观
- 极佳的可区分性

**适用场景：** 商业仪表盘、专业报告、演示文稿

### Accent

```javascript
d3.schemeAccent
// 8 种高饱和度颜色
```

**特点：**
- 明亮鲜艳的颜色
- 高对比度
- 现代美学

**适用场景：** 突出重要类别、现代 Web 应用

### Dark2

```javascript
d3.schemeDark2
// 8 种较暗、柔和的颜色
```

**特点：**
- 柔和的调色板
- 专业外观
- 适合深色背景

**适用场景：** 深色模式可视化、专业场景

### Paired

```javascript
d3.schemePaired
// 12 种颜色，成对相似色调
```

**特点：**
- 浅色和深色变体配对
- 适用于嵌套类别
- 12 种不同颜色

**适用场景：** 分组柱状图、分层类别、前后对比

### Pastel1 和 Pastel2

```javascript
d3.schemePastel1 // 9 种颜色
d3.schemePastel2 // 8 种颜色
```

**特点：**
- 柔和、低饱和度颜色
- 温和外观
- 适合大面积使用

**适用场景：** 背景颜色、细微分类、舒缓的可视化

### Set1、Set2、Set3

```javascript
d3.schemeSet1 // 9 种颜色 - 鲜艳
d3.schemeSet2 // 8 种颜色 - 柔和
d3.schemeSet3 // 12 种颜色 - 粉彩
```

**特点：**
- Set1：高饱和度，最大区分度
- Set2：专业、均衡
- Set3：微妙、多种类

**适用场景：** 根据视觉层次需求而变化

## 顺序配色方案

顺序方案使用单一色相或渐变将连续数据从低值映射到高值。

### 单色相顺序

**Blues（蓝色系）：**
```javascript
d3.interpolateBlues
d3.schemeBlues[9] // 9 级离散版本
```

**其他单色相选项：**
- `d3.interpolateGreens` / `d3.schemeGreens`
- `d3.interpolateOranges` / `d3.schemeOranges`
- `d3.interpolatePurples` / `d3.schemePurples`
- `d3.interpolateReds` / `d3.schemeReds`
- `d3.interpolateGreys` / `d3.schemeGreys`

**适用场景：**
- 简单热力图
- 等值线图
- 密度图
- 单一指标可视化

### 多色相顺序

**Viridis（推荐）：**
```javascript
d3.interpolateViridis
```

**特点：**
- 感知均匀
- 色盲友好
- 打印安全
- 无视觉死区
- 感知亮度单调递增

**其他感知均匀选项：**
- `d3.interpolatePlasma` - 紫色到黄色
- `d3.interpolateInferno` - 黑色到白色（经过红/橙）
- `d3.interpolateMagma` - 黑色到白色（经过紫色）
- `d3.interpolateCividis` - 色盲优化

**色盲无障碍：**
```javascript
d3.interpolateTurbo // 类彩虹但感知均匀
d3.interpolateCool  // 青色到洋红色
d3.interpolateWarm  // 橙色到黄色
```

**适用场景：**
- 科学可视化
- 医学影像
- 任何高精度数据可视化
- 无障碍可视化

### 传统顺序

**黄-橙-红：**
```javascript
d3.interpolateYlOrRd
d3.schemeYlOrRd[9]
```

**黄-绿-蓝：**
```javascript
d3.interpolateYlGnBu
d3.schemeYlGnBu[9]
```

**其他多色相选项：**
- `d3.interpolateBuGn` - 蓝色到绿色
- `d3.interpolateBuPu` - 蓝色到紫色
- `d3.interpolateGnBu` - 绿色到蓝色
- `d3.interpolateOrRd` - 橙色到红色
- `d3.interpolatePuBu` - 紫色到蓝色
- `d3.interpolatePuBuGn` - 紫色到蓝绿色
- `d3.interpolatePuRd` - 紫色到红色
- `d3.interpolateRdPu` - 红色到紫色
- `d3.interpolateYlGn` - 黄色到绿色
- `d3.interpolateYlOrBr` - 黄色到橙棕色

**适用场景：** 传统数据可视化、熟悉的颜色关联（温度、植被、水域）

## 发散配色方案

发散方案使用两种不同的色相突出显示与中心值的偏差。

### 红-蓝（温度）

```javascript
d3.interpolateRdBu
d3.schemeRdBu[11]
```

**特点：**
- 直观的温度隐喻
- 强烈对比
- 清晰的正/负区分

**适用场景：** 温度、利润/亏损、高于/低于平均水平、相关性

### 红-黄-蓝

```javascript
d3.interpolateRdYlBu
d3.schemeRdYlBu[11]
```

**特点：**
- 三色渐变
- 通过黄色实现更柔和的过渡
- 更多视觉层次

**适用场景：** 需要强调极值且中间值需要可见性时

### 其他发散方案

**交通灯：**
```javascript
d3.interpolateRdYlGn // 红色（差）到绿色（好）
```

**光谱（彩虹）：**
```javascript
d3.interpolateSpectral // 全光谱
```

**其他选项：**
- `d3.interpolateBrBG` - 棕色到蓝绿色
- `d3.interpolatePiYG` - 粉色到黄绿色
- `d3.interpolatePRGn` - 紫色到绿色
- `d3.interpolatePuOr` - 紫色到橙色
- `d3.interpolateRdGy` - 红色到灰色

**适用场景：** 根据语义含义和无障碍需求选择

## 色盲友好调色板

### 通用指南

1. **避免红绿组合**（最常见的色盲类型）
2. **使用蓝橙发散**替代红绿
3. **添加纹理或图案**作为冗余编码
4. **使用模拟工具测试**

### 推荐色盲安全方案

**分类：**
```javascript
// Okabe-Ito 调色板（色盲安全）
const okabePalette = [
  '#E69F00', // 橙色
  '#56B4E9', // 天蓝色
  '#009E73', // 蓝绿色
  '#F0E442', // 黄色
  '#0072B2', // 蓝色
  '#D55E00', // 朱红色
  '#CC79A7', // 红紫色
  '#000000'  // 黑色
];

const colourScale = d3.scaleOrdinal()
  .domain(categories)
  .range(okabePalette);
```

**顺序：**
```javascript
// 使用 Viridis、Cividis 或 Blues
d3.interpolateViridis  // 整体最佳
d3.interpolateCividis  // 针对 CVD 优化
d3.interpolateBlues    // 简单安全
```

**发散：**
```javascript
// 使用蓝橙替代红绿
d3.interpolateBrBG
d3.interpolatePuOr
```

## 自定义调色板

### 创建自定义顺序

```javascript
const customSequential = d3.scaleLinear()
  .domain([0, 100])
  .range(['#e8f4f8', '#006d9c']) // 浅蓝到深蓝
  .interpolate(d3.interpolateLab); // 感知均匀
```

### 创建自定义发散

```javascript
const customDiverging = d3.scaleLinear()
  .domain([0, 50, 100])
  .range(['#ca0020', '#f7f7f7', '#0571b0']) // 红、灰、蓝
  .interpolate(d3.interpolateLab);
```

### 创建自定义分类

```javascript
// 品牌颜色
const brandPalette = [
  '#FF6B6B', // 主红色
  '#4ECDC4', // 辅助青色
  '#45B7D1', // 第三蓝色
  '#FFA07A', // 强调珊瑚色
  '#98D8C8'  // 强调薄荷色
];

const colourScale = d3.scaleOrdinal()
  .domain(categories)
  .range(brandPalette);
```

## 语义颜色关联

### 通用颜色含义

**红色：**
- 危险、错误、负面
- 高温
- 负债、亏损

**绿色：**
- 成功、正面
- 增长、植被
- 利润、收益

**蓝色：**
- 信任、冷静
- 水、寒冷
- 信息、中性

**黄色/橙色：**
- 警告、谨慎
- 能量、温暖
- 注意力

**灰色：**
- 中性、非活跃
- 缺失数据
- 背景

### 上下文相关调色板

**金融：**
```javascript
const financialColours = {
  profit: '#27ae60',
  loss: '#e74c3c',
  neutral: '#95a5a6',
  highlight: '#3498db'
};
```

**温度：**
```javascript
const temperatureScale = d3.scaleSequential(d3.interpolateRdYlBu)
  .domain([40, -10]); // 热到冷（反转）
```

**交通/状态：**
```javascript
const statusColours = {
  success: '#27ae60',
  warning: '#f39c12',
  error: '#e74c3c',
  info: '#3498db',
  neutral: '#95a5a6'
};
```

## 无障碍最佳实践

### 对比度比例

确保颜色和背景之间有足够的对比度：

```javascript
// 良好对比度示例
const highContrast = {
  background: '#ffffff',
  text: '#2c3e50',
  primary: '#3498db',
  secondary: '#e74c3c'
};
```

**WCAG 指南：**
- 普通文本：最小 4.5:1
- 大号文本：最小 3:1
- UI 组件：最小 3:1

### 冗余编码

永远不要仅依赖颜色来传达信息：

```javascript
// 添加图案或形状
const symbols = ['circle', 'square', 'triangle', 'diamond'];

// 添加文本标签
// 使用线型（实线、虚线、点线）
// 使用尺寸编码
```

### 测试

测试可视化是否存在色盲问题：
- Chrome DevTools（渲染 > 模拟视觉缺陷）
- Colour Oracle（免费桌面应用）
- Coblis（在线模拟器）

## 专业颜色推荐

### 数据新闻

```javascript
// Guardian 风格
const guardianPalette = [
  '#005689', // 卫报蓝
  '#c70000', // 卫报红
  '#7d0068', // 卫报粉
  '#951c75', // 卫报紫
];

// FT 风格
const ftPalette = [
  '#0f5499', // FT 蓝
  '#990f3d', // FT 红
  '#593380', // FT 紫
  '#262a33', // FT 黑
];
```

### 学术/科学

```javascript
// Nature 期刊风格
const naturePalette = [
  '#0071b2', // 蓝色
  '#d55e00', // 朱红色
  '#009e73', // 绿色
  '#f0e442', // 黄色
];

// 连续数据使用 Viridis
const scientificScale = d3.scaleSequential(d3.interpolateViridis);
```

### 企业/商业

```javascript
// 专业、保守
const corporatePalette = [
  '#003f5c', // 深蓝
  '#58508d', // 紫色
  '#bc5090', // 洋红色
  '#ff6361', // 珊瑚色
  '#ffa600'  // 橙色
];
```

## 动态颜色选择

### 基于数据范围

```javascript
function selectColourScheme(data) {
  const extent = d3.extent(data);
  const hasNegative = extent[0] < 0;
  const hasPositive = extent[1] > 0;

  if (hasNegative && hasPositive) {
    // 发散：数据跨越零
    return d3.scaleSequentialSymlog(d3.interpolateRdBu)
      .domain([extent[0], 0, extent[1]]);
  } else {
    // 顺序：全正或全负
    return d3.scaleSequential(d3.interpolateViridis)
      .domain(extent);
  }
}
```

### 基于类别数量

```javascript
function selectCategoricalScheme(categories) {
  const n = categories.length;

  if (n <= 10) {
    return d3.scaleOrdinal(d3.schemeTableau10);
  } else if (n <= 12) {
    return d3.scaleOrdinal(d3.schemePaired);
  } else {
    // 对于多种类，使用带 quantize 的顺序方案
    return d3.scaleQuantize()
      .domain([0, n - 1])
      .range(d3.quantize(d3.interpolateRainbow, n));
  }
}
```

## 常见颜色错误避免

1. **对顺序数据使用彩虹渐变**
   - 问题：感知不均匀，难以阅读
   - 解决：使用 Viridis、Blues 或其他均匀方案

2. **红绿用于发散（色盲问题）**
   - 问题：8% 的男性无法区分
   - 解决：使用蓝橙或紫绿

3. **过多分类颜色**
   - 问题：难以区分和记忆
   - 解决：限制在 5-8 个类别，使用分组

4. **对比度不足**
   - 问题：可读性差
   - 解决：测试对比度比例，在浅色背景上使用更深颜色

5. **文化不一致的颜色**
   - 问题：语义含义混淆
   - 解决：研究目标受众的颜色关联

6. **温度比例反转**
   - 问题：反直觉（红=冷）
   - 解决：红/橙=热，蓝=冷

## 快速参考指南

**需要展示...**

- **类别（≤10）：** `d3.schemeCategory10` 或 `d3.schemeTableau10`
- **类别（>10）：** `d3.schemePaired` 或分组类别
- **顺序（通用）：** `d3.interpolateViridis`
- **顺序（科学）：** `d3.interpolateViridis` 或 `d3.interpolatePlasma`
- **顺序（温度）：** `d3.interpolateRdYlBu`（反转）
- **发散（零中心）：** `d3.interpolateRdBu` 或 `d3.interpolateBrBG`
- **发散（好/坏）：** `d3.interpolateRdYlGn`（反转）
- **色盲安全（分类）：** Okabe-Ito 调色板（如上所示）
- **色盲安全（顺序）：** `d3.interpolateCividis` 或 `d3.interpolateBlues`
- **色盲安全（发散）：** `d3.interpolatePuOr` 或 `d3.interpolateBrBG`

**始终记住：**
1. 测试色盲问题
2. 确保足够的对比度
3. 合理使用语义颜色
4. 添加冗余编码（图案、标签）
5. 保持简洁（颜色越少，可视化越清晰）
