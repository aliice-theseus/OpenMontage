# 第 4 层 — 逃生舱

## 测试内容

T4 是**仅 lint** 层级。无需渲染进行差异比较 — 技能的评分基于它是否能正确_拒绝_翻译每个案例（并推荐来自 PR #214 的运行时互操作模式），或者在适当情况下，在丢弃警告级别的装饰后进行翻译。

每个 `cases/*.tsx` 文件是一个最小的 Remotion 合成，演示一个特定模式。技能应：

1. 对源码运行 `scripts/lint_source.py`。
2. 将 JSON 输出与该案例的 `expected.json` 进行比较。
3. 执行文档化的 `skill_action`：
   - `refuse_translation_recommend_interop` — 打印理由 + PR #214 互操作指南的链接；不产生 HF 输出。
   - `drop_lambda_code_translate_remainder_if_clean` — 丢弃 `@remotion/lambda` 代码并附注说明；仅在没有其他阻断器时翻译其余部分。
   - `translate_after_dropping_wrappers` — 正常翻译；丢弃 `useCallback` / `useMemo` / `delayRender` 包装器。
   - `inline_hook_body_if_pure` — 如果是 `useCurrentFrame` 的纯推导，内联自定义 hook 的函数体；否则退出。

## 案例

| #   | 文件                       | 预期发现                             | 说明                                           |
| --- | -------------------------- | ------------------------------------ | ----------------------------------------------- |
| 01  | `01-use-state.tsx`         | 阻断器 `r2hf/use-state`              | useState 驱动动画                                |
| 02  | `02-use-effect-deps.tsx`   | 阻断器 `r2hf/use-effect-deps`        | useEffect/useLayoutEffect 带非空依赖             |
| 03  | `03-async-metadata.tsx`    | 阻断器 `r2hf/async-metadata`         | calculateMetadata 返回 Promise                   |
| 04  | `04-third-party-react.tsx` | 阻断器 `r2hf/third-party-react-ui`   | 导入 `@mui/material`                             |
| 05  | `05-lambda-config.tsx`     | 警告 `r2hf/lambda-import`            | 导入 `@remotion/lambda` — 丢弃，翻译             |
| 06  | `06-warnings-only.tsx`     | 仅警告                               | delayRender / useCallback / useMemo              |
| 07  | `07-custom-hook.tsx`       | 警告 `r2hf/custom-hook`              | 本地定义的 `useFadeIn`（export const 形式）       |
| 08  | `08-mixed.tsx`             | 3 个阻断器 + 1 个警告                 | 聚合发现测试                                      |

## 验证

```bash
./validate.sh
```

脚本对每个案例运行 `lint_source.py` 并断言：

- 每个预期的阻断器规则以 `blocker` 严重性触发。
- 每个预期的警告规则以 `warning`（或更强）严重性触发。
- 当预期有阻断器时，`lint_source.py` 的退出码为 1，否则为 0。

当每个案例匹配其预期输出时，T4 通过。不涉及渲染。
