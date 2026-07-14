# D3.js 颜色方案与调色板推荐

d3.js 数据可视化中颜色选择的全面指南。

## 内置分类颜色方案

### Category10（默认）

```javascript
d3.schemeCategory10
// ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
//  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
```

**特性：**
- 10 种不同颜色
- 良好的色盲可访问性
- 大多数分类数据的默认选择
- 平衡的饱和度和亮度

**用例：** 通用分类编码、图例项、多数据系列

### Tableau10

```javascript
d3.schemeTableau10
```

**特性：**
- 10 种为数据可视化优化的颜色
- 专业外观
- 出色的可区分性

**用例：** 商业仪表板、专业报告、演示文稿

### Accent

```javascript
d3.schemeAccent
// 8 种高饱和度颜色
```

**特性：**
- 明亮、鲜艳的颜色
- 高对比度
- 现代美学

**用例：** 突出重要类别、现代 Web 应用

### Dark2

```javascript
d3.schemeDark2
// 8 种较深、柔和的颜色
```

**特性：**
- 柔和的调色板
- 专业外观
- 适合深色背景

**用例：** 深色模式可视化、专业场景

### Paired

```javascript
d3.schemePaired
// 12 种颜色，以相似色调成对
```

**特性：**
- 浅色和深色变体的配对
- 适用于嵌套类别
- 12 种不同颜色

**用例：** 分组条形图、分层类别、之前/之后比较

### Pastel1 和 Pastel2

```javascript
d3.schemePastel1 // 9 种颜色
d3.schemePastel2 // 8 种颜色
```

**特性：**
- 柔和、低饱和度颜色
- 温和外观
- 适合大区域

**用例：** 背景颜色、微妙分类、令人平静的可视化

### Set1、Set2、Set3

```javascript
d3.schemeSet1 // 9 种颜色 - 鲜艳
d3.schemeSet2 // 8 种颜色 - 柔和
d3.schemeSet3 // 12 种颜色 - 粉彩
```

**特性：**
- Set1：高饱和度，最大区分度
- Set2：专业、平衡
- Set3：微妙、多类别

**用例：** 根据视觉层次需求变化

## 序列颜色方案

序列方案使用单色或渐变将连续数据从低到高值映射。

### 单色序列

**Blues：**
```javascript
d3.interpolateBlues
d3.schemeBlues[9] // 9 步离散版本
```

**其他单色选项：**
- `d3.interpolateGreens` / `d3.schemeGreens`
- `d3.interpolateOranges` / `d3.schemeOranges`
- `d3.interpolatePurples` / `d3.schemePurples`
- `d3.interpolateReds` / `d3.schemeReds`
- `d3.interpolateGreys` / `d3.schemeGreys`

**用例：**
- 简单热图
- 分区统计图
- 密度图
- 单指标可视化

### 多色序列

**Viridis（推荐）：**
```javascript
d3.interpolateViridis
```

**特性：**
- 感知均匀
- 色盲友好
- 打印安全
- 无视觉死区
- 感知亮度单调递增

**其他感知均匀选项：**
- `d3.interpolatePlasma` - 紫到黄
- `d3.interpolateInferno` - 黑到白通过红/橙
- `d3.interpolateMagma` - 黑到白通过紫
- `d3.interpolateCividis` - 色盲优化

**色盲可访问：**
```javascript
d3.interpolateTurbo // 类似彩虹但感知均匀
d3.interpolateCool  // 青到品红
d3.interpolateWarm  // 橙到黄
```

**用例：**
- 科学可视化
- 医学影像
- 任何高精度数据可视化
- 可访问可视化

### 传统序列

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

**其他多色：**
- `d3.interpolateBuGn` - 蓝到绿
- `d3.interpolateBuPu` - 蓝到紫
- `d3.interpolateGnBu` - 绿到蓝
- `d3.interpolateOrRd` - 橙到红
- `d3.interpolatePuBu` - 紫到蓝
- `d3.interpolatePuBuGn` - 紫到蓝绿
- `d3.interpolatePuRd` - 紫到红
- `d3.interpolateRdPu` - 红到紫
- `d3.interpolateYlGn` - 黄到绿
- `d3.interpolateYlOrBr` - 黄到橙棕

**用例：** 传统数据可视化、熟悉颜色关联（温度、植被、水）

## 发散颜色方案

发散方案使用两种不同色相突出与中心值的偏差。

### 红-蓝（温度）

```javascript
d3.interpolateRdBu
d3.schemeRdBu[11]
```

**特性：**
- 直观的温度隐喻
- 强对比度
- 清晰的正/负区分

**用例：** 温度、利润/亏损、高于/低于平均值、相关性

### 红-黄-蓝

```javascript
d3.interpolateRdYlBu
d3.schemeRdYlBu[11]
```

**特性：**
- 三色渐变
- 通过黄色更柔和的过渡
- 更多视觉步骤

**用例：** 当极端值需要强调且中间值需要可见性

### 其他发散方案

**交通灯：**
```javascript
d3.interpolateRdYlGn // 红（坏）到绿（好）
```

**光谱（彩虹）：**
```javascript
d3.interpolateSpectral // 全光谱
```

**其他选项：**
- `d3.interpolateBrBG` - 棕到蓝绿
- `d3.interpolatePiYG` - 粉到黄绿
- `d3.interpolatePRGn` - 紫到绿
- `d3.interpolatePuOr` - 紫到橙
- `d3.interpolateRdGy` - 红到灰

**用例：** 根据语义含义和可访问性需求选择

## 色盲友好调色板

### 通用指南

