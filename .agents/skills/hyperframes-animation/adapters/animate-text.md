# 文本特效 — 参考

关于确定性文本动画规范（例如，`typewriter` 以精确的 `240ms / 46ms stagger / steps(1, end) easing` 参数），此技能委托给 Pixel Point 维护的独立 **`animate-text`** 技能，地址为 [github.com/pixel-point/animate-text](https://github.com/pixel-point/animate-text)。它提供了 24 个命名文本特效的目录，包含可移植的约定和按库分类的实现方案（GSAP、Anime.js、WAAPI）。

**我们不会将此目录内置到本仓库中。** Pixel Point 的 `animate-text` 是真相源；在此处打包其文件会违反上游的许可（截至目前上游未声明明确许可）。单独加载该技能能在保持法律清晰的同时为你提供相同的目录。

## 如何使用

当一个节拍需要确定性文本动画时，将上游技能与本技能一起加载：

```bash
# 在你的项目根目录中，将上游技能安装到 .agents/skills/
npx skills add pixel-point/animate-text
```

或者在技能感知的代理运行时中，通过名称调用技能：

```
/animate-text
```

安装后，规范位于：

```
.agents/skills/animate-text/assets/effects/<id>.json   # 按库的实现方案
.agents/skills/animate-text/assets/specs/<id>.json     # 可移植的运动约定
```

读取这些文件的子代理将获得精确的 GSAP 时序、缓动字符串、DOM 分割规则和错开算法——无需创造性发明。

## 何时不需要上游技能

如果节拍的文本动画简单到可以用文字描述（"标题逐词淡入，80ms 错开"），则使用这些技能中已有的 GSAP 知识内联实现（`hyperframes-creative` → `references/motion-principles.md` 和 `references/beat-direction.md`；`hyperframes-animation` → `techniques.md`，条目 #4 "逐词动能排版"）。上游目录在以下情况下最有价值：

- 你希望在多个节拍中使用特定的**命名**特效（因此它们感觉像一个设计系统，而非一次性作品）
- 你在几个类似特效之间选择（打字机 vs 逐字上升 vs 自下而上字母）并希望在一个地方查看所有 24 个
- 你需要布局感知的特效（`kinetic-center-build`、`short-slide-right`、`short-slide-down`），仅靠参数不足以描述——这些带有自定义布局算法

## 特效名称 — 词汇表（不要将其用作实现来源）

为方便编写故事板时使用：上游技能提供了 24 个特效。它们的 ID 列在此处，以便你即使在加载上游技能之前也能在 `STORYBOARD.md` 中引用它们。**实现规范在上游技能中，不在此处。**

- **按字符 (7)：** soft-blur-in、per-character-rise、typewriter、bottom-up-letters、top-down-letters、stagger-from-center、stagger-from-edges
- **按单词 (8)：** per-word-crossfade、spring-scale-in、shared-axis-y、blur-out-up、kinetic-center-build、short-slide-right、short-slide-down、depth-parallax-words
- **按行 (2)：** mask-reveal-up、line-by-line-slide
- **整个元素 (7)：** micro-scale-fade、shimmer-sweep、fade-through、shared-axis-z、scale-down-fade、focus-blur-resolve、shared-axis-x

关于描述、时长、缓动曲线和按库的方案：加载 `/animate-text` 并阅读其自己的目录页面。

## 在故事板中

每个节拍中的每个文本元素都可以通过 ID 命名一个特效，例如：

```markdown
**文本动画：**

- 主标题：`kinetic-center-build`
- 眉标：`soft-blur-in`
- 正文 3 行：`mask-reveal-up`
```

实现该节拍的子代理将加载 `/animate-text`（如果尚未加载），然后从上游技能的文件中读取每个命名特效的规范。

如果上游技能不可用（离线构建、网络限制、不支持技能加载的代理运行时），子代理将仅根据描述回退实现特效——使用 GSAP 知识加上特效 ID 作为意图描述（例如，"typewriter" = 逐字符阶梯揭示，无插值）。
