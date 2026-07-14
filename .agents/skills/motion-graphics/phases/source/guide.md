# source 阶段 — 资产获取（资产优先）

**仅在 `shot-plan.json.asset_needs` 非空时运行**（形式类别永远不会到达此处）。获取每个所需资产 → **冻结的项目本地路径** + 账本（`assets/index.md`）。使用 `/hyperframes-media`（捕获/资产准备）以及，**当安装了外部资产搜索技能（如 media-use）时**，使用其 `resolve` 步骤。如果没有此类搜索能力可用，则**降级为无资产**（见下文）。

## 按资产需求

- `image/icon/logo/svg` → media-use `resolve`：**搜索**（asset_scout：Google Images / SerpAPI + Noun Project）、**生成**（图像模型）或**用户提供**（标志）。可选 `treatment`：抠图（remove-bg）/重新着色/矢量化。
- `news/web/tweet` → **RWA 风格搜索**（media-use 的文档化传统 — `media-use/references/search-strategy.md` 将 `resolve` 追溯到 RWA 子代理）。两极查询：**原子级**（1–3个词，可组合）或**具体级**（5–15个词：新闻事件/推文）；绝不要中间值。失败的具体查询被丢弃，不扩大范围。

## 步骤

1. 从 `shot-plan.json` 读取 `asset_needs`。
2. 对每个：**分析 → 搜索 → 审查（使用/可能/拒绝 — 选择是困难的部分；不要取第一个/生成的结果）→ 冻结**保留的资产到 `assets/`（重新托管远程 URL）。
3. 写入 `assets/index.md` — 代理可读的账本：`role → 冻结路径 + 来源`。
4. 对于 `asset-fusion`：同时捕获资产的可测量几何形状（以便 Director 第2部分可以设置 `element_positions`）+ 取色板。

## 优雅降级

如果提供方/搜索不可用，在 `context.log` 中标记需求未满足；类别尽可能回退到无资产（例如 `news` → 无来源图片时的排版标题）。

> 说明：`(cd "$PROJECT_DIR" && node <SKILL_DIR>/phases/source/resolve.mjs --plan ./shot-plan.json --out ./assets)` — 或直接驱动 media-use 的 `resolve` 过程。
