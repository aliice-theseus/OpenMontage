# OpenMontage 测试规范

> 基于项目现有测试实践总结的开发测试规范。

---

## 一、测试目录结构

```
tests/
├── contracts/       # 契约测试 — 基础设施、工具注册表、管道模式、阶段推进
├── tools/           # 工具单元测试 — 单个工具的隔离测试，不联网
├── qa/              # 质量验证测试 — 真实 API 调用、二进制输出验证
├── eval/            # 回归评估框架 — GoldenScenario + 基准运行器
├── pipelines/       # 管道级别集成测试（预留）
├── styles/          # 剧本风格测试（预留）
└── TEST_SPEC.md     # 本规范
```

### 各层级测试定位

| 层级 | 目录 | 网络依赖 | 外部服务 | 运行频率 | 典型耗时 |
|------|------|---------|---------|---------|---------|
| **单元测试** | `tests/tools/` | 否 | 无 | 每次提交 | 秒级 |
| **契约测试** | `tests/contracts/` | 否 | 无 | 每次提交 | 秒级 |
| **质量验证** | `tests/qa/` | 可能 | API/GPU | CI 每日/手动 | 分钟级 |
| **回归评估** | `tests/eval/` | 否 | 无 | PR 合并前 | 分钟级 |

---

## 二、命名规范

### 2.1 文件命名

```
tests/<category>/test_<module_name>.py
```

| 类别 | 模式 | 示例 |
|------|------|------|
| 工具测试 | `tests/tools/test_<tool_name>.py` | `test_seedance_video.py`、`test_clip_cache.py` |
| 契约测试 | `tests/contracts/test_phase<N>_*.py` | `test_phase0_contracts.py` |
| QA 测试 | `tests/qa/test_<NN>_<feature>.py` | `test_05_video_compose.py`、`test_08_end_to_end.py` |

### 2.2 测试类命名

按功能域分组，使用 `Test` 前缀：

```python
class TestConfig:          # 配置解析测试
class TestMetadata:        # 工具元数据测试
class TestEstimation:      # 成本/耗时估算测试
class TestBuildContent:    # 输入构建测试
class TestExecute:         # 执行路径测试
class TestEdgeCases:       # 边界/异常测试
```

### 2.3 测试函数命名

蛇形命名，清晰表达被测行为：

```python
def test_api_key_from_env(self):              # 环境变量读取
def test_endpoint_id_default(self):            # 默认值回退
def test_status_unavailable_when_key_missing(self):  # 状态与条件
def test_execute_fails_without_api_key(self):  # 错误路径
def test_with_reference_images(self):          # 含参考素材输入
def test_image_count_limit(self):              # 边界限制（异常）
```

---

## 三、夹具（Fixtures）规范

### 3.1 使用 `pytest` 内置夹具

```python
# 临时目录 — 自动清理
def test_with_temp_dir(self, tmp_path):
    p = tmp_path / "test.png"
    
# 环境变量隔离
def test_with_env(self, monkeypatch):
    monkeypatch.setenv("ARK_API_KEY", "test-key")
```

### 3.2 模块级夹具

```python
@pytest.fixture
def tool() -> SeedanceVideo:
    """返回一个干净的工具实例，不含任何环境变量。"""
    return SeedanceVideo()

@pytest.fixture
def tool_with_key(monkeypatch) -> SeedanceVideo:
    """返回一个已配置 API Key 的工具实例。"""
    monkeypatch.setenv("ARK_API_KEY", "ark-test-key")
    monkeypatch.setenv("SEEDANCE_ENDPOINT_ID", "ep-test-001")
    return SeedanceVideo()

@pytest.fixture
def sample_image(tmp_path) -> Path:
    """生成一个测试用 PNG 文件。"""
    p = tmp_path / "test.png"
    p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    return p
```

---

## 四、断言规范

### 4.1 优先使用原生 assert

```python
# ✅ 正确
assert tool.name == "seedance_video"
assert result.success is False
assert "error message" in result.error

# ❌ 避免不必要的 pytest 专用断言
# assert_equal(tool.name, "seedance_video")  
```

### 4.2 异常测试

```python
# 使用 pytest.raises 上下文管理器
def test_image_count_limit(self, tool):
    with pytest.raises(ValueError, match="最多接受 9 张"):
        tool._build_content_array({"prompt": "test", "reference_image_urls": too_many})
```

### 4.3 边界值测试

```python
def test_input_schema_duration_bounds(self, tool):
    props = tool.input_schema["properties"]["duration"]
    assert props["minimum"] == 4
    assert props["maximum"] == 15
    assert props["default"] == 5
```

---

## 五、测试内容覆盖规则

每个工具类至少应覆盖以下 6 类测试：

| 类别 | 覆盖内容 | 示例 |
|------|---------|------|
| **配置解析** | 环境变量读取、默认值回退、无效配置 | API Key 存在/缺失、Endpoint ID 自定义/默认 |
| **元数据** | 名称、版本、能力声明、运行时、质量评分 | `tool.name`、`tool.version`、`tool.supports` |
| **成本估算** | 估算函数返回值、参数对结果的影响 | 时长/分辨率变化时费用递增 |
| **输入构建** | 输入参数到 API payload 的正确转换 | content 数组结构、字段映射 |
| **边界检查** | 输入参数的上下界、枚举值 | 图片数量上限、时长范围 |
| **错误路径** | 缺少配置、无效输入时的错误返回 | API Key 缺失、文件不存在、超限 |

---

## 六、编写样例流程

参照 `_test_seedance.py` → `test_seedance_video.py` 的迁移过程：

```
步骤 1: 分析被测模块的公共 API
        ↓
步骤 2: 确定测试维度（配置/元数据/估算/输入构建/错误路径）
        ↓
步骤 3: 为每个维度创建 TestXxx 类
        ↓
步骤 4: 为每个具体行为创建 test_xxx 方法
        ↓
步骤 5: 抽取公共夹具（fixture）
        ↓
步骤 6: 运行：python -m pytest tests/tools/test_xxx.py -v
        ↓
步骤 7: 全部通过后，删除临时的测试脚本
```

### 快速测试命令

```bash
# 运行单个测试文件
python -m pytest tests/tools/test_seedance_video.py -v

# 运行所有工具单元测试
python -m pytest tests/tools/ -v

# 运行所有测试（不含网络）
python -m pytest tests/ --ignore=tests/qa --ignore=tests/eval -v

# 运行特定测试类
python -m pytest tests/tools/test_seedance_video.py::TestConfig -v
```
