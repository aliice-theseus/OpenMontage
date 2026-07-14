# shot-plan IR

Director 和 Builder 之间的单一约定。一个文件：`PROJECT_DIR/shot-plan.json`。

```jsonc
{
  // ── 概要（所有类别）──
  "category": "kinetic-type | stat | charts | logo-reveal | lower-thirds | webpage | news | tweet | asset-fusion",
  "duration_s": 6,
  "fps": 30,
  "canvas": { "w": 1080, "h": 1920, "aspect": "9:16" },
  "style": "自由形式视觉方向（氛围/能量/参考）",
  "palette": ["#…"], // 或 "derive-from-asset"
  "font": "<HF embed-list font>",
  "beats": [12, 37], // 可选的重音帧/秒
  "export": "mp4", // 或 "alpha-overlay"（透明 webm/mov）

  // ── 素材获取接缝（Director 第1部分）— [] 表示跳过素材来源阶段 ──
  "asset_needs": [
    {
      "role": "hero",
      "kind": "image|icon|logo|svg|news|web|tweet",
      "query": "…",
      "source": "…",
      "treatment": "cutout|recolor|vectorize|none",
    },
  ],

  // ── 构建指令（Director 第2部分，优先复用）──
  "block": "<catalog block id, e.g. data-chart | caption-kinetic-slam>", // 可选
  "customize": {
    /* 要在块上更改的内容：数据、文字、调色板、位置 */
  },

  // ── 类别特有内容 ──
  "content": {
    /* 形状因类别而异，见下文 */
  },
}
```

**各类别 `content` 形状：**

- `kinetic-type` → `scenes[]` `{ id, start, end, text, emphasis_words[], emotion, motion, beats[] }`
- `stat` → `{ value, prefix, suffix, label, ring: bool }`
- `charts` → `{ type: bar|line|pie|race|pct, data[], labels[], headline, axes: bool }`
- `logo-reveal` → `{ logo: <asset path>, tagline, url }`
- `lower-thirds` → `{ name, role, position, brand_colors[] }`
- `webpage` → `{ url, capture, highlights: [ { selector|region, label } ] }`（逐步高亮一个真实捕获的页面）
- `news` → `{ outlet, headline, body, keyword, layout: A|B, logo?, date?, subject? }`（文章高亮：将文字以可读大小排版 — **无缩放** — 然后在原地用标记带扫过关键词。布局**A** = 居中强调 9:16 纯文字；**B** = 完整文章 16:9，带 `logo` + `date` + `subject`（人物照片 → `remove-background` 抠图））
- `tweet` → `{ author, handle, avatar, text, metrics }`
- `asset-fusion` → `{ data_type, asset: <path>, affordance, element_positions: {center, extent, safe[], avoid[]}, derived_palette[], connectors[] }`

**不变规则：** `scenes`（如果存在）划分 `[0, duration_s]` 无间隙/重叠 · 空 `asset_needs` ⇒ 第2步（素材来源）跳过 · 指定了 `block` ⇒ Builder 复用它并定制，而非手动编写。
