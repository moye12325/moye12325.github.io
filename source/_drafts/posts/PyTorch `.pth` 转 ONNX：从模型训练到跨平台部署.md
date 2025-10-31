---
date: 2025-02-17T02:20:43.381Z
updated: null
title: PyTorch `.pth` 转 ONNX：从模型训练到跨平台部署
slug: pth2ONNX
oid: 67b29cfb81920129eb65a653
categories: 人工智能
type: post
permalink: /posts/人工智能/pth2ONNX
---


# **PyTorch `.pth` 转 ONNX：从模型训练到跨平台部署**

在深度学习里，**模型的格式决定了它的可用性**。

如果你是 PyTorch 用户，你可能熟悉 `.pth` 文件，它用于存储训练好的模型。

但当你想在**不同的环境**（如 TensorRT、OpenVINO、ONNX Runtime）部署模型时，`.pth` 可能并不适用。这时，ONNX（Open Neural Network Exchange）就必不可少。

本文目录：
- **什么是 `.pth` 文件？**
- **什么是 `.onnx` 文件？**
- **为什么要转换？**
- **如何转换 `.pth` 到 `.onnx`？**
- **转换后的好处和潜在风险**

---

## **1. 什么是 `.pth` 文件？**
`.pth` 是 **PyTorch 专属的模型权重文件**，用于存储：
1. **模型权重（state_dict）**：仅保存参数，不包含模型结构。
2. **完整模型**：包含模型结构和权重，适用于直接 `torch.save(model, "model.pth")` 保存的情况。

在 PyTorch 中，你可以用以下方式加载 `.pth`：

```python
import torch
from NestedUNet import NestedUNet  # 你的模型类

# 仅保存权重的加载方式
model = NestedUNet(num_classes=2, input_channels=3)
model.load_state_dict(torch.load("best_model.pth"))
model.eval()
```

`.pth` 文件只能在 PyTorch 运行的环境中使用，不能直接在 TensorFlow、OpenVINO 或 TensorRT 里运行。

---

## **2. 什么是 ONNX？**
ONNX（Open Neural Network Exchange）是 **一个开放的神经网络标准格式**，它的目标是：
1. **跨框架兼容**：支持 PyTorch、TensorFlow、Keras、MXNet 等。
2. **优化推理**：可以用 ONNX Runtime 或 TensorRT 加速推理。
3. **部署灵活**：支持在 CPU、GPU、FPGA、TPU 等硬件上运行。

ONNX 文件是一个 `.onnx` 文件，它包含：
- **模型的计算图**
- **算子（OPs）定义**
- **模型权重**

ONNX 让你可以在不同平台上运行同一个模型，而不必依赖某个特定的深度学习框架。

---

## **3. 为什么要转换 `.pth` 到 `.onnx`？**
转换为 ONNX 主要有以下好处：

✅ **跨平台兼容**
- `.pth` 只能在 PyTorch 里用，而 `.onnx` 可以在 **TensorRT、ONNX Runtime、OpenVINO、CoreML** 等多种环境中运行。

✅ **推理速度更快**
- **ONNX Runtime** 使用图优化（Graph Optimization），减少计算冗余，提高推理速度。
- **TensorRT** 可以将 ONNX 模型编译为高度优化的 GPU 代码，显著提高吞吐量。

✅ **支持多种硬件**
- `.pth` 主要用于 CPU/GPU，而 `.onnx` 可用于 **FPGA、TPU、ARM 设备**，如 **安卓手机、树莓派、Jetson Nano** 等。

✅ **更轻量级**
- PyTorch 运行时需要完整的 Python 解释器，而 ONNX 可以直接用 C++/C 代码运行，适用于嵌入式设备。

---

## **4. 如何转换 `.pth` 到 `.onnx`？**
### **4.1 安装依赖**
在转换前，确保你已安装 PyTorch 和 ONNX：

```sh
pip install torch torchvision onnx
```

### **4.2 编写转换代码**
假设你有一个 `NestedUNet` 训练好的 `.pth` 文件，转换方式如下：

```python
import torch
import torch.onnx
from NestedUNet import NestedUNet  # 你的模型文件

# 1. 加载 PyTorch 模型
model = NestedUNet(num_classes=2, input_channels=3, deep_supervision=False)
model.load_state_dict(torch.load("best_model.pth"))
model.eval()

# 2. 创建示例输入（确保形状正确）
dummy_input = torch.randn(1, 3, 256, 256)

# 3. 导出为 ONNX
onnx_path = "nested_unet.onnx"
torch.onnx.export(
    model, 
    dummy_input, 
    onnx_path,
    export_params=True,
    opset_version=11,  # 确保兼容性
    do_constant_folding=True,
    input_names=["input"], 
    output_names=["output"], 
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
)

print(f"✅ 模型已成功转换为 {onnx_path}")
```

### **4.3 验证 ONNX**
安装 `onnxruntime` 并测试：


```sh
pip install onnxruntime
```
然后运行：

```python
import onnxruntime as ort
import numpy as np

# 加载 ONNX
ort_session = ort.InferenceSession("nested_unet.onnx")

# 生成随机输入
input_data = np.random.randn(1, 3, 256, 256).astype(np.float32)
outputs = ort_session.run(None, {"input": input_data})

print("ONNX 推理结果：", outputs[0].shape)
```

---

## **5. 转换后的好处和潜在风险**
### **5.1 好处**
✅ **提高推理速度**
- ONNX Runtime 和 TensorRT 可以显著加速推理，尤其是在 GPU 上。

✅ **跨平台部署**
- `.onnx` 可用于 Windows、Linux、安卓、iOS、嵌入式设备。

✅ **减少依赖**
- 直接用 ONNX Runtime 运行，不需要完整的 PyTorch 依赖。

---

### **5.2 可能遇到的问题**
⚠ **ONNX 可能不支持某些 PyTorch 操作**
- PyTorch 的某些自定义操作（如 `grid_sample`）可能在 ONNX 不支持，需要手动修改模型。

⚠ **ONNX 的 `Upsample` 可能需要 `align_corners=False`**
- 如果 `Upsample(scale_factor=2, mode='bilinear', align_corners=True)`，可能会导致 ONNX 兼容性问题，建议改为：
  
  ```python
  self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False)
  ```

⚠ **ONNX 在 CPU 上的推理可能比 PyTorch 慢**
- 如果模型没有经过优化，ONNX 可能不会比 PyTorch 快，尤其是在 CPU 上。

⚠ **TensorRT 需要额外优化**
- 直接用 TensorRT 运行 ONNX 可能会报错，需要 `onnx-simplifier`:
  
  ```sh
  pip install onnx-simplifier
  python -m onnxsim nested_unet.onnx nested_unet_simplified.onnx
  ```

---

## **6. 对比**
| 比较项           | `.pth` (PyTorch) | `.onnx` (ONNX) |
|----------------|----------------|---------------|
| **框架依赖**  | 仅支持 PyTorch  | 兼容多框架 |
| **推理速度**  | 较慢           | 更快（ONNX Runtime / TensorRT） |
| **跨平台性**  | 仅支持 PyTorch  | 可在多种设备上运行 |
| **部署难度**  | 需要完整 Python | 轻量级，适用于嵌入式 |

👉 **建议**
- **如果模型只在 PyTorch 中用，不建议转换**。
- **如果要跨平台部署（如服务器、移动端），转换为 ONNX 是最佳方案**。
- **如果要在 GPU 加速，建议用 TensorRT 进一步优化 ONNX**。