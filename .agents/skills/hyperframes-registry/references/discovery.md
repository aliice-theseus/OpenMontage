# 注册表发现

## 读取注册表清单

顶层 `registry.json` 列出所有可用项：

```bash
curl -s https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry/registry.json
```

每个条目有 `name` 和 `type`（`hyperframes:example`、`hyperframes:block` 或 `hyperframes:component`）。

## 读取项的清单

每个项有一个 `registry-item.json`，包含完整元数据：

```
<base>/<type-dir>/<name>/registry-item.json
```

其中 `<type-dir>` 是 `examples`、`blocks` 或 `components`。

## 项清单字段

| 字段 | 类型 | 必需 | 描述 |
| ---------------------- | -------- | -------- | ---------------------------------------------- |
| `name` | string | 是 | 短横线命名标识符 |
| `type` | string | 是 | `hyperframes:block` 或 `hyperframes:component` |
| `title` | string | 是 | 人类可读标题 |
| `description` | string | 是 | 一行描述 |
| `tags` | string[] | 否 | 过滤标签（例如 `["data", "chart"]`） |
| `dimensions` | object | 块 | `{ width, height }`——仅块 |
| `duration` | number | 块 | 时长（秒）——仅块 |
| `files` | array | 是 | 要安装的文件（`path`、`target`、`type`） |
| `registryDependencies` | string[] | 否 | 依赖的其他注册表项 |

## 可用项

### 块

获取最新列表请运行 `npx hyperframes catalog --type block`。下表将 97 个块按分类分组。**块名 ≠ 着色器名**：着色器过渡块（例如 `domain-warp-dissolve`）包装了一个 HyperShader 运行时，其内部名称省略了 `-dissolve`/`-warp` 后缀——参见与块一起安装的展示 HTML 以获取规范名称。

#### 着色器过渡（14）

单个着色器块；每个安装一个 HyperShader 运行时 + 一个展示作品。每个视频使用 ≤2 个。

| 名称 | 描述 |
| ------------------------ | ------------------------------------------------------------------------ |
| `chromatic-radial-split` | 色差径向分割 |
| `cinematic-zoom` | 戏剧性缩放模糊 |
| `cross-warp-morph` | 交叉扭曲变形 |
| `domain-warp-dissolve` | 分形噪点域扭曲 |
| `flash-through-white` | 白色闪光交叉淡入淡出（很少是中性的默认——参见 SKILL.md 指南） |
| `glitch` | 数字故障伪影 |
| `gravitational-lens` | 引力透镜扭曲 |
| `light-leak` | 电影感漏光叠加 |
| `ridged-burn` | 脊状湍流烧灼 |
| `ripple-waves` | 同心波纹扭曲 |
| `sdf-iris` | 有符号距离场虹膜揭示 |
| `swirl-vortex` | 漩涡扭曲 |
| `thermal-distortion` | 热雾热扭曲 |
| `whip-pan` | 快速相机甩镜 |

#### 社交叠加（7）

平台可识别的 UI 叠加。盖印在节拍上或用作节拍结尾。

| 名称 | 描述 |
| -------------------- | ------------------------------------------------ |
| `instagram-follow` | 个人资料卡 + 关注按钮 |
| `tiktok-follow` | 个人资料卡 + 关注按钮 |
| `yt-lower-third` | YouTube 订阅下方三分之一带虚拟形象 |
| `x-post` | X/Twitter 帖子卡带互动指标 |
| `reddit-post` | 帖子卡带赞和评论 |
| `spotify-card` | 正在播放卡片带专辑封面和进度条 |
| `macos-notification` | macOS 风格横幅带应用图标和消息 |

### 组件

| 名称 | 描述 | 标签 |
| -------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| `grain-overlay` | 动画胶片颗粒纹理叠加 | texture、grain、overlay、film |
| `shimmer-sweep` | 用于 AI 强调的 CSS 渐变光扫 | text、shimmer、highlight、effect |
| `morph-text` | 粘性文本变形循环可编辑词列表（SVG 阈值 + GSAP 模糊） | text、text-effect、typography、morph、gooey |
| `grid-pixelate-wipe` | 场景间的网格溶解过渡 | transition、wipe、grid、pixelate |
| `parallax-zoom` | 中心卡片放大填满画面，同时兄弟元素向外视差（单个 `--pz-progress` 0→1） | transition、zoom、parallax、grid、hero |
| `parallax-unzoom` | `parallax-zoom` 的反向——聚焦卡片从全屏缩小，兄弟元素视差进入 | transition、reveal、unzoom、parallax、grid、hero |
