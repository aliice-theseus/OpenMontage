# lambda — 在 AWS Lambda 上云端渲染

将 HyperFrames 分布式渲染部署到 AWS Lambda，并从您的笔记本或 CI 驱动渲染。封装了 `@hyperframes/aws-lambda` SDK 和 AWS SAM。端到端三步：

```bash
npx hyperframes lambda deploy
npx hyperframes lambda render ./my-project --width 1920 --height 1080 --wait
npx hyperframes lambda destroy
```

## 何时使用 Lambda 与本地渲染

- **本地 `render`** — 开发循环迭代，单台主机，几分钟以内的 1080p 内容。
- **`lambda render`** — 长视频、4K、大型并行批次，或本地 Chrome 会超时/耗尽 RAM 的任何情况。按调用付费，无空闲成本。

对于一次性短渲染，Lambda 不值得部署开销。

## 先决条件

- 已配置 AWS 凭证（环境变量、`~/.aws/credentials`、SSO 或 IMDS）。
- `PATH` 中有 AWS SAM CLI。
- `PATH` 中有 `bun`（构建 Lambda 处理程序 ZIP）。

## 子命令

### deploy

```bash
npx hyperframes lambda deploy \
  --stack-name=hyperframes-prod \
  --region=us-east-1 \
  --concurrency=8 \
  --memory=10240
```

构建 `packages/aws-lambda/dist/handler.zip` 并通过 SAM 部署堆栈（Lambda + Step Functions + S3 + IAM）。幂等——在同一 `--stack-name` 上重新运行时，如果无变化则不做任何操作。写入 `<cwd>/.hyperframes/lambda-stack-<name>.json`，以便后续子命令无需调用 `describe-stacks`。

| 标志             | 默认值                            | 描述                    |
| ---------------- | --------------------------------- | ----------------------- |
| `--stack-name`   | `hyperframes-default`             | CloudFormation 堆栈名称 |
| `--region`       | `AWS_REGION` 环境变量或 `us-east-1` | AWS 区域                |
| `--profile`      | `AWS_PROFILE` 环境变量            | 命名 AWS 凭证配置文件   |
| `--concurrency`  | `8`                               | Lambda 预留并发数       |
| `--memory`       | `10240`                           | Lambda 内存（MB）       |
| `--skip-build`   | 关闭                              | 重用现有的 `handler.zip` |

### sites create

```bash
npx hyperframes lambda sites create ./my-project
# → siteId: abc1234deadbeef0  (同一目录树重复运行结果稳定)

npx hyperframes lambda render ./my-project --site-id=abc1234deadbeef0 ...
```

将 `<projectDir>` 打包并上传到 S3，使用内容寻址键。返回一个稳定的 `siteId` 可重复使用——相同目录树的重新渲染会跳过上传。

### render

```bash
npx hyperframes lambda render ./my-project \
  --width 1920 --height 1080 --fps 30 --format mp4 \
  --chunk-size 240 --max-parallel-chunks 16 \
  --wait
```

启动一个 Step Functions 执行。立即返回 `renderId`，除非设置了 `--wait`，此时 CLI 会阻塞直到完成并流式输出每个块的进度行。添加 `--json` 以获得机器可解析的输出。

