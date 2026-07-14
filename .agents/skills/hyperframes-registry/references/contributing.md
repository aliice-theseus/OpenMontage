# 向注册表贡献块或组件

引导用户从想法到合并 PR，用于新的注册表块或组件。

## 工作流

```
1. 澄清 → 2. 脚手架 → 3. 构建 → 4. 验证 → 5. 预览 → 6. 发布
```

### 步骤 1：澄清

询问他们在构建什么。注册表有两种项目类型：

- **块**（`registry/blocks/`，类型 `hyperframes:block`）——具有固定尺寸和时长的完整独立作品。字幕样式、VFX 效果、标题卡、下方三分之一。
- **组件**（`registry/components/`，类型 `hyperframes:component`）——没有固定尺寸或时长的可重用片段。CSS 效果、文本处理、适应任何作品大小的叠加。

然后询问：

- 效果的一句话描述
- 视觉参考（URL、截图或描述）
- 谁在什么时候使用它？

### 步骤 2：脚手架

创建注册表结构：

**对于块：**

```
registry/blocks/{block-name}/
  {block-name}.html
  registry-item.json
```

**对于组件：**

```
registry/components/{component-name}/
  {component-name}.html
  registry-item.json
```

**命名约定：**

| 项目名称 | ID 前缀 | 示例 ID |
| ---------------- | --------- | ---------------------- |
| `cap-hormozi` | `hz` | `hz-cg-0`、`hz-cw-3` |
| `cap-typewriter` | `tw` | `tw-cg-0`、`tw-ch-0-5` |
| `vfx-chrome` | `vc` | `vc-canvas` |

使用 2-3 字母前缀。所有元素 ID 必须使用此前缀以避免在子作品中冲突。

### 步骤 3：构建

根据类型应用正确的模板。参见 [templates.md](templates.md) 获取可复制粘贴的起始模板。

#### 字幕块

**不可协商的字幕规则：**

- 字体：比例字体**最小 96px**。等宽字体**可接受 64-72px**（更宽的字符需要较小尺寸）。
- 可读性：`-webkit-text-stroke: 2-3px` 或多层 `text-shadow`
- 溢出：在每个组上调用 `window.__hyperframes.fitTextFontSize()`
- 卡拉 OK：通过 `tl.to(wordEl, { color/scale }, WORDS[wi].start)` 高亮活跃词
- 硬清除：在每个组上使用 `tl.set(groupEl, { opacity: 0, visibility: "hidden" }, g.end)`
- **永远不要在 `tl.set(el, { opacity: 1 })` 的相同位置使用 `tl.from(el, { opacity: 0 })`**——from 会覆盖 set。改用 `tl.to`。

### 步骤 4：验证

```bash
hyperframes lint                    # 需要 0 错误
hyperframes validate --no-contrast  # 需要 0 控制台错误
```

### 步骤 5：预览

```bash
# 渲染预览视频
hyperframes render -o preview.mp4

# 快照用于视觉 QA
hyperframes snapshot --at "1.0,3.0,5.0,7.0"

# 发布到 hyperframes.dev 供审核
npx hyperframes publish
```

### 步骤 6：发布

**所有步骤都是必需的。缺少任何一个都会产生破损的目录条目。**

```bash
# 1. 创建分支
git checkout -b feat/registry-{name}

# 2. 格式化 HTML
npx oxfmt registry/{kind}/{name}/*.html

# 3. 更新 registry/registry.json — 向 "items" 数组添加条目：
#    { "name": "{name}", "type": "hyperframes:block" }  (或 "hyperframes:component")

# 4. 生成目录文档页面
npx tsx scripts/generate-catalog-pages.ts

# 5. 发布到 hyperframes.dev 以便审阅者预览
npx hyperframes publish

# 6. 暂存所有内容
git add registry/{kind}/{name}/ registry/registry.json docs/catalog/

# 7. 提交
git commit -m "feat(registry): 添加 {name} — {一句话描述}"

# 8. 推送并打开带 hyperframes.dev 链接的 PR
git push origin feat/registry-{name}
gh pr create --title "feat(registry): {name}" --body "preview: {hyperframes.dev-url}"
```

## 质量关卡

- [ ] `hyperframes lint` → 0 错误
- [ ] `hyperframes validate` → 0 控制台错误
- [ ] `npx oxfmt --check` 通过
- [ ] `registry/registry.json` 已更新新条目
- [ ] `scripts/generate-catalog-pages.ts` 已运行（文档页面已生成）
- [ ] `npx hyperframes publish` 已运行（声明你的项目 URL）
- [ ] 预览 MP4 已附加到 PR（外部）或目录 PNG 已上传（内部）
- [ ] 所有 ID 唯一且带前缀
