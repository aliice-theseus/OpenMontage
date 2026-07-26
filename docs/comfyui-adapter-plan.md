# OpenMontage 的 ComfyUI 提供商适配器

**RFC：用于图像和视频生成的原生 ComfyUI 后端**

---

## 动机

OpenMontage 的本地 GPU 工具（`wan_video`、`hunyuan_video`、`cogvideo_video`、`local_diffusion`）直接使用 HuggingFace `diffusers`。这在 x86 + 消费级 GPU 上可以工作，但在 PyTorch 生态尚未跟上的较新硬件上会出问题：

| 问题 | 详情 |
|------|------|
| **NVIDIA Blackwell（sm_121）** | 没有适用于 aarch64 + CUDA 13.0 的稳定 PyTorch wheel。需要 NGC 容器或 nightly 构建。 |
| **Flash Attention** | 不支持 sm_121。必须替换为 SageAttention v3 或原生 SDPA。 |
| **统一内存（GB10/DGX Spark）** | `nvidia-smi` 无法报告 VRAM。Diffusers 的内存估算会出错。 |
| **模型格式不匹配** | Diffusers 期望 HF 仓库。生产部署使用带量化变体（NVFP4、FP8）的 `.safetensors` 检查点，而 diffusers 无法原生加载。 |

ComfyUI 已经解决了所有这些问题。NVIDIA 为 DGX Spark 提供官方 ComfyUI 容器。社区已经优化了 Blackwell 的工作流（SageAttention、NVFP4 量化、LightX2V 4-step LoRA）。像 WAN 2.2、FLUX 2 和 ACE-Step 这样的模型在 diffusers 无法运行的硬件上，通过 ComfyUI 也能可靠运行。

ComfyUI 适配器使 OpenMontage 能够访问 ComfyUI 支持的任何模型，在任何 ComfyUI 可运行的硬件上，无需提供或维护 PyTorch 构建。

---

## 设计

### 架构

```
OpenMontage 代理
    |
    v
video_selector / image_selector
    |
    v
comfyui_video    comfyui_image    （新工具）
    |                |
    v                v
ComfyUI REST API  （POST /prompt, GET /history, GET /view）
    |
    v
GPU（ComfyUI 支持的任何硬件）
```

### 集成模型

两个新的 `BaseTool` 子类加一个共享客户端库：

```
tools/
  _comfyui/
    __init__.py
    client.py              # 共享的 ComfyUI REST 客户端
    workflows/             # 捆绑的工作流模板
      flux2-txt2img.json
      wan22-t2v-4step.json
      wan22-i2v-4step.json
  graphics/
    comfyui_image.py       # capability="image_generation", provider="comfyui"
  video/
    comfyui_video.py       # capability="video_generation", provider="comfyui"
```

### 注册表和选择器集成

工具将 `capability` 和 `provider` 声明为类属性。`tool_registry.discover()` 通过 `pkgutil.walk_packages` 自动发现它们。`video_selector` 和 `image_selector` 通过 `registry.get_by_capability()` 找到它们。唯一的选择器变更是在 `video_selector` 中的操作特定过滤，这样当仅安装了文生视频捆绑模型（或反之）时，ComfyUI 不会被选为 `image_to_video` 使用。

---

## 共享客户端：`tools/_comfyui/client.py`

封装了经过生产验证的 ComfyUI REST API 模式（被 Bard 项目的 Airflow DAG 用于数千次生成）：

端点契约已根据当前 ComfyUI 服务器文档和 2026 年 4 月第三方开发者指南进行了检查：

- 官方路由：`POST /prompt`、`GET /history/{prompt_id}`、`GET /view`、`POST /upload/image`、`GET /object_info/{node_class}`、`GET /models/{folder}`、`GET /system_stats` 和 `WS /ws` 是已记录的服务器路由。
- `/prompt` 接受 `prompt` 键下的 API 格式工作流，并返回 `prompt_id`、`number` 和验证时的 `node_errors`。
- `/history/{prompt_id}` 返回完成的节点输出；工件记录包括 `filename`、`subfolder` 和 `type`。客户端将所有三个参数传递给 `/view`，而不是假定 `type=output`。
- 工作流必须以 ComfyUI API 格式导出，而不是常规的可视画布工作流格式。