1. **避免红绿组合**（最常见的色盲类型）
2. **使用蓝橙发散**代替红绿
3. **添加纹理或图案**作为冗余编码
4. **使用模拟工具测试**

### 推荐色盲安全方案

**分类：**
```javascript
// Okabe-Ito 调色板（色盲安全）
const okabePalette = [
  '#E69F00', // 橙
  '#56B4E9', // 天蓝
  '#009E73', // 蓝绿
  '#F0E442', // 黄
  '#0072B2', // 蓝
  '#D55E00', // 朱红
  '#CC79A7', // 红紫
  '#000000'  // 黑
];

const colourScale = d3.scaleOrdinal()
  .domain(categories)
  .range(okabePalette);
```

**序列：**
```javascript
// 使用 Viridis、Cividis 或 Blues
d3.interpolateViridis  // 总体最佳
d3.interpolateCividis  // 为 CVD 优化
d3.interpolateBlues    // 简单、安全
```

**发散：**
```javascript
// 使用蓝橙代替红绿
d3.interpolateBrBG
d3.interpolatePuOr
```

## 自定义调色板

### 创建自定义序列

```javascript
const customSequential = d3.scaleLinear()
  .domain([0, 100])
  .range(['#e8f4f8', '#006d9c']) // 浅到深蓝
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
// 品牌色
const brandPalette = [
  '#FF6B6B', // 主红
  '#4ECDC4', // 次青
  '#45B7D1', // 第三蓝
  '#FFA07A', // 强调珊瑚
  '#98D8C8'  // 强调薄荷
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
- 债务、亏损

**绿色：**
- 成功、积极
- 生长、植被
- 利润、收益

**蓝色：**
- 信任、平静
- 水、寒冷
- 信息、中性

**黄色/橙色：**
- 警告、谨慎
- 能量、温暖
- 注意

**灰色：**
- 中性、非活跃
- 缺失数据
- 背景

### 上下文特定调色板

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

## 可访问性最佳实践

### 对比度比率

确保颜色与背景之间的充分对比：

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
- 普通文本：最低 4.5:1
- 大号文本：最低 3:1
- UI 组件：最低 3:1

### 冗余编码

永远不要仅依赖颜色传达信息：

```javascript
// 添加图案或形状
const symbols = ['circle', 'square', 'triangle', 'diamond'];

// 添加文本标签
// 使用线条样式（实线、虚线、点线）
// 使用大小编码
```

### 测试

测试可视化的色盲友好性：
- Chrome DevTools（渲染 > 模拟视觉缺陷）
- Color Oracle（免费桌面应用）
- Coblis（在线模拟器）

## 专业颜色推荐

### 数据新闻

```javascript
// Guardian 风格
const guardianPalette = [
  '#005689', // Guardian 蓝
  '#c70000', // Guardian 红
  '#7d0068', // Guardian 粉
  '#951c75', // Guardian 紫
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
  '#0071b2', // 蓝
  '#d55e00', // 朱红
  '#009e73', // 绿
  '#f0e442', // 黄
];

// 连续数据使用 Viridis
const scientificScale = d3.scaleSequential(d3.interpolateViridis);
```

### 企业/商业

```javascript
// 专业、保守
const corporatePalette = [
  '#003f5c', // 深蓝
  '#58508d', // 紫
  '#bc5090', // 品红
  '#ff6361', // 珊瑚
  '#ffa600'  // 橙
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
    // 序列：全正或全负
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
    // 对于多类别，使用带量化的序列
    return d3.scaleQuantize()
      .domain([0, n - 1])
      .range(d3.quantize(d3.interpolateRainbow, n));
  }
}
```

## 应避免的常见颜色错误

1. **连续数据使用彩虹渐变**
   - 问题：非感知均匀，难以阅读
   - 解决方案：使用 Viridis、Blues 或其他均匀方案

2. **发散使用红绿（色盲）**
   - 问题：8% 的男性无法区分
   - 解决方案：使用蓝橙或紫绿

3. **过多分类颜色**
   - 问题：难以区分和记忆
   - 解决方案：限制在 5-8 个类别，使用分组

4. **对比度不足**
   - 问题：可读性差
   - 解决方案：测试对比度比率，在浅色背景上使用深色

5. **文化不一致的颜色**
   - 问题：语义含义混淆
   - 解决方案：研究目标受众的颜色关联

6. **颠倒的温度标尺**
   - 问题：反直觉（红 = 冷）
   - 解决方案：红/橙 = 热，蓝 = 冷

## 快速参考指南

**需要展示……**

- **类别（≤10）：** `d3.schemeCategory10` 或 `d3.schemeTableau10`
- **类别（>10）：** `d3.schemePaired` 或分组类别
- **序列（通用）：** `d3.interpolateViridis`
- **序列（科学）：** `d3.interpolateViridis` 或 `d3.interpolatePlasma`
- **序列（温度）：** `d3.interpolateRdYlBu`（反转）
- **发散（零）：** `d3.interpolateRdBu` 或 `d3.interpolateBrBG`
- **发散（好/坏）：** `d3.interpolateRdYlGn`（反转）
- **色盲安全（分类）：** Okabe-Ito 调色板（上面已显示）
- **色盲安全（序列）：** `d3.interpolateCividis` 或 `d3.interpolateBlues`
- **色盲安全（发散）：** `d3.interpolatePuOr` 或 `d3.interpolateBrBG`

**始终记住：**
1. 测试色盲友好性
2. 确保足够对比度
3. 适当使用语义颜色
4. 添加冗余编码（图案、标签）
5. 保持简单（更少的颜色 = 更清晰的可视化）
