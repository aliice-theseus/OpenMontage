# HyperFrames 技能 — 来源

`.agents/skills/` 下的 12 个 HyperFrames 系列技能来自上游 HyperFrames monorepo：

- **来源**：https://github.com/heygen-com/hyperframes
- **供应商提交**：`3351fb1a`（`chore: release v0.7.17`，2026-06-27）
- **供应商标签**：`v0.7.17`
- **供应商日期**：2026-06-27
- **供应商者**：在分支 `chore/version-bumps-and-hf-resync` 上重新供应商

## 已供应商的内容

**从之前的 0.4.2 时代副本重新供应商（上游重命名/重构）：**

| 技能 | 说明 |
|---|---|
| `hyperframes` | 0.7 中的精简入口点；深层内容已移到下方专注技能。 |
| `hyperframes-cli` | 0.7 大幅扩展（原来是 1 个文件，现在是 7 个）。现在原生涵盖 `validate`、`inspect`、`snapshot`、`benchmark`、`lambda` 等——旧的 OM 本地补丁教授 `validate` 已过时并被移除。 |
| `hyperframes-registry` | 块/组件注册表工作流。 |
| `website-to-video` | 上游从 `website-to-hyperframes` 重命名。 |

**新供应商（0.5–0.7 中的战略新增）：**

| 技能 | OpenMontage 中需要它的原因 |
|---|---|
| `hyperframes-core` | 组合契约——`data-*` 时间、轨道、子组合。从 `hyperframes` 0.4 拆分出的核心内容。 |
| `hyperframes-creative` | 非动画创意方向——调色板、排版、旁白、节拍规划。 |
| `hyperframes-media` | 音频 + 媒体资产——TTS、BGM、SFX、转录、字幕、背景移除。 |
| `hyperframes-animation` | 所有动画知识（规则、蓝图、过渡、技术、7 种运行时适配器）。替换以前散落在 `hyperframes` 中的临时运动指导。 |
| `media-use` | 代理媒体 OS——一个 `resolve` 动词通过项目/全局缓存 + HeyGen 目录将 BGM/SFX/图片/图标需求解析为本地文件。对 OpenMontage 资产阶段具有战略意义。 |
| `motion-graphics` | 短的设计主导动态图形模式（动态排版、统计揭示、Logo 片头、下三分之一）。 |
| `remotion-to-hyperframes` | 迁移指导——鉴于 OpenMontage 运行两种运行时，直接相关。 |
| `music-to-video` | 使用 `hyperframes beats` 的节拍同步音乐驱动视频工作流。 |

## 故意未供应商

这些上游技能是 HF 工作流特定的，会与 OpenMontage 自身的管道路由竞争或重复。根据管道需要重新评估：

`embedded-captions`、`faceless-explainer`、`general-video`、`pr-to-video`、`product-launch-video`、`slideshow`、`talking-head-recut`。

## 重新同步说明

要重新供应商较新的上游版本：

```bash
cd C:/Users/ishan/Documents/hyperframes
git pull --ff-only origin main
# 然后在 OpenMontage 中：
cd /c/Users/ishan/Documents/OpenMontage
HF=C:/Users/ishan/Documents/hyperframes
for d in hyperframes hyperframes-cli hyperframes-registry hyperframes-core \
         hyperframes-creative hyperframes-media hyperframes-animation \
         media-use motion-graphics remotion-to-hyperframes \
         music-to-video website-to-video; do
  rm -rf ".agents/skills/$d"
  cp -r "$HF/skills/$d" ".agents/skills/$d"
done
# 然后更新此文件顶部的供应商提交/标签/日期。
```

## 未来自动化

上游 0.7 添加了 `hyperframes skills`——一个带有新鲜度清单和版本检查来安装/更新 HF 技能的 CLI。考虑采用它作为机械真实来源，而不是手动供应商（也会在多代理设置中自动标记过时）。参见 HF 历史中的 `feat(cli): skills freshness — version check, manifest, global install + multi-agent mirror (#1753)`。