参考文档：

- https://docs.comfy.org/development/comfyui-server/comms_routes
- https://www.runflow.io/blog/comfyui-api-developer-guide

```python
class ComfyUIClient:
    """ComfyUI REST API 的轻量客户端。"""

    def __init__(self, server_url: str | None = None):
        self.server_url = server_url or os.environ.get(
            "COMFYUI_SERVER_URL", "http://localhost:8188"
        )

    def is_available(self) -> bool:
        """健康检查——能否到达服务器？"""

    def submit(self, workflow: dict) -> str:
        """POST /prompt。返回 prompt_id。遇 node_errors 时抛出异常。"""

    def poll(self, prompt_id: str, timeout: int = 600, interval: int = 5) -> dict:
        """GET /history/{prompt_id} 直到完成。返回 outputs 字典。"""

    def download(self, filename: str, subfolder: str, dest: Path) -> Path:
        """GET /view?filename=...&type=output。将字节写入目标路径。"""

    def upload_image(self, local_path: Path, name: str) -> str:
        """POST /upload/image。返回用于 LoadImage 节点的服务器端文件名。"""

    def generate(self, workflow: dict, output_node: str, dest: Path,
                 timeout: int = 600) -> Path:
        """完整周期：提交 -> 轮询 -> 下载。返回工件路径。"""
```

**为什么需要共享客户端？** 提交/轮询/下载循环在图像和视频生成中是相同的。唯一的区别是：使用哪个工作流模板、自定义哪些节点、以及从哪个输出节点读取。

---

## 工具规格

### `comfyui_image`——图像生成

| 字段 | 值 |
|------|-----|
| capability | `image_generation` |
| provider | `comfyui` |
| runtime | `LOCAL_GPU` |
| tier | `GENERATE` |
| stability | `EXPERIMENTAL` |
| capabilities | `text_to_image`, `image_to_image` |
| dependencies | （运行时：ComfyUI 服务器可访问） |
| fallback_tools | `openai_image`, `local_diffusion` |
| cost | `¥0.00`（本地计算） |

**捆绑工作流：** `flux2-txt2img.json`

加载带有 Mistral 文本编码器的 FLUX 2 Dev（NVFP4）。模板化节点：

| 节点 | 类 | 模板化字段 |
|------|-----|-----------|
| 4 | CLIPTextEncode | `text`（提示词） |
| 6 | EmptyFlux2LatentImage | `width`, `height` |
| 7 | RandomNoise | `noise_seed` |
| 10 | Flux2Scheduler | `steps` |
| 13 | SaveImage | `filename_prefix` |

**输入模式：**

```yaml
prompt:        string    # 必填
width:         integer   # 默认 1024
height:        integer   # 默认 1024
steps:         integer   # 默认 20
seed:          integer   # 可选（省略时随机）
guidance:      number    # 默认 3.5
output_path:   string    # 保存图像的路径
workflow_json: string    # 可选自定义工作流；需要 output_node
workflow_path: string    # 可选工作流 JSON 路径；需要 output_node
output_node:   string    # 自定义工作流时必填
workflow_name: string    # 可选自定义工作流来源标签
workflow_model: string   # 可选自定义模型/来源标签
workflow_model_stack: [] # 可选自定义依赖来源
```

**get_status()：** 对 ComfyUI 服务器进行 ping 检查，并通过 `/object_info` 检查捆绑的 FLUX 模型名称。当服务器和捆绑模型集就绪时返回 `AVAILABLE`，当服务器可达但捆绑模型缺失时返回 `DEGRADED`，当服务器不可达时返回 `UNAVAILABLE`。

**execute() 流程：**
1. 深拷贝工作流模板
2. 将提示词、种子、尺寸、步数注入模板化节点
3. `client.generate(workflow, output_node="13", dest=output_path)`
4. 返回带有工件路径、种子、模型信息的 `ToolResult`

