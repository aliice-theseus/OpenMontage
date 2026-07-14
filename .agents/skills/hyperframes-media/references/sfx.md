# 音效（SFX）

命名的音效，由共享音频引擎（`scripts/audio.mjs` → `scripts/lib/sfx.mjs`）生成。**由引擎的一个开关根据提供商决定**——是否存在 HeyGen 凭证，一次性决定（不是每个提示单独决定）：

- **存在 HeyGen 凭证 → 从 HeyGen 音频库检索每个提示**（`/v3/audio/sounds`、`type=sound_effects`、`min_score=0.4`）。搜索并下载，**不是**生成。不会查询内置库。
- **无凭证 → 内置的 21 文件库**（`assets/sfx/` + `manifest.json`）：匹配每个提示名称，将匹配的文件复制到项目中。离线、确定、免费。

没有 `npx hyperframes sfx` 命令。SFX 从不生成——它是在线检索或从内置库获取（离线）。

## 提示 — 请求 → 元数据

每一行命名它想要的效果：`lines[].sfx: ["whoosh", "ui click"]`。引擎将这些展平为提示，根据开关解析它们，去重相同的 `(id, name)` 对（同一个效果命名两次只下载/复制一次），并写入 `audio_meta.sfx[]`：

```jsonc
{
  "id": "3",                       // 将提示连接到调用方的模型（帧/场景/段落）
  "name": "whoosh",
  "file": "assets/sfx/whoosh.mp3", // 已下载或复制，相对于项目根目录
  "source": "heygen" | "local",    // 哪个路径解析了它
  "offset_s": 0,                   // 从该行开始的延迟
  "duration_s": 0.57,
  "volume": 0.35                   // SFX 位于语音 + BGM 下方
}
```

没有匹配的提示被**跳过**（记录为异常）；SFX 从不阻塞渲染。

## HeyGen 检索（有凭证）

`searchSounds(name, "sound_effects", { limit: 3, minScore: 0.4 })` → 最佳命中 → `assets/sfx/<slug>.mp3`。结果按 `score` 排序（每个结果都带有预签名的 `audio_url`、`duration`、`description`）。最低分数为 **0.4**，因为好的 SFX 命中得分约为 0.5–0.67——低于 API 默认的 `0.7`，那会静默丢弃大多数命名的提示（只有 whoosh/swoosh 系列能通过 0.7）。`duration_s` 来自结果（否则为 1.0）。具体命名效果（`glass shatter`，不要用 `dramatic sound`）；模糊的查询会返回较差的匹配。

## 内置库（无凭证）

`assets/sfx/` 中的 21 个精选文件，由 `manifest.json` 索引——每个键有 `{ file, duration, description }`（例如 `whoosh`、`pop`、`click`、`chime`、`riser`、`impact-bass-1`、`glitch-1`、`typing`……）。提示名称通过**清单键、文件基名或 slug** 解析，因此 `whoosh`、`whoosh.mp3` 或 `"ui click"`（→ slug）都能匹配。匹配的文件被复制到项目的 `assets/sfx/`；`duration_s` 来自清单，因此时序**离线**已知——例如 `riser` 是 10.03s，所以应在 `climax − 10.03s` 触发它。清单的 `description` 字段包含每个效果的放置提示；阅读 `assets/sfx/manifest.json` 获取完整集合和使用说明。

## 规则

- **音量约 0.35。** SFX 必须位于叙述和 BGM 之下，不能与之争抢。
- **无匹配 → 跳过，不要失败。** 缺失的效果记录异常并继续；从不阻塞渲染。
- **检索（有凭证）或内置库（离线）——从不生成。** 你通过文本搜索 HeyGen，或将名称与 21 文件清单匹配。
- **每个不同名称一个资源。** 跨行重复使用去重为一次下载/复制，多个提示共享。
- **开关是全局的，不是每个提示的。** 有凭证时，检索甚至处理长尾效果（不在 21 个中的）；没有凭证时，只有 21 个捆绑的名称能解析。
