# 排版

编译器**预捆绑了一组固定**的字体（下表）——在 `font-family` 中写入这些字体家族之一，它就能确定性、离线地渲染，无需设置且无警告。如果使用该集合**之外**的名称，**不会静默丢弃**：如果它是一个真正的 Google 字体，编译器会在**构建时**从 Google Fonts 获取并嵌入它，因此它_确实_会渲染——但这条隐式路径 (a) 会触发 `font_family_without_font_face` 的 lint 警告，(b) 在**分布式/云端渲染中会失败关闭**——如果 Google 不可达，渲染会_报错_，而不是静默替换为系统字体。除此之外，**本地渲染会自动捕获你实际拥有的字体**：你机器上安装的字体家族、本地 `@font-face` 路径或外部 CDN 样式表都会在构建时压缩为 woff2 并内联。所以一个**既不**在捆绑中**也不**在 Google Fonts 中的名称，仅当它_同时_未在本地安装且未在 `@font-face` 中声明时，才会真正回退到通用系统字体——即便如此也会记录编译警告。**一个注意事项**：分布式/云端（Lambda）渲染禁用系统字体捕获，因此不要依赖仅本地安装的字体。所以不要假设未捆绑的显示名称就能直接工作：对于任何必须可预测渲染的内容，请选择以下捆绑家族**或嵌入你自己的 `@font-face`**（参见"寻找字体"）。

## 目录

- 可嵌入的字体（自动解析）
- 禁用字体
- 护栏规则
- 未经指示不得做的事
- 寻找字体
- 选择思维
- 相似字体搭配
- 深色背景
- 用于数据的 OpenType 特性

## 可嵌入的字体（自动解析）

以下 **18 个家族**是渲染器**预捆绑**的——嵌入为本地 data URI，无需网络获取，因此它们离线且确定性地渲染，零设置，无 lint 警告，无失败关闭的获取风险。将它们中的任何一个作为 `font-family` 写入，它就会渲染；**只存在列出的字重**（请求一个家族不提供的字重会得到合成/回退字重，而不是真实切口）。（任何_其他_真正的 Google 字体仍然通过介绍中描述的隐式构建时获取工作——但只有这些字体渲染时没有任何那些注意事项。）

| 家族              | 字重             | 角色                |
| ----------------- | --------------- | ------------------- |
| Inter             | 400 · 700 · 900 | 无衬线（正文/UI）     |
| Roboto            | 400 · 700 · 900 | 无衬线               |
| Open Sans         | 400 · 700       | 无衬线               |
| Lato              | 400 · 700 · 900 | 无衬线               |
| Nunito            | 400 · 700 · 900 | 无衬线（圆角）        |
| Montserrat        | 400 · 700 · 900 | 几何无衬线            |
| Poppins           | 400 · 700 · 900 | 几何无衬线            |
| Outfit            | 400 · 700 · 900 | 几何无衬线            |
| Oswald            | 400 · 700       | 紧缩无衬线            |
| **League Gothic** | **仅 400**      | 紧缩展示              |
| **Archivo Black** | **仅 400**      | 粗重展示              |
| Playfair Display  | 400 · 700 · 900 | 衬线（展示）          |
| EB Garamond       | 400 · 700       | 衬线（正文）          |
| Space Mono        | 400 · 700       | 等宽                 |
| IBM Plex Mono     | 400 · 700       | 等宽                 |
| JetBrains Mono    | 400 · 700       | 等宽                 |
| Source Code Pro   | 400 · 700       | 等宽                 |
| Noto Sans JP      | 400 · 700       | CJK（日文）           |

> ⚠ **League Gothic 和 Archivo Black 仅提供 400 字重**——它们本身就是粗重/紧缩的展示字体。不要对它们请求 `font-weight: 700/900`。

**别名**——这些常用名称解析为嵌入家族，因此你可以安全地使用它们：`Helvetica Neue` / `Helvetica` / `Arial` → Inter · `Futura` / `DIN Alternate` / `Arial Black` → Montserrat · `Bebas Neue` → League Gothic · `Segoe UI` → Roboto · `Courier New` / `Courier` → JetBrains Mono · `Garamond` → EB Garamond。（这就是为什么"安全"的 `Helvetica Neue` 堆叠总是能渲染——它映射到嵌入的 Inter。）

**与下面的禁用列表协调：** 几个嵌入家族（Inter、Roboto、Open Sans、Lato、Nunito、Poppins、Outfit、Playfair Display、EB Garamond）_也_在禁用单一文化列表中——它们渲染得很好但读起来很通用。**已嵌入且未被禁用**的家族——你的安全且独特的选择——是：**Montserrat、Oswald、League Gothic、Archivo Black、Space Mono、IBM Plex Mono、JetBrains Mono、Source Code Pro、Noto Sans JP**。选择这些（或通过"寻找字体"步骤确认的非捆绑字体）。非捆绑名称不一定会出问题——真正的 Google 字体会被自动获取和嵌入——但它带有 lint 警告和在云端渲染中的失败关闭获取，因此对于任何必须可预测渲染的内容，**通过 `@font-face` 自行嵌入**（参见"寻找字体"）而不是依赖隐式获取。