对于自定义工作流，调用方必须提供 `workflow_json` 或 `workflow_path` 加上 `output_node`。该工具不对自定义工作流假定捆绑节点 ID，并且除非调用方提供 `workflow_model`，否则来源报告为用户提供的。结果还包括最终工作流的 SHA-256 哈希，对于捆绑工作流，还包括已知的模型栈。

---

### `comfyui_video`——视频生成

| 字段 | 值 |
|------|-----|
| capability | `video_generation` |
| provider | `comfyui` |
| runtime | `LOCAL_GPU` |
| tier | `GENERATE` |
| stability | `EXPERIMENTAL` |
| capabilities | `text_to_video`, `image_to_video` |
| dependencies | （运行时：ComfyUI 服务器可访问） |
| fallback_tools | `wan_video`, `hunyuan_video`, `ltx_video_local` |
| cost | `¥0.00`（本地计算） |

**捆绑工作流：**

1. **`wan22-i2v-4step.json`**——图生视频（WAN 2.2 14B，fp8，4-step LightX2V LoRA）
2. **`wan22-t2v-4step.json`**——文生视频（WAN 2.2 14B，fp8，4-step LightX2V LoRA）

这些捆绑的 WAN 2.2 14B FP8 工作流属于高质量配置档案，建议约 16GB VRAM。这不是 ComfyUI 整体的要求。`comfyui_video` 工具顶层的 `resource_profile` 是 8GB 提供商底限，因此预检不会暗示 ComfyUI 本身需要 16GB。低 VRAM 用户应使用自定义工作流，如 Wan 2.1 1.3B、LTX-Video/LTXV FP8 或量化图、或 Wan 2.2 GGUF/量化社区工作流，并根据需要减少帧数和降低分辨率。

**I2V 工作流——模板化节点：**

| 节点 | 类 | 模板化字段 |
|------|-----|-----------|
| 93 | CLIPTextEncode | `text`（正向提示词） |
| 97 | LoadImage | `image`（来自上传的服务器文件名） |
| 98 | WanImageToVideo | `width`, `height`, `length` |
| 86 | KSamplerAdvanced | `noise_seed` |
| 108 | SaveVideo | `filename_prefix` |

**输入模式：**

```yaml
prompt:               string    # 必填
operation:            string    # "text_to_video" | "image_to_video"（默认：t2v）
reference_image_path: string    # 本地路径（用于 i2v）
reference_image_url:  string    # URL（用于 i2v，先下载）
width:                integer   # 默认 640
height:               integer   # 默认 640
num_frames:           integer   # 默认 81（16fps 下 5 秒）
seed:                 integer   # 可选
output_path:          string    # 保存视频的路径
workflow_json:        string    # 可选自定义工作流；需要 output_node
workflow_path:        string    # 可选工作流 JSON 路径；需要 output_node
output_node:          string    # 自定义工作流时必填
workflow_name:        string    # 可选自定义工作流来源标签
workflow_model:       string    # 可选自定义模型/来源标签
workflow_model_stack: []        # 可选自定义依赖来源
```

**execute() 流程（i2v）：**
1. 通过 `client.upload_image()` 上传参考图像
2. 深拷贝 i2v 工作流模板
3. 注入提示词、上传的图像名称、种子、尺寸
4. `client.generate(workflow, output_node="108", dest=output_path, timeout=900)`
5. 返回 `ToolResult`

**execute() 流程（t2v）：**
1. 深拷贝 t2v 工作流模板
2. 注入提示词、种子、尺寸
3. `client.generate(workflow, output_node="16", dest=output_path, timeout=900)`
4. 返回 `ToolResult`

`comfyui_video` 在 `get_info()` 中发布 `operation_statuses`，并实现 `is_operation_available(operation)` 用于选择器路由。这样即使 ComfyUI 安装不完整，也能对已安装的模式有用，而不会将不可用的操作模式标记为就绪。`video_selector` 在 `operation="rank"` 时也通过使用 `target_operation` 应用此就绪检查，因此预检排名不会将 ComfyUI 推荐给其捆绑模型缺失的操作。

---

### `comfyui_music`——音乐生成（未发布）

