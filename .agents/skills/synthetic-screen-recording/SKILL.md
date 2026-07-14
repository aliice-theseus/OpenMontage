---
name: synthetic-screen-recording
description: 用于 Remotion `TerminalScene` 的合成终端风格屏幕录制指南。
license: MIT
---

# 合成屏幕录制（Remotion TerminalScene）

**此技能回答的决策：** 当用户想要一个终端、CLI 工具或编码工作流的屏幕录制风格演示时 — 我是否**捕获真实桌面**（通过 `screen_recorder`、Windows-MCP、Cap 或 Playwright 进行 OS 屏幕录制），还是我是否在 Remotion 中使用 `TerminalScene` 组件**合成它**？

> **启发式判断：** 如果代理可以预先编写确切的命令/输出序列，则合成。仅在真实行为不可预测、需要真实应用 UI 或用户明确要求真实录制时才捕获实时画面。

## 为什么存在这个技能

OpenMontage 展示的 v3 版本尝试使用 Windows-MCP + `screen_recorder` 驱动 Git-Bash 窗口进行安装演示。它在窗口定位、焦点竞争和任务栏隐私问题上卡住。我们转向了**纯 Remotion 渲染** — 一个名为 `TerminalScene` 的 React 组件，它绘制一个假终端并逐字符键入命令。输出在视觉上与真实屏幕录制无法区分（相同的红绿灯窗口装饰、闪烁光标、滚动输出），但是确定性的、隐私安全的、1080p 像素完美的、并且节奏可控制到帧级别。

该组件 + 模式是此技能使其可被发现的能力。

## 何时使用合成（TerminalScene）

**是，合成当：**
- 演示是**终端 / CLI / 编码会话**，命令和输出可预测
- 用户想要精致的教程感（清晰的排版、浮动药丸标签、光标闪烁）
- 安装演示、设置演示、API 密钥配置、`make` 目标、`git clone` 流程
- 你需要与旁白紧密同步 — 每个命令必须落在特定的节拍上
- 你想要结果可重现（重新渲染获得相同的像素）
- 用户的实际桌面有私人应用/窗口可见，否则你必须裁剪

**否，捕获真实屏幕当：**
- 演示是**一个真实的应用程序 UI**，无法伪造（Figma、Photoshop、具有实时状态的 Web 应用、浏览器流程）
- 用户明确要求录制*他们*的实际屏幕
- 行为依赖于你无法脚本化的时序（流式 LLM 输出、实时网络延迟）
- 有一个仅出现在实时环境中的视觉特色（光标效果、插件弹出窗口）

**对于浏览器演示** → `playwright-recording` 技能，非此技能。
**对于真实桌面** → `screen_recorder` 工具或通过 `cap_recorder` 的 Cap。

## 组件 — `TerminalScene`

位于：`remotion-composer/src/components/TerminalScene.tsx`
从：`remotion-composer/src/components/index.ts` 导出
在 dispatch 中接入：`remotion-composer/src/Explainer.tsx`（`if (cut.type === "terminal_scene")`）

**Props：**
```ts
interface TerminalSceneProps {
  title?: string;           // 显示在窗口标题栏中
  steps: TerminalStep[];    // 时间线
  prompt?: string;          // "$"、">" 等
  accentColor?: string;     // 药丸标签 + 提示符光晕
  backgroundColor?: string;
}
```

**步骤类型：**
```ts
{ kind: "cmd",   text: string, typeSpeed?: number, holdSeconds?: number }
{ kind: "out",   text: string, holdSeconds?: number }
{ kind: "pause", seconds: number }
{ kind: "pill",  text: string, color?: string, durationSeconds?: number }
```

- `cmd` — 打印提示符，逐字符键入文本（`typeSpeed` 是每字符秒数，默认 0.035），然后保持 `holdSeconds`（默认 0.3）
- `out` — 程序输出的一行，立即揭示并带短淡入
- `pause` — 死时间。终端保持在最后一个可见状态。用来与旁白同步。
- `pill` — 非阻塞浮动徽章（右上角）。弹簧进入、保持、弹簧退出。**不**推进光标 — 下一步骤并行运行。

## 编写模式

通过向 `build_composition.py`（或你等效的 props 构建器）添加一个 cut 来编写新场景：

```python
install_steps = [
    {"kind": "pause", "seconds": 7.0},                 # 等待介绍旁白
    {"kind": "cmd", "text": "git clone https://github.com/calesthio/OpenMontage.git",
     "typeSpeed": 0.045, "holdSeconds": 0.3},
    {"kind": "out", "text": "Cloning into 'OpenMontage'..."},
    {"kind": "out", "text": "remote: Enumerating objects: 2847, done."},
    {"kind": "pill", "text": "repo cloned", "color": "#34D399", "durationSeconds": 2.6},
    {"kind": "pause", "seconds": 3.8},                 # 桥接到下一个旁白提示
    # ...
]

cuts.append({
    "id": "install-terminal",
    "type": "terminal_scene",
    "terminalTitle": "bash — OpenMontage setup",
    "prompt": "$",
    "accentColor": "#22D3EE",
    "steps": install_steps,
    "in_seconds": 50.0,
    "out_seconds": 110.0,
})
```

## 规则：与旁白同步，绝不超前