## 禁用

每个 LLM 都会使用的训练数据默认值。这些会在合成中产生单一文化。

Inter, Roboto, Open Sans, Noto Sans, Arimo, Lato, Source Sans, PT Sans, Nunito, Poppins, Outfit, Sora, Playfair Display, Cormorant Garamond, Bodoni Moda, EB Garamond, Cinzel, Prata, Syne

**尤其是 Syne** 是最被滥用的"独特"展示字体。它是一个即时的 AI 设计标志。

## 护栏规则

你知道这些规则但违反它们。停止。

- **不要搭配两种无衬线字体。** 你经常这样做——一个用于标题，一个用于正文。跨越边界：衬线 + 无衬线，或无衬线 + 等宽。
- **每场景一个表现性字体。** 你选择两种有趣的字体试图让它"更好"。一个表现，一个退居次要。
- **字重对比必须极端。** 你默认使用 400 vs 700。视频需要 300 vs 900。差异必须在运动中一目了然。
- **视频尺寸，而非网页尺寸。** 正文：最小 20px。标题：60px+。数据标签：16px。你会想用 14px。不要。

## 未经指示不得做的事

- **张力应有意义。** 不要模式匹配搭配。问为什么这两种字体不一致。搭配应体现内容的矛盾——机械 vs 人性化、公开 vs 私密、机构 vs 个人。如果你说不清这种张力，它就是武断的。
- **语域切换。** 将不同的字体分配给不同的交流模式——一种声音用于陈述，另一种用于数据，再一种用于归属。不是页面上的层级。而是对话中的声音。
- **张力可以存在于单个字体内部。** 一个看起来熟悉但暗藏奇怪的字体，是与观众的期望产生张力，而不是与另一种字体。
- **改变一个变量 = 戏剧性的对比。** 相同的字形，等宽 vs 比例。同一家族在不同视觉尺寸下。只改变节奏而其他一切保持不变。
- **双重个性有效。** 两种表现性字体如果共享态度（都玩世不恭，都精确），即使它们的形式完全不同，也可以共存。
- **时间就是层级。** 第一个出现的元素最重要。在视频中，顺序取代位置。
- **运动即是排版。** 一个词如何进入画面承载着与字体本身同样多的意义。0.1 秒的撞击 vs 2 秒的淡入——同样的字体，完全不同的信息。
- **固定阅读时间。** 屏幕上 3 秒 = 必须在 2 秒内可读。更少的词，更大的字体。
- **字距比网页更紧。** 显示尺寸上 -0.03em 到 -0.05em。视频编码会压缩字母细节。

## 寻找字体

不要默认使用你知道的字体。如果内容是奢华品，一个 grotesque 无衬线体可能比预期的 Didone 衬线体创造更多张力。先决定语域，再搜索。

将此脚本保存到 `/tmp/fontquery.py` 并运行 `curl -s 'https://fonts.google.com/metadata/fonts' > /tmp/gfonts.json && python3 /tmp/fontquery.py /tmp/gfonts.json`：

