---
name: comfyui
description: 在 OpenMontage 中使用 ComfyUI 工作流时使用，包括 comfyui_image/comfyui_video、自定义 workflow_json/workflow_path 输入、输出节点选择、缺失模型设置、LoRA、低显存工作流选择和社区工作流导入。
---

# OpenMontage 中的 ComfyUI 工作流

在调用 `comfyui_image` 或 `comfyui_video` 之前，以及在将社区 ComfyUI 工作流转换为 OpenMontage 工具调用时使用此技能。

## 服务器契约

- ComfyUI 必须在工具生成前正在运行。默认服务器为 `http://localhost:8188`；可通过 `COMFYUI_SERVER_URL` 覆盖。
- 健康状态和硬件信息来自 `GET /system_stats`。
- 任务提交至 `POST /prompt`，完成的输出从 `GET /history/{prompt_id}` 读取，制品字节通过 `GET /view` 下载。
- 使用 ComfyUI 的 API 格式 JSON（而非 UI 布局格式）导出工作流。如果下载的工作流无法提交，请在 ComfyUI 中启用 API 格式后重新导出。

## 选择工作流

- 当请求的操作匹配且本地机器具有所需模型和显存时，使用捆绑的工作流。
- 当用户需要社区配方、较低显存的模型、不同风格系列或自定义节点时，使用自定义 `workflow_json` 或 `workflow_path`。
- 对于 8GB-12GB GPU，优先选择占用较低的工作流，例如 Wan 2.1 1.3B、LTXV FP8 或量化工作流，或 Wan 2.2 GGUF/量化社区工作流。捆绑的 Wan 2.2 14B FP8 视频工作流是 16GB 级别的路径，而非提供商的通用最低配置。
- 不要承诺任意自定义工作流都能适配某台机器。工作流、量化、分辨率、帧数和卸载设置决定了实际的资源开销范围。

## 输出节点约定

- 自定义工作流必须传递 `output_node`。
- 选择写入制品的节点，通常为 `SaveImage`、`SaveVideo`、`VHS_VideoCombine` 或其他终端保存节点。
- 将节点 ID 作为字符串传递，例如 `"108"`。不要传递类名。
- 如果工作流有多个保存器，选择最终的交付节点，而非预览或中间节点。

## 模板化节点与固定节点

- 在执行前识别模板化节点：提示文本、种子、尺寸、帧数、源图像、采样器设置和输出文件名前缀。
- 固定节点是模型加载器、VAE、文本编码器、LoRA 加载器、调度器和图连接。除非工作流作者意图自定义，否则不要修改这些节点。
- 对于社区工作流，检查每个加载器节点，并在运行前记录每个必需的模型或自定义节点。缺失模型应通过工具的 `missing_models` 结构化负载处理（若可用）。

## 模型和 LoRA 设置

- 在可用时使用 ComfyUI Manager 或工作流作者的模型链接，并遵守模型许可。
- 将模型放置在加载器节点期望的文件夹中：扩散模型在 `ComfyUI/models/diffusion_models/` 下，文本编码器在 `ComfyUI/models/text_encoders/` 下，VAE 在 `ComfyUI/models/vae/` 下，LoRA 在 `ComfyUI/models/loras/` 下。
- 对于 LoRA 栈，在工作流中使用 `LoraLoader` 或 `LoraLoaderModelOnly` 链。记录每个 LoRA 名称以及适用的 `strength_model` 和 `strength_clip`。
- 当前的 ComfyUI 工具不会将 LoRA 注入任意图。要使用 LoRA，请提供一个已包含 LoRA 加载器链的工作流，并传递模型栈来源信息。

## 溯源信息

- 对于自定义工作流，在已知时提供 `workflow_name` 和 `workflow_model`。
- 当工作流非捆绑时，提供 `workflow_model_stack` 以确保可重现性。如果工作流暴露，包括基础检查点或扩散模型、量化、文本编码器、VAE、LoRA 及强度、采样器或调度器、步数和引导尺度。
- 工具会记录最终的工作流哈希。将该哈希连同模型栈、种子、尺寸和提示词视为可重现性契约。

## 故障处理

- 如果服务器不可用，展示结构化的设置建议。启动 ComfyUI 或设置 `COMFYUI_SERVER_URL` 是首要修复步骤。
- 如果模型缺失，读取 `data.missing_models[]`；每个条目应包含文件名、角色、目标位置提示和下载 URL（当 OpenMontage 知道时）。
- 如果缺少自定义节点，要求用户通过 ComfyUI Manager 或工作流作者文档中记录的安装路径来安装，然后重新启动 ComfyUI。
- 如果长时间渲染在本地超时，在从头重试前检查 ComfyUI 历史记录；服务器可能已经完成了该提示。