**#1 失败模式：** 步骤连续运行，在场景的前 40% 就耗尽所有内容，终端在剩余 60% 冻结。这就是 v3 首次通过失败的原因 — 能力菜单在 t=80s 渲染但旁白直到 t=92s 才宣布它。

**改为这样做：**

1. **知道你的旁白提示** — 对每个场景，写下每个旁白片段开始的精确视频时间。
2. **以停顿开始** — 在任何命令键入之前达到第一个旁白提示。
3. **将每个命令计时到与其旁白行对齐** — `cmd` 应在旁白说出其行的时刻开始键入，而不是之前。
4. **在命令组之间放置停顿** — 桥接到下一个旁白提示。
5. **以结尾保持结束** — 停顿足够长，使最终状态在旁白结束后可读。

**在渲染前检查步骤是否符合预期** — Remotion 每分每秒的渲染都很宝贵。求和步骤持续时间并验证它们等于场景时长：

```python
import math
def trace(steps, scene_start, fps=30):
    t = 0.0
    for s in steps:
        k = s["kind"]
        if k == "cmd":
            tf = math.ceil(len(s["text"]) * s.get("typeSpeed", 0.035) * fps)
            t += tf / fps + s.get("holdSeconds", 0.3)
        elif k == "out":
            t += max(2, math.ceil(0.08 * fps)) / fps + s.get("holdSeconds", 0.15)
        elif k == "pause":
            t += s["seconds"]
        # "pill" 是非阻塞的 — 不推进光标
        print(f"  {t + scene_start:6.2f}s  {k}: {s.get('text', '')[:40]}")
trace(install_steps, 50)
```

查看输出列。每个旁白提示的视频时间必须与它宣布的命令/输出相邻。如果一个命令在其提示前或后 10 秒出现，调整停顿。

参见 `lib/verify_scene_pacing.py` 获取此脚本的可复用版本。

## 设计规则（继承自 v3 重新调整）

- **介绍停顿** — 每个终端场景以至少 2 秒的空终端带闪烁光标开始，之后才键入任何内容。观众需要识别窗口。
- **药丸标签时机** — 药丸标签应在屏幕上其命名事件完成的精确时刻触发（例如 `repo cloned` 紧接在最后一行 `Receiving objects` 之后）。药丸标签是真实世界 UI 通知的替代品。
- **键入后的命令保持** — 在每个 `cmd` 上保持 `holdSeconds` ≥ 0.3，使观众在第一个输出滚入之前识别完成的命令。
- **输出节奏** — 输出行的 `holdSeconds` 间隔在 0.4 和 1.0 之间。输出太快感觉像 bug；输出太慢感觉无聊。
- **自动滚动有效** — 终端保持最近的 18 行。不用担心屏幕外内容。
- **光标仅在最新命令行上键入时闪烁，并在键入完成后约 0.2s 尾巴**。

## `ProviderChip`（配套组件）

`.agents/skills/synthetic-screen-recording` 模式还拥有 `ProviderChip` — 一个旋转徽章覆盖层，以固定节奏循环遍历提供商名称列表。在 v3 展示中使用，用于在"生成的运动"部分循环通过所有 11 个 AI 视频生成提供商。

```python
overlays.append({
    "type": "provider_chip",
    "providers": ["Veo 3.1", "Seedance 2.0", "Kling 2.5", ...],
    "cycleSeconds": 2.5,
    "position": "bottom-right",
    "accentColor": "#22D3EE",
    "label": "generated with",
    "in_seconds": 195.0,
    "out_seconds": 222.5,
})
```

在 dispatch 中接入：`remotion-composer/src/Explainer.tsx` 覆盖层渲染器（`overlay.type === "provider_chip"`）。

## 添加新的合成 UI 组件

该模式可泛化。当你需要伪造另一个 UI 表面（Claude Code 聊天气泡、Jira 工单视图、GitHub PR diff、Slack 消息、VS Code 状态栏）时：

1. 复制 `TerminalScene.tsx` 作为模板。
2. 为相关的时间线基元定义一个 `steps` 接口。
3. 通过将 `frame` 与累计开始/结束时间插值来渲染每个步骤。
4. 在 `Explainer.tsx` 的 `SceneRenderer` dispatch 中用新的 `cut.type` 接入。
5. 将类型添加到 `Explainer.tsx` 的 `Cut` 接口和 `components/index.ts`。
6. 在此技能中添加一个部分进行文档记录。
7. 用新的 cut 类型更新 `remotion-composer/SCENE_TYPES.md`。

## 相关技能

- `.agents/skills/remotion` — 通用的 Remotion 编写（钩子、弹簧、序列）
- `.agents/skills/playwright-recording` — 用于 Web 应用的实时浏览器流程捕获
- `tools/capture/screen_recorder` — 基于 FFmpeg 的桌面捕获
- `tools/capture/cap_recorder` — Cap.so 精致的桌面捕获
- `skills/pipelines/screen-demo/asset-director.md` — 在屏幕演示项目中选择合成还是真实

## 溯源

引入时间：OpenMontage 展示 v3 渲染（2026-04-16）。最初动机：v3 设置演示部分需要一个 60 秒的安装演示，其中每个命令与 Chirp 3 HD 旁白提示对齐，而 Windows-MCP 驱动的真实捕获在实践中太不稳定。参见 `projects/openmontage-showcase/build_composition.py` 获取参考实现。