我们曾探索使用 ACE-Step 3.5B 模型添加 `comfyui_music` 工具。该模型在 ComfyUI 中运行良好，但 ACE-Step 的 ComfyUI 节点接口尚未标准化——存在多个具有不同类名的自定义节点包（`AceStepModelLoader` 与原生 `TextEncodeAceStepAudio` 等）。提供一个仅适用于特定自定义节点包的工作流会导致大多数用户无法使用。

**未来路径：** 一旦 OpenMontage 确定了音乐生成的路由形态和可移植的 ComfyUI 音频工作流契约，应重新审视 ACE-Step 支持。当前的图像/视频工作流覆盖机制有意范围限定在图像和视频工件上，而非任意音频工作流。

---

## 工作流覆盖机制

图像和视频工具接受 `workflow_json` 或 `workflow_path`。提供时，自定义工作流完全替换捆绑模板，调用方还必须提供 `output_node`。这个更严格的契约是必需的，因为社区工作流使用任意的节点 ID。

- 使用更新的模型检查点而无需改动代码
- 自定义采样策略（不同的调度器、步数、LoRA）
- 原样放入的社区工作流
- 不同生成方法的 A/B 测试

代理还可以从 `tools/_comfyui/workflows/` 读取工作流文件，并在传递给 `execute()` 之前以编程方式修改它们。

自定义工作流结果的元数据将 `workflow_provenance.source` 报告为 `user_supplied`，并在提供时使用 `workflow_model`、`model` 或 `workflow_name` 作为模型标签。如果未提供自定义标签，模型将报告为 `custom-comfyui-workflow` 而非其中一个捆绑模型名称。来源信息还记录 `workflow_hash_sha256`。对于用户提供的工作流，调用方应在已知时提供带有基础模型、文本编码器、VAE、LoRA 及其强度、调度器、步数和引导系数的 `workflow_model_stack`。

---

## 代理技能和设置契约

两个 ComfyUI 工具都宣传 Layer 3 的 `comfyui` 技能。代理在调用任一工具前必须阅读 `.agents/skills/comfyui/SKILL.md`，以便了解如何加载社区工作流、识别输出节点、处理 LoRA 加载器链以及记录自定义工作流来源。

不可用的 ComfyUI 工具在 `get_info()`、`provider_menu()` 和 `provider_menu_summary().setup_offers[]` 中暴露结构化的 `setup_offer`：

```yaml
kind: local_server
env_var: COMFYUI_SERVER_URL
default_url: http://localhost:8188
health_check: GET /system_stats
```

当捆绑模型缺失时，工具返回机器可读的 `data.missing_models[]` 列表，包含文件名、角色、目标路径提示和下载 URL（当 OpenMontage 知道规范来源时）。代理应展示该信息，而不是解析文本错误信息。

---

## 配置

**环境变量：**

```bash
# .env
COMFYUI_SERVER_URL=http://localhost:8188    # ComfyUI API 端点
COMFYUI_POLL_INTERVAL=5                     # 状态检查之间的秒数
COMFYUI_POLL_TIMEOUT=600                    # 图像生成的最大等待时间
COMFYUI_VIDEO_TIMEOUT=900                   # 视频生成的最大等待时间
```

**对于 Docker Compose 设置**（容器中的 ComfyUI）：

```bash
COMFYUI_SERVER_URL=http://host.docker.internal:8188
# 或
COMFYUI_SERVER_URL=http://comfyui:8188      # 如果在同一个 docker 网络下
```

---

## 提供商选择行为

当适配器可用时，选择器将使用 OpenMontage 的 7 维评分将其与其他提供商一起排名：

| 维度 | ComfyUI 评分 | 理由 |
|-------|-------------|------|
| 任务匹配度 | 高 | 支持 t2i、i2v、t2v |
| 质量 | 高 | 最新模型（FLUX 2, WAN 2.2 14B） |
| 控制力 | 最高 | 完整的工作流自定义 |
| 可靠性 | 高 | 经生产验证 |
| 成本 | ¥0 | 本地计算 |
| 延迟 | 中等 | GPU 受限，无网络往返 |
| 连续性 | 高 | 使用种子可确定性生成 |

当 ComfyUI 不可用（服务器宕机）时，选择器会回退到其他可用提供商。当仅配置了一种视频操作时，`video_selector` 使用工具的操作特定就绪状态来避免为缺失的模式选择 ComfyUI。

