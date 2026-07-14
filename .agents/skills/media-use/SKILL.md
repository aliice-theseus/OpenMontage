---
name: media-use
description: 代理媒体操作系统 — 将任何媒体需求（BGM、音效、图片、图标）解析为冻结的本地文件 + 账本记录。一个动词（`resolve`）处理完整级联 — 项目缓存、全局缓存、HeyGen 目录搜索、冻结、注册。将搜索噪音保留在磁盘上，向代理返回一个路径。当合成需要背景音乐、音效、图片或图标时使用。
---

# media-use

将媒体需求解析为冻结的本地文件。一个动词，四种类型，零上下文噪音。

## 何时使用

每当合成需要媒体时调用 `resolve` — 背景音乐、音效、图片或图标。media-use 会搜索 HeyGen 目录、下载最佳匹配、本地冻结并注册到清单中。代理只得到一行输出；所有搜索噪音保留在磁盘上。

## Resolve

```bash
node <SKILL_DIR>/scripts/resolve.mjs --type <type> --intent "<description>" --project <dir>
```

返回一行：`resolved <id> → <path> (<type>, <metadata>)`

### 类型

| 类型    | 查找内容       | 提供商                                 |
| ------- | ------------------- | ---------------------------------------- |
| `bgm`   | 背景音乐    | HeyGen 音频目录（1 万+ 曲目）       |
| `sfx`   | 音效       | 内置 19 文件库 + HeyGen 目录 |
| `image` | 照片、背景 | HeyGen 资产搜索（7.5 万+ 矢量）       |
| `icon`  | 图标、标志        | HeyGen 资产搜索（type=icon）          |

### 示例

```bash
# 背景音乐
node <SKILL_DIR>/scripts/resolve.mjs --type bgm --intent "upbeat tech launch" --project .
# → resolved bgm_001 → .media/audio/bgm/bgm_001.mp3 (bgm, 25s)

# 音效
node <SKILL_DIR>/scripts/resolve.mjs --type sfx --intent "whoosh" --project .
# → resolved sfx_001 → .media/audio/sfx/sfx_001.mp3 (sfx, 0.57s)

# 图片
node <SKILL_DIR>/scripts/resolve.mjs --type image --intent "gradient tech background" --project .
# → resolved image_001 → .media/images/image_001.jpg (image)

# 图标
node <SKILL_DIR>/scripts/resolve.mjs --type icon --intent "rocket" --project .
# → resolved icon_001 → .media/images/icon_001.png (icon, transparent)
```

### 标志

| 标志            | 描述                                |
| --------------- | ------------------------------------------ |
| `--type, -t`    | 媒体类型：bgm、sfx、image、icon          |
| `--intent, -i`  | 你需要的内容（自然语言）           |
| `--entity, -e`  | 用于缓存匹配的实体名称（可选）  |
| `--project, -p` | 项目目录（默认：当前目录）             |
| `--adopt`       | 批量导入现有资产到清单 |
| `--json`        | 输出 JSON 而非一行结果     |

## 工作原理

1. 检查项目 `.media/manifest.jsonl` 是否有完全匹配的提示
2. 扫描现有 `assets/` 目录中未注册但匹配需求的文件
3. 检查全局缓存 `~/.media/` 是否有可复用的资产
4. 通过提供商搜索（HeyGen 音频目录、HeyGen 资产搜索）
5. 将文件冻结到 `.media/<type>/`，在清单中注册，重新生成 `index.md`

代理只收到**一行**。候选、评分、溯源信息留在磁盘上。

## 采纳现有项目

大多数 HyperFrames 项目已在 `assets/` 中有资产。media-use 采纳它们：

```bash
node <SKILL_DIR>/scripts/resolve.mjs --adopt --project .
# → adopted 9 assets from assets/
#   bgm_001 → assets/bgm/mango-fizz.mp3 (bgm, 146.6s)
#   image_001 → assets/images/avatar.jpg (image, 400×400)
```

`ffprobe` 提取真实的时长和尺寸。在 resolve 过程中，`assets/` 中匹配意图的未注册文件会自动被采纳。

## 读取库存清单

在 resolve 或 adopt 后，阅读 `.media/index.md` 获取完整库存清单：

```
# .media · 4 个资产

id         type   dur   dims       path                          description
bgm_001    bgm    25s   —          .media/audio/bgm/bgm_001.mp3  充满活力的科技发布
sfx_001    sfx    0.6s  —          .media/audio/sfx/sfx_001.mp3  嗖声
image_001  image  —     1920×1080  .media/images/image_001.jpg   渐变科技背景
icon_001   icon   —     200×200    .media/images/icon_001.png    火箭
```

## 跨项目复用

资产在 resolve 时自动缓存。相同提示的后续 resolve 会命中 `~/.media/` 的全局缓存 — 无需重新下载，无需提供商调用。使用 `organize --promote <id>` 显式推广资产，使其可在所有项目中复用。

## 文件

- `.media/manifest.jsonl` — 机器单一真相来源，每行一条 JSON 记录
- `.media/index.md` — 代理可读的表格（id、type、dur、dims、path、description）
- `~/.media/` — 全局跨项目复用缓存（内容寻址，SHA-256）

## 使用的 CLI 工具

| 工具      | 用途                                    | 是否必需？     |
| --------- | ------------------------------------------ | ------------- |
| `ffprobe` | 在 adopt 时探测时长、尺寸、编码器 | 是           |
| `heygen`  | 音频目录、资产搜索                | 提供商需要 |

安装 `heygen` CLI（单个静态二进制，无运行时）并认证：

```bash
curl -fsSL https://static.heygen.ai/cli/install.sh | bash   # 安装最新版到 ~/.local/bin
heygen update                                               # 如果已安装：需要 >= v0.1.6
export HEYGEN_API_KEY=<your-key>                            # 或：heygen auth login --key <key>
```

需要 **heygen >= v0.1.6** — 提供商标签使用已列入白名单的 `--headers 'X-HeyGen-Client-Source: media-use'` 标志请求，该标志在 v0.1.6 中添加。`asset search` 是一个预发布命令，从 `heygen --help` 中隐藏，但可以运行。如果 PATH 上没有 `heygen`（或没有有效密钥），提供商会向 stderr 打印一行诊断信息，resolve 会回退到"没有提供商可以解析"。
