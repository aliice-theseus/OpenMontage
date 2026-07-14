# titlecard-reveal — 标题卡片 / 单卡片揭示

**意图**：平静的呼吸/着陆节拍——一张干净的标题或单一品牌/证明卡片，用一个克制的动作（上滑交叉淡入淡出，或擦拭揭示）揭示，然后静止保持。低运动是交付物，而非缺陷。

**服务角色**

- Benefits（来自 `benefits-titlecard-crossfade`，#34）：一个平静的两行价值标题卡片——标题价值行，然后一次上滑交叉淡入淡出到限定词/阐述行，该行居中保持。
- Social_Proof（来自 `social-proof-reveal-card`，#35）：用一个对角胶囊擦拭将繁忙的应用拼贴画擦开，露出一个干净的品牌组合（图标 + wordmark）加上一个居中的"受 [N]+ [audience] 团队喜爱"社交证明行，弹簧稳定并保持。

**时长**：3–5 秒（Benefits 3–4 秒；Social_Proof ~5 秒 / 观察到 4.7 秒）。

**镜头结构**

```
场景 1（0.0–~0.4 秒）：摄像机静止在 [中性/暗色背景] 上。建立开场状态。
  变体 — Benefits：空白到文本 — [benefit line 1] 即将居中淡入（无繁忙开场）。
  变体 — Social_Proof：一个繁忙的引入画幅短暂保持 — 重叠卡片组成的 [app-screenshot / use-case collage] 在 [setup line] 下。

场景 2（~0.4–~1.5 秒）：**一个**动作执行 — 一个克制的揭示，将平静的卡片带到中心。
  变体 — Benefits：[benefit line 1] 居中淡入同时略微缩放（~95%→100%，平滑缓出）并保持。
  变体 — Social_Proof：一个大的 [accent-color] 圆角胶囊沿对角线左下→右上扫过并离开角落，clip-path 擦除拼贴画，露出下方的 [品牌 logo 组合]，同时 [logo 图标] 描画绘制。

场景 3（~1.5 秒–结束）：揭示/稳定的卡片保持到结束（分配的静止）。最多一个微妙的动态元素（卡片上的缓慢呼吸脉冲，或非常缓慢的摄像机漂移）。无第二阶段发展。
  变体 — Benefits：[benefit line 1] 上移并淡出，同时 [benefit line 2 — qualifier / elaboration] 从中心下方上移并淡入占据中心；保持。（这个单次上滑交叉淡入淡出就是**那一个**动作 — Benefits 在场景 2 中没有前置擦拭。）
  变体 — Social_Proof：组合 — [logo icon] 居中，[wordmark] 在其下，居中的 [social-proof tagline] "受 [N]+ [audience] 团队喜爱"（[N]+ 可能计数递增）— 弹簧小幅稳定，然后保持。
```

**动词语汇**：单次克制揭示（柔和淡入 + 微妙缩放稳定 | 对角 clip-path 胶囊擦拭），两个居中行之间的一次上滑交叉淡入淡出（Benefits），图标描画绘制（Social_Proof），可选 "[N]+ 团队"计数递增，logo+标语弹簧稳定并保持，保持卡片上的微妙呼吸，保持到结束。平静基调——无弹簧链、无翻滚、无逐个节拍翻转、无第二阶段。摄像机静止（可选仅非常缓慢的漂移）。

**规则映射**

- 柔和淡入 + 微妙缩放稳定（Benefits 场景 2）→ `rules/scale-swap-transition.md`（克制进入/稳定；交叉参考 `techniques.md` 中的淡入缓动）
- 两个居中行之间的单次上滑交叉淡入淡出（Benefits 场景 3）→ `rules/discrete-text-sequence.md`（一行交接给下一行；上移 + 交叉淡入淡出）
- 对角胶囊擦拭揭示（Social_Proof 场景 2）→ `rules/techniques.md`（clip-path 揭示遮罩 — 擦拭）
- 图标描画绘制（Social_Proof 场景 2）→ `rules/svg-path-draw.md`
- "[N]+ 团队"计数递增（Social_Proof 场景 3，可选）→ `rules/counting-dynamic-scale.md`
- 标语弹簧稳定并保持（Social_Proof 场景 3）→ `rules/spring-pop-entrance.md`（单次柔和稳定；有意为一个节拍，而非链）
- 保持卡片上的微妙呼吸（保持期间的一个动态元素）→ `rules/sine-wave-loop.md`

**摄像机修饰**：可选 — 仅在保持期间的单次非常缓慢的漂移/推进 → `rules/multi-phase-camera.md`。默认为完全静止；除非保持的节拍会读作定格画面，否则不要添加。

**静止说明**：这是一个合法的分配静止节拍。场景 3 中的保持是交付物，而非未动画化的间隙——不要制造发展阶段、额外交换或强制动画。一次克制动作 + 微妙保持（可选一个呼吸元素或一次缓慢漂移）是正确且完整的形态。
