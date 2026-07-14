# 过渡注册表 — 机器真相源

**PLV 场景到场景过渡**的单一真相源。确定性注入器（`product-launch-video/scripts/inject-transitions.mjs`）读取下面的 JSON 块并将匹配的 `gsap_template` 印到主时间线上。规划器（`product-launch-video/agents/visual-design.md`）通过其 `name` 命名过渡；其他一切都是线束。

此文件**不是**所有过渡的目录 — 那是 `catalog.md` + `css-*.md`（≈40 个 CSS + 着色器）。此注册表是经过策划的子集，是 **Tier-B 就绪**的：在两个场景**剪辑包裹容器**（`#el-<sid>`）上的纯 transform / opacity / filter，无注入叠加 DOM，无逐场景协作。叠加族（错开块、百叶窗、漏光、网格溶解、页面灼烧）和着色器过渡推迟到后期阶段。

## 注入器如何应用过渡

在场景 _i_（`from`）和场景 _i+1_（`to`）之间的 `break` 边界，注入器：

1. 将 `#el-<from>` 包裹容器 `data-duration` 延长 `duration_s`（保持其最终帧 — 已验证：`core/src/runtime/init.ts:1393-1410` 外部槽分支）。
2. 将 `#el-<to>` 包裹容器 `data-start` 提前 `duration_s`（创建重叠窗口）。
3. 将所有剪辑 `data-track-index` 重新分配为 0/1 乒乓，使两个重叠包裹容器从不同享一个轨道（同轨道重叠是非法的 — `core/src/lint/rules/composition.ts`）。更高轨道合成在上面。
4. 在 `T = overlap-start` 时将 `gsap_template` 印入 `window.__timelines["main"]`。

由原型渲染验证（2026-05-31）：主时间线包裹容器补间被定位和渲染（无需与子组合自己的暂停时间线双重定位 — 运行时独立驱动它们），扩展的包裹容器保持场景 _i_ 的最终帧，且更高轨道的进入包裹容器合成在上面 + 与退出容器混合。

## 模板占位符

注入器在每个 `gsap_template` 行中替换这些标记：

| 标记                              | 含义                                                                    |
| --------------------------------- | ----------------------------------------------------------------------- |
| `__OLD__`                         | `"#el-<from>"` — 退出剪辑包裹容器选择器（带引号）                        |
| `__NEW__`                         | `"#el-<to>"` — 进入剪辑包裹容器选择器（带引号）                          |
| `__T__`                           | 重叠开始时间（秒，主时钟）                                                |
| `__DUR__`                         | 此边界的 `duration_s`                                                    |
| `__DX__`                          | 方向类型的水平行程：`-1920`（左）/ `1920`（右）                          |
| `__DY__`                          | 垂直行程：`-1080`（上）/ `1080`（下）                                    |
| `__ORIGIN_OUT__` / `__ORIGIN_IN__` | `squeeze` 的 transformOrigin 对                                          |

`filter` / `scaleX` / `transformOrigin` 在主时间线上对 lint 是干净的（已验证：`core/src/lint/rules/gsap.ts` 无逐属性白名单，并将其检查范围限定到 `data-composition-id` 范围；x/y/scale/rotation/opacity 白名单仅是_场景工作线程_提示规则 — 它不绑定 index.html）。

## 注册表