---

## 这将解锁的能力

### 立即获得（使用现有模型）

- **FLUX 2 Dev NVFP4** 图像生成——Blackwell 优化，每张约 60 秒
- **WAN 2.2 14B FP8 高质量配置档案** i2v，4 步加速——每个 5 秒片段约 3.5 分钟，建议约 16GB VRAM
- **WAN 2.2 14B FP8 高质量配置档案** t2v（模型已下载，工作流已包含），建议约 16GB VRAM

### 低 VRAM 配置

当用户提供合适的 `workflow_json` 或 `workflow_path` 时，ComfyUI 在 8GB-12GB GPU 上仍然有用。好的候选包括：

- Wan 2.1 1.3B 工作流，用于较低内存的文生视频。
- LTX-Video/LTXV FP8 或量化工作流，用于快速短片段。
- Wan 2.2 GGUF/量化社区工作流，较低分辨率和帧数。

OpenMontage 应将这些视为自定义工作流配置档案，直到捆绑了官方支持的低 VRAM 工作流。对于自定义工作流，资源需求由工作流提供，而非从捆绑的 WAN 2.2 14B 配置档案推断。

### 未来（添加模型到 ComfyUI，无需修改 OpenMontage 代码）

- 更新的检查点（WAN 3.x、FLUX 3 等）——只需更新工作流 JSON
- ControlNet、IP-Adapter、AnimateDiff——通过 ComfyUI 自定义节点支持
- 放大、内补绘制、外补绘制——ComfyUI 节点已存在
- ComfyUI 生态系统支持的任何模型

### 硬件可移植性

同一适配器可在以下设备上工作：
- NVIDIA DGX Spark（GB10，aarch64，CUDA 13.0）
- 消费级 GPU（RTX 3090/4090，x86）
- 云实例（A100，H100）
- 多 GPU 设置（ComfyUI 处理设备放置）

无 PyTorch 版本锁定、无特定架构的 wheel、无 CUDA 兼容性矩阵。ComfyUI 就是抽象层。

---

## 实现范围

| 组件 | 文件 | 预估大小 |
|------|------|---------|
| 共享客户端 | `tools/_comfyui/client.py` | ~180 行 |
| 共享元数据 | `tools/_comfyui/metadata.py` | 设置、模型栈、来源辅助函数 |
| 图像工具 | `tools/graphics/comfyui_image.py` | ~140 行 |
| 视频工具 | `tools/video/comfyui_video.py` | ~190 行 |
| Layer 3 技能 | `.agents/skills/comfyui/SKILL.md` | 使用契约 |
| 注册表摘要 | `tools/tool_registry.py` | 设置提供展示 |
| 选择器就绪过滤器 | `tools/video/video_selector.py` | 小型操作就绪检查 |
| 工作流模板 | `tools/_comfyui/workflows/*.json` | 3 个文件 |
| 测试 | `tests/contracts/test_comfyui_tools.py` | ~200 行 |
| 文档 | `docs/comfyui-adapter-plan.md` | 本文件 |

**总计：** ~500 行 Python + 3 个工作流 JSON。

无需更改：`base_tool.py`、现有非 ComfyUI 生成提供商、任何流水线定义或任何模式。

---

## 开放问题

1. **工作流版本管理：** 工作流 JSON 应存放在仓库中，还是由用户通过配置目录提供？捆绑提供可重现性，外部提供灵活性。

2. **异步生成：** ComfyUI 支持 WebSocket 连接以提供实时进度。对于长时间的视频生成，是值得实现还是轮询就足够了？

3. **多服务器：** 适配器是否应支持多个 ComfyUI 实例（例如一个用于图像，一个用于视频）通过按能力划分的 URL？

4. **音乐生成：** ACE-Step 在 ComfyUI 中可以工作，但 OpenMontage 需要一个专用的音乐生成路由契约，然后才能添加 `comfyui_music`。后续工作应决定选择器集成、音频工件模式以及可移植的工作流/输出节点契约，而不是将音乐视为隐藏的图像/视频工作流覆盖。
