# 质量验证计划——阶段 3.5 + G3.11

## 目的

使用真实的 API 密钥运行每个工具，检查输出（查看图片、收听音频、观看视频），发现差距并修复。这是在将阶段 3.5 标记为"已验证"之前的关卡。

## 测试脚本（均已准备好运行）

| 脚本 | 测试的工具 | 使用的 API 密钥 | 预估成本 |
|------|----------|---------------|---------|
| `test_01_tts.py` | `elevenlabs_tts`（ElevenLabs） | ELEVENLABS_API_KEY | ~¥0.02 |
| `test_02_image_gen.py` | `image_gen`（DALL-E 3 + FLUX） | OPENAI_API_KEY | ~¥0.15 |
| `test_03_music.py` | `music_gen`（ElevenLabs） | ELEVENLABS_API_KEY | ~¥0.10 |
| `test_04_audio_mix.py` | `audio_mixer` | 无（仅 ffmpeg） | ¥0 |
| `test_05_video_compose.py` | `video_compose` | 无（仅 ffmpeg） | ¥0 |
| `test_06_video_stitch.py` | `video_stitch` | 无（仅 ffmpeg） | ¥0 |
| `test_07_playbook_intelligence.py` | `playbook_loader.py` 函数 | 无（纯 Python） | ¥0 |
| `test_08_end_to_end.py` | 完整动画讲解流水线 | 无（ffmpeg 固定数据） | ¥0 |

## 检查协议

对于每个输出：
1. **音频文件**：使用 `ffprobe` 检查格式/时长/声道数，然后**收听**（在媒体播放器中播放或使用 Whisper 验证内容与提示匹配）
2. **图片文件**：使用 `ffprobe` 检查尺寸，然后**查看**（打开图片，检查构图、文字可读性、风格匹配）
3. **视频文件**：使用 `ffprobe` 检查分辨率/帧率/时长/编码，然后**观看**（检查音视频同步、转场、字幕时间）
4. **设计智能**：对所有 3 个剧本书运行，验证对比度与手动计算匹配，检查 CVD 警告是否准确

## 已知风险区域

| 区域 | 风险 | 如何验证 |
|------|------|---------|
| TTS 语音选择 | 默认语音可能与剧本书情绪不匹配 | 使用多个语音 ID 测试，与剧本书 `voice_style` 对比 |
| 图像生成一致性 | DALL-E/FLUX 输出因提示而异 | 测试时附加剧本书 `image_prompt_prefix` |
| 音乐时长对齐 | 音乐可能与旁白时长不匹配 | 比较 `music.duration` 与 `tts.duration`，检查填充/循环 |
| 音频闪避时机 | 闪避可能过度削减音乐 | 检查波形：音乐应在语音下闪避约 6dB，平滑恢复 |
| 视频拼接转场 | 交叉淡化可能因编码不匹配而闪烁 | 使用匹配和不匹配的片段测试，检查 `auto_normalize` |
| 字幕烧录 | 字体大小/位置可能在移动端格式上裁剪 | 使用 9:16（TikTok）和 16:9（YouTube）配置文件测试 |
| Remotion 渲染 | 组件可能因真实数据而失败 | 使用所有 8 个组件构建测试合成，以 1080p 渲染 |
| 剧本书对比度 | 深色上深色或浅色上浅色主题的边界情况 | 使用所有 3 个剧本书 + 一个故意低对比度的自定义剧本书测试 |

## 运行顺序

```bash
cd C:/Users/ishan/Documents/OpenMontage

# 阶段 1：单个工具（可以并行运行）
python tests/qa/test_01_tts.py
python tests/qa/test_02_image_gen.py
python tests/qa/test_03_music.py

# 阶段 2：合成（依赖阶段 1 的输出）
python tests/qa/test_04_audio_mix.py
python tests/qa/test_05_video_compose.py
python tests/qa/test_06_video_stitch.py

# 阶段 3：智能验证（无 API 调用）
python tests/qa/test_07_playbook_intelligence.py

# 阶段 4：完整流水线
python tests/qa/test_08_end_to_end.py
```

## 成功标准

- [ ] 所有 3 个 TTS 样本：清晰的语音、正确的内容、无伪影、≥44.1kHz
- [ ] 所有 4 张图片：匹配提示意图、正确的尺寸、无水印、良好的构图
- [ ] 两个音乐曲目：匹配情绪提示、正确的时长（±2s）、无突兀的剪切
- [ ] 音频混音：语音明显高于音乐、闪避平滑、无削波
- [ ] 视频合成：音视频同步误差在 50ms 以内、正确的分辨率、可在 VLC 中播放
- [ ] 视频拼接：平滑转场、无丢帧、画中画正确定位
- [ ] 剧本书智能：所有 3 个剧本书通过 a11y 检查、对比度与手动计算偏差在 0.1 以内
- [ ] 端到端：60 秒讲解视频无错误渲染、所有阶段正确设置检查点
