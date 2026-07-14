# stat — 类别模块

单个**主角数字**揭示。无资产（"输入"就是数字）。约4–6秒。

## 规划（Director）

`content`：`{ value, prefix ($), suffix (% / x / K-M-B), label, ring: bool }`。概要：粗体显示字体、克制调色板 + 一个强调色。

## 词汇表 / 依赖

- 块：**`apple-money-count`**（金融风格：$计数器 + 绿色闪光 + 金钱爆发 + 音效）适合时使用；否则手动编写。
- 规则：`hyperframes-animation/rules/{counting-dynamic-scale, stat-bars-and-fills}`。
- 原语：`count_up`（里程表）· `scale_pop` · `ring_fill`（弧线）· `label_stagger`（在数值之后）· `hold`。

## 构建（优先复用）

复用 `apple-money-count` + 设置目标值/前缀/后缀/标签/调色板；**或**根据已验证的原型 `v0-stat-motion-demo` 手动编写：

- **计数由时间线驱动** — 补间代理对象 `{v:0}→target` 通过 `onUpdate` 写入格式化数字（seek 安全；绝不用 setInterval/时钟）。
- `font-variant-numeric: tabular-nums`；减速缓动；约1.2–1.6秒然后**保持**最终值。
- 环形/弧线通过 `stroke-dashoffset`，与计数同步完成；标签在数字落地**之后**淡入（数值 → 含义）。