```python
import json, sys, random
from collections import OrderedDict

random.seed()  # true random each run

with open(sys.argv[1]) as f:
    data = json.load(f)
fonts = data.get("familyMetadataList", [])

ban = {"Inter","Roboto","Open Sans","Noto Sans","Lato","Poppins","Source Sans 3",
       "PT Sans","Nunito","Outfit","Sora","Playfair Display","Cormorant Garamond",
       "Bodoni Moda","EB Garamond","Cinzel","Prata","Arimo","Source Sans Pro","Syne"}
skip_pfx = ("Roboto","Noto ","Google Sans","Bpmf","Playwrite","Anek","BIZ ",
            "Nanum","Shippori","Sawarabi","Zen ","Kaisei","Kiwi ","Yuji ","Radio ")

def ok(f):
    if f["family"] in ban: return False
    if any(f["family"].startswith(b) for b in skip_pfx): return False
    if "latin" not in (f.get("subsets") or []): return False
    return True

seen = set()
R = OrderedDict()

# Trending Sans — recent (2022+), popular (<300)
R["Trending Sans"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") in ("Sans Serif","Display") and f.get("dateAdded","") >= "2022-01-01" and f.get("popularity",9999) < 300:
        R["Trending Sans"].append(f); seen.add(f["family"])

# Trending Serif — recent (2018+), popular (<600)
R["Trending Serif"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Serif" and f.get("dateAdded","") >= "2018-01-01" and f.get("popularity",9999) < 600:
        R["Trending Serif"].append(f); seen.add(f["family"])

# Monospace — recent (2018+), popular (<600)
R["Monospace"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Monospace" and f.get("dateAdded","") >= "2018-01-01" and f.get("popularity",9999) < 600:
        R["Monospace"].append(f); seen.add(f["family"])

# Impact & Condensed — heavy display fonts with 800+ weight
R["Impact & Condensed"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    has_heavy = any(k in list(f.get("fonts",{}).keys()) for k in ("800","900"))
    is_display = f.get("category") in ("Sans Serif","Display")
    if has_heavy and is_display and f.get("popularity",9999) < 400:
        R["Impact & Condensed"].append(f); seen.add(f["family"])

# Script & Handwriting — popular (<300)
R["Script & Handwriting"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Handwriting" and f.get("popularity",9999) < 300:
        R["Script & Handwriting"].append(f); seen.add(f["family"])


# Randomize the top 5 in each category so the LLM doesn't always pick the same first result
for cat in R:
    R[cat].sort(key=lambda x: x.get("popularity",9999))
    top5 = R[cat][:5]
    rest = R[cat][5:]
    random.shuffle(top5)
    R[cat] = top5 + rest
limits = {"Trending Sans":15,"Trending Serif":12,"Monospace":8,
          "Impact & Condensed":12,"Script & Handwriting":10}
for cat in R:
    items = R[cat][:limits.get(cat,10)]
    if not items: continue
    print(f"--- {cat} ({len(items)}) ---")
    for ff in items:
        var = "VAR" if ff.get("axes") else "   "
        print(f'  {ff.get("popularity"):4d} | {var} | {ff["family"]}')
    print()
```

五个类别：流行无衬线、流行衬线、等宽、冲击/紧缩、手写/手书。全部从 Google Fonts 元数据动态筛选——没有硬编码的字体名称。搭配时跨越分类界限。

## 选择思维

不要凭类别反射选择字体（编辑→衬线、科技→等宽、现代→几何无衬线）。那是模式匹配，不是设计。

1. **命名语域。** 内容在用哪种声音说话？机构权威？个人忏悔？技术精确？随意不敬？语域比类别更能缩小选择范围。
2. **物理化思考。** 想象字体作为品牌可以交付的物理对象——博物馆展品说明、手绘店招、1970 年代大型机终端手册、外套内的织物标签、印刷在廉价新闻纸上的儿童书、税务表格。符合语域的物理对象指向了正确_种类_的字体。
3. **拒绝你的第一直觉。** 第一个感觉正确的字体通常是你对该语域的训练数据默认值。如果你上次也选了它，找点别的。
4. **交叉检查假设。** 编辑简报不需要衬线体。技术简报不需要无衬线体。儿童产品不需要圆角展示字体。最独特的选择往往违背类别期望。

## 相似字体搭配

永远不要搭配两种相似但不相同的字体——两种几何无衬线体、两种过渡衬线体、两种人文无衬线体。它们会产生视觉摩擦而没有清晰的层级。观看者感觉有些"不对"但说不出来。要么使用一种字体的两个字重，要么搭配在多个轴上对比的字体：衬线 + 无衬线、紧缩 + 宽体、几何 + 人文。

## 深色背景

深色背景上的浅色文字会产生两种需要补偿的视错觉：

- **表观字重增加。** 相同的 `font-weight` 下，浅色在深色上比深色在浅色上更重。正文用 350 代替 400。标题受影响较小，因为尺寸补偿了。
- **表观间距更紧。** 字形周围的浅色光晕减少了感知间隙。将 `line-height` 比浅色背景值增加 0.05-0.1。对于显示尺寸，添加 0.01em `letter-spacing` 来抵消。

## 用于数据的 OpenType 特性

大多数字体内置了默认关闭的 OpenType 特性。为数据合成打开它们：

```css
/* 表格数字——数字在列中垂直对齐 */
.stat-value,
.timer,
.data-column {
  font-variant-numeric: tabular-nums;
}

/* 对角分数——将 1/2 渲染为 ½ */
.recipe-amount,
.ratio {
  font-variant-numeric: diagonal-fractions;
}

/* 缩写的小型大写——减少视觉喊叫 */
.abbreviation,
.unit {
  font-variant-caps: all-small-caps;
}

/* 禁用代码中的连字——fi, fl, ffi 应保持分离 */
code,
.code {
  font-variant-ligatures: none;
}
```

任何数字垂直堆叠的地方——统计标注、计时器、记分牌、数据表——`tabular-nums` 都是必需的。没有它，数字具有比例宽度，列无法对齐。
