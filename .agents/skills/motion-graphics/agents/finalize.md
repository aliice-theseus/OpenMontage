# 最终化/修复（子代理）

快照视觉 QA + 一次原地修复 + 渲染。仅在 Step 6 的 `lint`/`inspect` 报告问题，或需要执行最终渲染时调用。

## 调度上下文

`SKILL_DIR`/`PROJECT_DIR`/`渲染质量: draft|standard|high`/快照时间/`lint`+`inspect` 尾部输出（如有）。

## 流程

1. **快照** — `npx hyperframes inspect . --at <节拍时间>`；目测检查：溢出/出画、文字碰撞、空白帧、错误内容、不易读的动画。
2. **一次原地修复** — `Edit` `compositions/index.html` 修复可见问题。**切勿更改固定的 `data-duration`**（时间由上游设定；更改它会破坏组装）。重新运行 `lint`/`inspect`。
3. **渲染** — `(cd "$PROJECT_DIR" && npx hyperframes render . --skill=motion-graphics -q <quality> -o ./renders/video.mp4)`（为透明覆盖层导出添加 `--format webm`）。验证 mp4 存在 + 时长匹配。

## 停止 / 升级

仅当镜头**根本上错误**（整个内容偏离，需要重新合成）时 — 返回第3/4步（重新设计 + 重新构建），不要靠编辑强推。小修复绝不升级。
