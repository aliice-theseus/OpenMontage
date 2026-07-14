# OpenMontage 背景移除使用指南

> 来源：rembg 库文档、U2Net 论文 (Qin et al. 2020)、IS-Net 论文
> (Qin et al. 2022)、OpenMontage `tools/bg_remove.py` 实现

## 快速参考卡

```
默认模型：        u2net（通用，快速）
人物模式：        u2net_human_seg（针对人形轮廓优化）
精细边缘：        启用 alpha_matting（头发、毛皮、树叶）
输出：            默认透明 PNG；设置 bg_color 用于纯色替换
运行时：          每张图约1-3秒（CPU），<0.5秒（GPU 配合 onnxruntime-gpu）
安装：            pip install rembg（CPU）| pip install rembg[gpu]（CUDA）
```

## 何时使用 bg_remove

背景移除是一个**资产准备**步骤。在合成阶段之前使用。

- **产品演示/电商视频** — 将产品隔离在干净背景上
- **合成** — 将说话者叠加在生成的背景或图表上
- **缩略图生成** — YouTube 缩略图的干净抠图
- **绿幕替换** — 无需实际绿幕即可实现绿幕效果
- **B-roll 准备** — 清理原始照片以供叠加使用

## 模型选择指南

| 模型 | 最适合 | 速度 | 说明 |
|------|--------|------|------|
| `u2net` | 通用物体、产品、场景 | 快 | 默认；良好的全能型 |
| `u2net_human_seg` | 人物、肖像、演讲者 | 快 | 对人形轮廓更准确的遮罩 |
| `isnet-general-use` | 复杂边缘、头发、毛皮 | 较慢 | 在精细边界上细节更高 |

**决策规则：** 如果主体是人，使用 `u2net_human_seg`。如果主体有复杂边缘（头发、毛皮、树叶）且需要最高质量，使用 `isnet-general-use`。否则，使用默认的 `u2net`。

## Alpha 抠图

Alpha 抠图通过计算边界的软透明度来细化边缘遮罩。产生更自然的边缘，但处理时间约增加2倍。

| 主体类型 | Alpha 抠图 | 原因 |
|----------|-----------|------|
| 头发、毛皮、羽毛 | 启用 | 精细的半透明丝线需要软边缘 |
| 树叶、树木、草 | 启用 | 不规则的有机边界受益于抠图 |
| 产品、设备 | 禁用 | 干净的几何边缘；抠图不增加价值 |
| 文字、标志、形状 | 禁用 | 硬边缘对这些主体是正确的 |

## 常见工作流程

### 1. 用于合成的演讲者抠图

将演讲者从背景中提取出来并叠加在图表或幻灯片上。

```
bg_remove(input_path="speaker.png", model="u2net_human_seg")
  --> speaker_nobg.png（透明）
  --> 在合成阶段叠加在图表/幻灯片上
```

### 2. 产品隔离

隔离产品并可选地放置在品牌颜色的背景上。

```
bg_remove(input_path="product.jpg", model="u2net")
  --> product_nobg.png（透明）

# 或带品牌背景：
bg_remove(input_path="product.jpg", model="u2net", bg_color="#FFFFFF")
  --> product_nobg.png（白色背景）
```

### 3. 缩略图准备

移除背景、放大、然后与文字叠加合成。

```
bg_remove(input_path="subject.png", model="u2net_human_seg", alpha_matting=True)
  --> subject_nobg.png
  --> upscale --> 在合成阶段与文字叠加合成
```

### 4. 批量帧处理

在准备用于合成序列的多个帧时，在进入合成阶段前处理所有源帧。

```
for each source frame:
    bg_remove(input_path=frame, model="u2net_human_seg")
    --> frame_nobg.png
then: 将所有透明帧与背景序列合成
```

## 质量检查清单

在进入合成阶段前，验证每个 bg_remove 输出：

- [ ] **边缘质量干净** — 主体周围无光晕伪影
- [ ] **精细细节保留** — 头发、手指和细部特征完好
- [ ] **透明度完整** — 透明区域无残留背景渗色
- [ ] **主体完整性** — 主体无部分被错误移除
- [ ] **合成测试** — 叠加到目标背景上时，主体自然融合

## 应用于 OpenMontage

在资产准备中使用 `bg_remove` 工具时：

1. **任何包含人物的帧使用 `u2net_human_seg`** — 它比通用模型在人形轮廓周围产生更紧密的遮罩
2. **仅对具有复杂边缘的主体启用 `alpha_matting`** 如头发、毛皮或树叶 — 对边缘干净的主体跳过以节省处理时间
3. **合成工作流输出透明 PNG**（省略 `bg_color`）并在合成阶段分层 — 保持最大灵活性
4. **纯色背景替换设置 `bg_color`** 以匹配剧本的背景色令牌 — 使输出与项目风格一致
5. **在合成阶段之前处理源帧** — bg_remove 是资产准备步骤，而非合成时操作
6. **在合成前以全分辨率检查输出边缘** — 光晕伪影和边缘渗色在最终视频中可见，必须早期发现
