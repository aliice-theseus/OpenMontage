# OpenMontage 素材来源使用指南

> 如何有效使用素材图片和视频工具 — 查询构建、提供商选择、许可证意识和与资产流程的集成。

## 可用的素材工具

| 工具 | 提供商 | 内容 | 费用 | 速率限制 | 最适合 |
|------|--------|------|------|----------|--------|
| `pexels_image` | Pexels | 照片 | 免费 | 200/小时 | 高质量摄影，丰富的库 |
| `pixabay_image` | Pixabay | 照片、插图、矢量 | 免费 | 100/分钟 | 分类筛选，大型库（500万+） |
| `pexels_video` | Pexels | 视频片段 | 免费 | 200/小时 | HD/4K真实世界素材 |
| `pixabay_video` | Pixabay | 视频片段 | 免费 | 100/分钟 | 分类筛选视频，动画片段 |

## 提供商选择指南

### 何时使用 Pexels
- 需要**高质量摄影**（精选、专业）
- 需要**视频**（比 Pixabay 更大的视频库）
- 想要**方向筛选**（横屏/竖屏/方形）
- 想要**颜色筛选**（匹配剧本调色板）
- 需要**多语言**结果（28个地区）

### 何时使用 Pixabay
- 需要**基于分类的筛选**（自然、商业、科学等）
- 想要除照片外的**插图或矢量图**
- 想要**编辑精选**的筛选结果
- 需要**更高速率限制**（100/分钟 vs 200/小时）
- 需要**视频类型筛选**（实拍 vs 动画）

### 决策流程
```
需要素材图片？
├── 需要特定分类（科学、商业等）？→ pixabay_image
├── 需要插图/矢量？→ pixabay_image
├── 需要颜色匹配？→ pexels_image
└── 一般照片？→ pexels_image（更高质量的筛选）

需要素材视频？
├── 需要4K？→ pexels_video（支持4K通过 size="large"）
├── 需要动画片段？→ pixabay_video（video_type="animation"）
├── 需要分类筛选？→ pixabay_video
└── 一般素材？→ pexels_video（更好的HD质量）
```

## 输入参数指南

### pexels_image / pexels_video
```python
{
    "query": "城市天际线日落",      # 必填：搜索词
    "orientation": "landscape",           # 可选：landscape/portrait/square
    "size": "large",                      # 可选：large/medium/small
    "color": "FF6B35",                    # 可选：不带#的十六进制或颜色名称
    "per_page": 5,                        # 每页结果数（1-80）
    "download_size": "large2x",           # 图像：original/large2x/large/medium
    "preferred_quality": "hd",            # 视频：hd/sd
    "output_path": "assets/images/s3.jpg" # 保存位置
}
```

### pixabay_image / pixabay_video
```python
{
    "query": "服务器机房",              # 必填：搜索词（最多100字符）
    "image_type": "photo",               # 图像：all/photo/illustration/vector
    "video_type": "film",                # 视频：all/film/animation
    "orientation": "horizontal",          # all/horizontal/vertical
    "category": "computer",              # 20个分类之一
    "colors": "blue,gray",              # 逗号分隔的颜色名称
    "editors_choice": true,              # 仅精选高质量结果
    "safesearch": true,                  # 生产环境始终为true
    "output_path": "assets/video/s5.mp4" # 保存位置
}
```

## 注意事项和最佳实践

### 1. Pixabay URL 会过期
Pixabay 下载 URL 包含嵌入式令牌，会过期。**搜索后始终立即下载**。工具会自动处理此问题，但绝不缓存 Pixabay URL 以供日后使用。

### 2. Pixabay 分辨率限制
标准 Pixabay API 用户最大获得 1280px 宽的图像（`largeImageURL`）。完整分辨率需要经过批准的 API 访问。对于大多数视频制作叠加，1280px 足够。

### 3. Pexels 认证头
Pexels 使用 `Authorization` 头中的纯 API 密钥（不是 `Bearer`）。工具会处理此问题，但调试时需注意。

### 4. 搜索结果因地区而异
Pexels 支持28个地区。如果搜索特定文化内容，设置 locale 参数。

### 5. 素材图片是确定性的
与 AI 生成不同，两次搜索"海浪"返回相同的结果。如果第一个结果不够好，尝试不同的关键词 — 不要重试相同的查询。

### 6. 视频时长筛选
两个素材视频工具都支持 `min_duration` 和 `max_duration` 参数。当你只需要4秒时，使用这些参数避免下载30秒的片段 — 可节省带宽和时间。

## 与资产流程的集成

素材工具与生成工具完全一样集成。在资产清单中：

```json
{
    "id": "broll-s3",
    "type": "image",
    "subtype": "broll",
    "path": "assets/images/broll-s3.jpg",
    "source_tool": "pexels_image",
    "scene_id": "scene-3",
    "cost_usd": 0.00,
    "metadata": {
        "photographer": "Joey Farina",
        "source_url": "https://www.pexels.com/photo/2014422/",
        "license": "Pexels License（免费，无需署名）"
    }
}
```

编辑导演和合成导演将素材资产视为与生成的资产完全相同 — 它们只引用清单中的文件路径。

## 许可摘要

| 提供商 | 商业使用 | 署名 | 限制 |
|--------|----------|------|------|
| Pexels | 是，免费 | 不需要（但感谢） | 不得出售未修改的；不得暗示背书 |
| Pixabay | 是，免费 | 不需要 | 不得出售未修改的；不得创建竞争性素材服务 |

两者对 OpenMontage 所有用例都是安全的。无需许可费、无需按使用版税、无需署名义务。
