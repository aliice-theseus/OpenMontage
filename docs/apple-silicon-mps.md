# Apple Silicon（MPS）支持

OpenMontage 通过 PyTorch 的 Metal Performance Shaders（MPS）后端支持 Apple Silicon Mac（M1/M2/M3/M4/M5）。本地 GPU 工具——视频生成、放大和人脸修复——在可用时会自动检测并使用 MPS。

## 要求

- macOS 12.3（Monterey）或更高版本
- Apple Silicon Mac（M 系列芯片）
- Python 3.10+

## 快速设置

```bash
# 启用本地生成
export VIDEO_GEN_LOCAL_ENABLED=true

# 安装依赖——MPS 支持已包含在默认的 torch wheel 中
uv pip install diffusers transformers accelerate torch pillow requests

# 用于放大和人脸修复
uv pip install realesrgan gfpgan
```

无需特殊的 CUDA 构建或单独的 MPS 包——在 macOS 上 `uv pip install torch` 会自动包含 MPS 支持。

## 工作原理

`tools/video/_shared.py` 中的 `get_torch_device()` 辅助函数会自动检测最佳可用设备：

1. **CUDA**（NVIDIA GPU）——可用时使用；对扩散模型性能最快
2. **MPS**（Apple Silicon Metal）——在 M 系列 Mac 上使用；性能良好
3. **CPU**——回退方案，始终可用但速度明显较慢

设备选择是自动的。所有本地 GPU 工具（`upscale`、`face_restore`、`ltx_video_local`、`wan_video_local` 等）都通过此辅助函数进行路由。

## 已知限制

- **VRAM**：Apple Silicon 使用统一内存。需要超过 16 GB VRAM 的模型可能无法在 16GB Mac 上运行。请查看工具的 `resource_profile.vram_mb`。
- **bfloat16**：MPS 不支持。流水线在 MPS 上自动使用 float16，在 CPU 上使用 float32。
- **CPU offloading**：`enable_model_cpu_offload()` 仅支持 CUDA。在 MPS 上，流水线回退到直接设备放置。
- **Real-ESRGAN 半精度**：fp16 在 MPS 上可能产生 NaN 伪影，因此在非 CUDA 设备上放大自动使用 fp32。

## 验证 MPS 是否生效

```python
from tools.video._shared import get_torch_device
print(get_torch_device())  # 在 Apple Silicon 上应输出 "mps"
```

如果它在 Apple Silicon Mac 上输出 `"cpu"`，请验证：
- macOS 版本为 12.3+
- 已安装 PyTorch（`uv pip install torch`）
- 正在运行原生 ARM Python（而不是 Rosetta x86）