| 标志                      | 描述                                                                                                                                                                                                                                                                               |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--width` / `--height`    | 输出尺寸（像素）                                                                                                                                                                                                                                                                   |
| `--output-resolution`     | 超采样预设（启用 Chrome `deviceScaleFactor`）——`landscape` / `landscape-4k` / `portrait` / `portrait-4k` / `square` / `square-4k`，以及别名（`1080p`、`4k`、`uhd`、`hd`、`1080p-portrait`、`4k-portrait`、`1080p-square`、`4k-square`）。用于以 4K 渲染以 1080p 创作的组合而无需重新布局——见下面的陷阱说明。 |
| `--fps`                   | `24` / `30` / `60`                                                                                                                                                                                                                                                               |
| `--format`                | `mp4` / `mov` / `png-sequence`（默认 `mp4`）                                                                                                                                                                                                                                      |
| `--codec`                 | `h264` / `h265`（仅 mp4）                                                                                                                                                                                                                                                          |
| `--quality`               | `draft` / `standard` / `high`                                                                                                                                                                                                                                                      |
| `--chunk-size`            | 每块帧数（默认 `240`）                                                                                                                                                                                                                                                            |
| `--max-parallel-chunks`   | 最大并发块数（默认 `16`）                                                                                                                                                                                                                                                         |
| `--site-id`               | 重用现有站点（跳过上传）                                                                                                                                                                                                                                                           |
| `--wait`                  | 阻塞直到完成，流式输出进度                                                                                                                                                                                                                                                         |
| `--json`                  | 机器可解析的进度快照                                                                                                                                                                                                                                                               |

**`--width` / `--height` 陷阱。** 对 `data-width="1920"` 的组合设置 `--width 3840 --height 2160` 会静默产生 1080p——运行时按组合创作的尺寸布局页面，CLI 标志在布局中被忽略。要实际输出 4K，请使用 `--output-resolution 4k`（通过 `deviceScaleFactor` 超采样）。当 CLI 尺寸与组合的 `data-width` / `data-height` 不一致且未设置 `--output-resolution` 时，CLI 现在会打印警告；当 `--json` 开启或 `index.html` 不在磁盘上时（`--site-id` 流程），警告被抑制。

### progress

```bash
npx hyperframes lambda progress hf-render-abcd1234
npx hyperframes lambda progress arn:aws:states:us-east-1:...:execution:...
```

打印一次快照——总体百分比、已渲染帧数、Lambda 调用次数、累计成本以及任何错误。接受纯 `renderId`（根据堆栈的状态机 ARN 解析）或完整的 SFN 执行 ARN。

### destroy

```bash
npx hyperframes lambda destroy
```

调用 `sam delete --no-prompts` 并删除本地状态文件。**渲染 S3 存储桶配置为 `Retain`（保留）**，因此它在堆栈销毁后仍然存在——如果您想要回收存储空间，可通过 AWS 控制台/CLI 清空并删除它。

### 不可重试的错误

Step Functions 状态机绕过其 4×15 分钟重试预算而直接短路的失败子集。`progress` 会立即显示这些错误及其错误类名；看到这些错误时不要盲目重新发出 `lambda render`。

- **`ChromeBinaryUnavailableError`**——`@sparticuz/chromium` 返回了空的/缺失的可执行文件路径。前一个块在提取过程中遇到了 `Sandbox.Timedout`，导致热实例被卡住，直到执行环境回收。解决方法：修改一个 Lambda 环境变量（强制新建执行环境）或再次 `lambda deploy`。这不是临时渲染失败；重试会在同一个卡住的实例上浪费预算。
- **`FFMPEG_VERSION_MISMATCH`** / **`PLAN_HASH_MISMATCH`**——规划器/执行器版本偏移。重新部署。

### policies

打印或验证 CLI 所需的最小 IAM 权限。

```bash
npx hyperframes lambda policies user                                  # IAM 用户的内联策略
npx hyperframes lambda policies role --principal=cloudformation       # { TrustRelationship, InlinePolicy }
npx hyperframes lambda policies validate ./infra/iam/hf-deploy.json   # CI 门控
```

`validate` 读取 JSON 策略文档，检查其 `Effect: Allow` 操作的并集（扩展 `s3:*` / `s3:Get*` / `*` 通配符）是否覆盖 CLI 所需的操作集。缺失的操作打印到 stderr；命令退出码非零。在 CI 中配置它，以便在下一次部署失败前捕获策略漂移。

默认操作集故意较宽（`Resource: "*"`），因为 CloudFormation 在每个采用者的首次部署时创建新的 ARN。首次运行后，如果安全要求需要，可以收紧 `Resource`。

## 状态文件

`hyperframes lambda` 在 `<cwd>/.hyperframes/lambda-stack-<name>.json` 中存储每堆栈的元数据（存储桶名称、状态机 ARN、区域）。不是机密，但可标识 AWS 账户。可提交到代码仓库或根据工作流将其加入 `.gitignore`。

## 成本和清理

- `lambda destroy` 移除 SAM 堆栈，但**保留 S3 存储桶**（`Retain`）。如需回收存储空间，请手动删除。
- Lambda 按调用次数 + 持续时间计费。`progress` 报告累计成本。
- `--concurrency` 限制并行 Lambda 调用次数——请与您的账户配额保持一致。
- `--chunk-size` 和 `--max-parallel-chunks` 权衡每块开销与并行度；更大的块减少协调器开销，更小的块更积极地并行化。
