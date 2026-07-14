# kinetic-type — 类别模块

文字是主角；排版 + 动态承载信息。通常无资产（`asset_needs: []`）。

## 规划（Director）

- **先定风格。** 如果项目有 **`design.md`/`frame.md`**（优先级：`frame.md` → `design.md` → `DESIGN.md`），读取它并使用其**精确的调色板/字体/约束** — 不要自行发明。无规格 → 选择一个命名风格，或询问：氛围 + 亮色/暗色 + 任何品牌颜色/字体。（风格是案例必须练习的输入；同一个镜头在两个不同的 `design.md` 下应看起来不同。）
- 按含义/换气将文案分割成场景（英文约3–7个词；中文约4–12个字）。标记每个场景 **钩子 → 构建 → 重击 → 收束**。
- 每场景1–2个 `emphasis_words`。每场景：`emotion` + `motion`（自由形式）+ `beats`。

## 词汇表

动态原语 + 注册表块：**`references/motion-vocabulary.md`**（slide / scale / fade / blur / typewriter / word_reveal / wave / bounce / slam / scale_pulse / shake / glow / color_shift，加上18个 `caption-*` 块）。

## 构建（优先复用）

- 当有合适的 **`caption-*` 块**时优先使用（`caption-kinetic-slam`/`caption-editorial-emphasis`/…）：`npx hyperframes add` + 设置文字/`emphasis_words`/调色板/字体。
- 否则手动编写：一个全时长的 `.clip`；每场景一个 `.group`（flex 居中）；文字作为 span；按场景 `motion` 确定的 `gsap.from()` 入场；强调词 → 在节拍上 `glow`/`scale_pulse`；**seek 安全揭示**（`autoAlpha`）。遵守 `references/builder-contract.md`。
- 参考实现：原型 `v0-text-motion-demo` + `pipeline-demo`。
