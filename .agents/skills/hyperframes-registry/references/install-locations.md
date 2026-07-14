# 安装位置

## 默认路径

| 项目类型 | 默认安装路径 | 由……配置 |
| --------- | ------------------------------------- | ----------------------------------- |
| 块 | `compositions/<name>.html` | `hyperframes.json#paths.blocks` |
| 组件 | `compositions/components/<name>.html` | `hyperframes.json#paths.components` |

## 路径重映射的工作原理

每个项的 `registry-item.json` 中的 `target` 字段指定了默认安装路径。`add` 命令基于 `hyperframes.json#paths` 重映射前缀：

- 以 `compositions/` 开头的块目标被重映射到 `<paths.blocks>/`
- 以 `compositions/components/` 开头的组件目标被重映射到 `<paths.components>/`

## hyperframes.json

由 `hyperframes init` 自动创建。如果在运行 `add` 时不存在，CLI 会使用默认值创建：

```json
{
  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": {
    "blocks": "compositions",
    "components": "compositions/components",
    "assets": "assets"
  }
}
```

## 自定义布局

要将块安装到 `scenes/` 目录而不是 `compositions/`：

```json
{
  "paths": {
    "blocks": "scenes"
  }
}
```

然后 `hyperframes add data-chart` 写入 `scenes/data-chart.html` 而不是 `compositions/data-chart.html`。片段输出反映重映射后的路径。