```json
{
  "transitions": [
    {
      "name": "crossfade",
      "tier": "b",
      "overlay": false,
      "energy": "any",
      "default_duration_s": 0.5,
      "directions": [],
      "source": "css-dissolve.md",
      "gsap_template": [
        "tl.to(__OLD__, { opacity: 0, duration: __DUR__, ease: \"power2.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { opacity: 0 }, { opacity: 1, duration: __DUR__, ease: \"power2.inOut\" }, __T__);"
      ]
    },
    {
      "name": "blur-crossfade",
      "tier": "b",
      "overlay": false,
      "energy": "calm",
      "default_duration_s": 0.6,
      "directions": [],
      "source": "css-dissolve.md",
      "note": "当两个场景 #root 背景差异大时的默认值 — 模糊掩盖了纯交叉淡入淡出会暴露的背景色冲突。",
      "gsap_template": [
        "tl.to(__OLD__, { filter: \"blur(10px)\", scale: 1.03, opacity: 0, duration: __DUR__, ease: \"power2.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { filter: \"blur(10px)\", scale: 0.97, opacity: 0 }, { filter: \"blur(0px)\", scale: 1, opacity: 1, duration: __DUR__, ease: \"power2.inOut\" }, __T__);"
      ]
    },
    {
      "name": "push-slide",
      "tier": "b",
      "overlay": false,
      "energy": "medium",
      "default_duration_s": 0.5,
      "directions": ["LEFT", "RIGHT", "UP", "DOWN"],
      "default_direction": "LEFT",
      "source": "css-push.md",
      "note": "方向性。注入器从方向选择 __DX__/__DY__ 并发出水平或垂直对（非两者）。",
      "gsap_template_horizontal": [
        "tl.to(__OLD__, { x: __DX__, duration: __DUR__, ease: \"power3.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { x: __DXIN__, opacity: 1 }, { x: 0, duration: __DUR__, ease: \"power3.inOut\" }, __T__);"
      ],
      "gsap_template_vertical": [
        "tl.to(__OLD__, { y: __DY__, duration: __DUR__, ease: \"power3.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { y: __DYIN__, opacity: 1 }, { y: 0, duration: __DUR__, ease: \"power3.inOut\" }, __T__);"
      ]
    },
    {
      "name": "zoom-through",
      "tier": "b",
      "overlay": false,
      "energy": "high",
      "default_duration_s": 0.4,
      "directions": [],
      "source": "css-scale.md",
      "gsap_template": [
        "tl.to(__OLD__, { scale: 2.5, opacity: 0, filter: \"blur(8px)\", duration: __DUR__, ease: \"power3.in\" }, __T__);",
        "tl.fromTo(__NEW__, { scale: 0.5, opacity: 0, filter: \"blur(8px)\" }, { scale: 1, opacity: 1, filter: \"blur(0px)\", duration: __DUR__, ease: \"power3.out\" }, __T__);"
      ]
    },
    {
      "name": "squeeze",
      "tier": "b",
      "overlay": false,
      "energy": "medium",
      "default_duration_s": 0.4,
      "directions": [],
      "source": "css-push.md",
      "note": "旧场景压缩到左边缘的垂直线；新场景从右边缘扩展。进入场景从偏移开始（scaleX 0），因此其更高轨道堆叠无害。",
      "gsap_template": [
        "tl.to(__OLD__, { scaleX: 0, transformOrigin: \"left center\", duration: __DUR__, ease: \"power3.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { scaleX: 0, transformOrigin: \"right center\", opacity: 1 }, { scaleX: 1, transformOrigin: \"right center\", duration: __DUR__, ease: \"power3.inOut\" }, __T__);"
      ]
    }
  ],
  "tier_a_types": ["morph", "shared-element"],
  "default_high_energy": "zoom-through",
  "default_calm": "blur-crossfade",
  "max_duration_s": 2.0
}
```

## 默认推导（当规划器省略 `**Transition:**` 时使用）

没有命名过渡的 `break` 边界获得默认值：

1. 如果进入场景的创意简报读作 HIGH 能量（爆炸性/动感/狂乱关键词），使用 `default_high_energy`（`zoom-through`）。
2. 否则使用 `default_calm`（`blur-crossfade`）— 通用默认值。模糊掩盖任何背景变化并读作有意为之，使整个视频保持在约 2 种过渡类型（"重复 2-3"原则）。

## 作为规划器的选择（唯一代理接触点）

为整个视频选择 **2-3 种类型**并重复它们 — 重复读作专业（参见 `overview.md`）。此预算仅计算 **Tier-B 场景间类型**（上面注册表中的 5 个）；Tier-A `shared-element` 变形是由叙事 `intent: morph` 驱动的工作作者桥梁 — 它**豁免且不计入** 2-3 种。在每个场景上命名进入过渡：

```
**Transition:** blur-crossfade
**Transition:** push-slide LEFT
**Transition:** zoom-through 0.3s
```

省略锚点以接受上述默认值。不要编写 GSAP、调整时间或编辑 index.html — 线束印代码、计算重叠并分配轨道。
