# 能力扩展协议

## 何时使用

当你遇到现有工具都无法满足的制作需求时。agent 可以扩展系统——但需要有防护措施。这取代了笼统的"不要编写临时 Python 脚本"规则，代之以结构化的协议。

## 先评估

在编写任何内容之前，对缺口进行分类：

| 缺口类型 | 示例 | 操作 |
|----------|---------|--------|
| **一次性转换** | 自定义图像裁剪、颜色调整、格式转换 | 编写项目范围内的 Python 脚本 |
| **重复性视觉需求** | 新的插图风格、自定义图表类型 | 生成自定义 playbook 或 Remotion 组件 |
| **缺失的提供商** | 用户想要注册表中没有的特定 API | 创建最小工具包装器 |
| **缺失的知识** | agent 不知道如何为特定模型编写提示 | 使用网络搜索学习，然后作为第 3 层技能记录 |

## 临时脚本规则

脚本仅在以下情况下允许：
1. 没有现有工具覆盖该需求（通过预检查验注册表确认）
2. 脚本是幂等的（重新运行安全）
3. 脚本在项目工作区中生成文件工件
4. 脚本已记录在决策日志中：`category: "capability_extension"`
5. 用户已知情："我写了一个用于 X 的自定义脚本，因为没有现有工具处理 Y"
6. 脚本在没有用户批准的情况下**不**调用外部 API

脚本存放位置：`projects/<project-name>/scripts/`

### 脚本模板

```python
"""<此脚本功能的一行描述>

由能力扩展协议创建，原因：<没有现有工具覆盖此需求的原因>
决策日志条目：<decision_id>
"""
import sys
from pathlib import Path

def main(input_path: str, output_path: str) -> None:
    # 幂等：检查输出是否已存在
    out = Path(output_path)
    if out.exists():
        print(f"输出已存在：{out}")
        return

    # ... 转换逻辑 ...

    print(f"已创建：{out}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

## 自定义 Playbook 规则

当现有 playbook 与需求不匹配时：
1. 使用 `lib/playbook_generator.py` 创建新 playbook
2. 如果可能，基于最接近的现有 playbook
3. 对照 `schemas/styles/playbook.schema.json` 验证
4. 保存到 `styles/custom/<project-name>.yaml`
5. 作为决策记录：`category: "playbook_selection"`，`subject: "custom playbook created"`

## 新技能规则（技术学习）

当 agent 在网络研究期间发现技术知识时：
1. 将其记录为项目范围的技能：`projects/<project-name>/skills/<name>.md`
2. 遵循第 3 层技能格式：
   - 提供商名称和版本
   - 提供商特定的提示模式
   - 此用例的最佳参数
   - 质量提示和已知失败模式
   - 信息的来源 URL
3. 在决策日志中引用它
4. 如果普遍有用，建议推广到 `.agents/skills/`

## 工具包装器规则

当用户需要注册表中没有的特定提供商时：
1. agent 可以创建一个最小化的 `BaseTool` 子类
2. 保存到 `projects/<project-name>/tools/<name>.py`
3. 它**必须**继承自 `BaseTool` 并实现完整合约（input_schema、execute、capabilities 等）
4. 它**必须**在使用前注册
5. 作为决策记录：`category: "capability_extension"`
6. 首次付费 API 调用前需要用户批准

## 仍然禁止的内容

- 绕过流水线（所有制作仍需经过阶段）
- 在用户不知情的情况下调用外部 API
- 修改 `tools/` 中的现有工具（创建包装器，不要修改原始文件）
- 跳过决策日志
- 编写有超出其输出文件范围的副作用的脚本（不发送电子邮件、不推送到远程、不删除项目工作区外的文件）

## 决策日志条目格式

每个扩展必须被记录：

```json
{
  "decision_id": "ext-001",
  "stage": "<current stage>",
  "category": "capability_extension",
  "subject": "为 <purpose> 创建了自定义 <script|playbook|skill|tool>",
  "options_considered": [
    {"option_id": "existing-tool", "label": "<closest existing tool>", "rejected_because": "<why it doesn't work>"},
    {"option_id": "extension", "label": "<what was created>", "reason": "<why this approach>"}
  ],
  "selected": "extension",
  "reason": "<concise justification>",
  "user_visible": true,
  "confidence": 0.8
}
```
