# locate — 在图像中查找"X"（不假设检测器 API）

每个消费者（asset-fusion 环形、网页高亮、未来讲解器/重剪覆盖层）使用的单一约定：

```
locate(image, target-description) → { box: [x0,y0,x1,y1], center: [cx,cy] }   # 归一化 0..1
```

## 为什么存在

作者模型在**回归杂乱完整图像中的像素坐标**方面不可靠（测量：弱视觉模型约16–24%中心误差 → 环形偏离目标），但在**挑选编号条**方面可靠（使用下面的循环约3–4%）。因此：绝不要目测坐标；通过离散选择定位。（RSVP, ACL 2025。）

## 路由 — 选择实际可用的最便宜路径

1. **有强检测器可用**（例如环境中存在 `GEMINI_API_KEY`）→
   `node grounding/locate.mjs auto <img> "<target>"` — 一次调用，完成。
   **绝不要假设密钥存在。** 没有密钥 → 路径 2。
2. **无检测器（正常情况）** → 您就是定位器；运行网格循环。

## 网格循环（您在步骤之间读取图像）

```
node grounding/locate.mjs overlay <img> --out /tmp/g
  → 读取 /tmp/g/gv.png（垂直条带 1-9）和 gh.png（水平条带 1-9）；
    决定目标跨越哪些条带编号（列出它触及的每个条带）。
node grounding/locate.mjs region <img> --vids 4,5 --hids 6,7 --out /tmp/g
  → 读取 /tmp/g/gc.png（裁剪并放大后的区域，更精细的 6×6 网格）；
    选择更精细的条带。（再次选择条带 — 不要切换为估算坐标；离散选择是全部意义所在，在两个阶段都是如此。）
node grounding/locate.mjs final <img> --region <from step 2> --vids 3,4 --hids 3,4
  → 最终的 {box, center}。
node grounding/locate.mjs mark <img> --box <final box> --out /tmp/g/check.png
  → 验证：读取 check.png。红框在目标上 → 完成。偏离 → 用修正后的条带重做
    region/final（您现在知道方向了）。绝不要跳过此步骤；它将静默失误转化为一次廉价重试。
```

## 歧义 — 在定位前解决

如果目标描述可以匹配多个实例（场景中有五个"鼓"），没有几何信息能拯救您。首先使引用唯一（"最右边的鼓"、"前船上的鼓"），必要时询问用户 — 然后运行循环。

## 降级路径（如果 locate.mjs 本身不可用）

思路只有5行 — 用任何图像工具都可复现：
绘制编号 9×9 网格 → 选择目标跨越的条带 → 裁剪该区域
（+填充约0.4条带）并放大 → 绘制更精细的 6×6 网格 → 再次选择 → 映射回
（`global = region_origin + local × region_size`）→ 绘制框并查看它。

## 说明

- 几何逻辑固定在 `locate.mjs` 中（node + ffmpeg，零 npm 依赖 — 两者
  已是 hyperframes 所需）。不要临时重新实现；测量的精度
  仅对该实现成立。
- 消费者：`samples/asset-fusion/_ref-circle-highlight.html` 直接从 `final`/`auto` 输出获取 `CFG.box`。
- 端到端测量（同一代理、同一模板、仅定位步骤不同）：
  目测平均中心误差 6.5% → 本协议 2.3%，无更差案例。
