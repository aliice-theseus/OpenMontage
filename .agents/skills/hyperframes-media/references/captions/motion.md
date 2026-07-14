# 动态字幕技术

你来到这里是因为 SKILL.md 告诉你在编写动画代码之前先阅读此文件。根据你从转录中检测到的能量水平，从下表中选择你的技术组合，然后使用标准 GSAP 模式实现。

## 按能量选择技术

| 能量级别 | 高亮 | 退出 | 循环模式 |
| ------------ | ------------------------------------- | ------------------- | ----------------------------------------- |
| 高 | 卡拉 OK 带强调光晕 + 缩放弹出 | 散射或下落 | 每 2 组交替高亮样式 |
| 中高 | 卡拉 OK 带颜色弹出 | 散射或折叠 | 每 3 组交替 |
| 中 | 卡拉 OK（微妙，仅白色） | 淡出 + 滑动 | 每 3 组交替 |
| 中低 | 卡拉 OK（最小缩放变化） | 淡出 | 单一风格，每组变化缓动方式 |
| 低 | 卡拉 OK（暖色调，慢过渡） | 折叠 | 每 4 组交替 |

**所有能量级别都以卡拉 OK 高亮为基础。** 区别在于强度——高能量在活跃词语上使用强调色 + 光晕 + 15% 缩放弹出，低能量使用温和的白色偏移和 3% 缩放。

**强调词总是打破模式。** 当一个词被标记为强调（情感关键词、全大写、品牌名），给它一个比周围词语更强的动画（更大的缩放、强调色、过冲缓动）。这创造了对比。

**标记高亮模式在卡拉 OK 之上添加视觉层。** 对于需要超越颜色/缩放的强调词，添加标记风格效果：高亮扫光、圆形、爆发、涂鸦或草图轮廓。参见 `hyperframes-animation/rules/css-marker-patterns.md` 了解实现细节。模式与能量匹配：爆发用于 hype，圆形用于关键术语，高亮用于标准，涂鸦用于微妙。

## 音频响应字幕（音乐时强制性）

**如果源音频是音乐（带伴奏的人声、节拍、任何音乐内容），你必须提取音频数据并添加音频响应动画。** 这不是可选的——没有音频响应的音乐看起来脱节。即使是低能量的抒情歌曲也能得到微妙的贝斯脉冲和高音光晕。

不需要特殊的连接。组循环已经遍历每个字幕组来构建入场、卡拉 OK 和退出动画。此时，读取每组时间范围的音频数据，并用常规 GSAP 动画来调节组的动画强度。

```js
// 内联加载音频数据（与 TRANSCRIPT 相同模式）
var AUDIO = JSON.parse(audioDataJson); // { fps, totalFrames, frames: [{ bands: [...] }] }

GROUPS.forEach(function (group, gi) {
  var groupEl = document.getElementById("cg-" + gi);
  if (!groupEl) return;

  // 读取此组时间范围的峰值能量
  var startFrame = Math.floor(group.start * AUDIO.fps);
  var endFrame = Math.min(Math.floor(group.end * AUDIO.fps), AUDIO.totalFrames - 1);
  var peakBass = 0;
  var peakTreble = 0;
  for (var f = startFrame; f <= endFrame; f++) {
    var frame = AUDIO.frames[f];
    if (!frame) continue;
    peakBass = Math.max(peakBass, frame.bands[0] || 0, frame.bands[1] || 0);
    peakTreble = Math.max(peakTreble, frame.bands[6] || 0, frame.bands[7] || 0);
  }

  // 调节入场——更响亮的组进入时更大、更有光晕
  tl.to(
    groupEl,
    {
      scale: 1 + peakBass * 0.06,
      textShadow:
        "0 0 " + Math.round(peakTreble * 12) + "px rgba(255,255,255," + peakTreble * 0.4 + ")",
      duration: 0.3,
      ease: "power2.out",
    },
    group.start,
  );

  // 在退出时重置，使音频驱动的值不会持续
  tl.set(groupEl, { scale: 1, textShadow: "none" }, group.end - 0.15);
});
```

这是在构建时塑造动画，而不是播放时——没有逐帧回调，没有 `tl.call()` 循环，没有异步获取时序问题。响亮的组进入时更有重量和光晕；安静的组柔和进入。音频数据调节的是**程度**，内容决定的是**内容**。

保持音频响应微妙——3-6% 的缩放变化和柔和的光晕。重脉冲会使文本不可读。

要生成音频数据文件：

```bash
python3 skills/hyperframes-creative/scripts/extract-audio-data.py audio.mp3 --fps 30 --bands 8 -o audio-data.json
```

## 组合技术

不要在每组上使用相同的高亮动画——使用组索引在样式之间循环。不要在同一时间戳的同一个词上组合多个相互冲突的动画。根据内容节奏变化跨组的技术。

**标记高亮效果**与卡拉 OK 搭配良好——使用卡拉 OK 逐词揭示，然后只在强调词上添加标记效果。例如：卡拉 OK 以白色高亮每个词，但品牌名获得黄色高亮扫光，统计数字获得红色圆圈。跨组循环标记模式以获得视觉多样性。

## 运行时工具

字幕动画使用标准的 HyperFrames 运行时 API。使用规范来源：

- **GSAP 时间线 + 动画语法**——`hyperframes-animation/adapters/gsap.md`（缓动、位置参数、性能）
- **`window.__hyperframes.fitTextFontSize` / `pretext`**——`hyperframes-core/references/determinism-rules.md` → 布局约定（溢出预防、逐帧文本测量）
- **音频数据提取**——通过 `python3 skills/hyperframes-creative/scripts/extract-audio-data.py audio.mp3 --fps 30 --bands 8 -o audio-data.json` 生成，然后如上面的「音频响应字幕」所示内联加载
