# ManimGL 交互式开发

ManimGL 的杀手级功能是交互式开发模式，让你无需重新渲染整个场景即可快速迭代。

## 启动交互模式

使用 `-se`（跳过并嵌入）标志并指定行号：

```bash
# 在第 20 行进入交互模式
manimgl scene.py MyScene -se 20

# 在开头进入
manimgl scene.py MyScene -se 1
```

场景运行到该行，然后进入 IPython shell。

## checkpoint_paste()

核心工作流函数。将代码复制到剪贴板，然后：

```python
# 从剪贴板运行代码并显示全部动画
checkpoint_paste()

# 立即运行（无动画），用于快速迭代
checkpoint_paste(skip=True)

# 运行时录制动画
checkpoint_paste(record=True)
```

### 典型工作流程

1. 编写场景，包含占位行
2. 使用 `-se` 在该行运行
3. 将动画代码复制到剪贴板
4. 调用 `checkpoint_paste()` 进行测试
5. 迭代直到满意
6. 将代码移到实际文件中

## self.embed()

编程方式进入 IPython shell：

```python
class MyScene(InteractiveScene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))

        self.embed()  # 在此暂停，进入 shell

        # 退出 shell 后运行以下代码
        self.play(FadeOut(circle))
```

在 shell 中，你可以完全访问：
- `self` - 场景
- 作用域内的所有 mobject
- 所有 ManimGL 函数

## 交互式 Shell 命令

进入 shell 后：

```python
# 检查当前 mobject
self.mobjects

# 添加新内容
square = Square()
self.play(ShowCreation(square))

# 清空并重试
self.clear()

# 退出 shell 并继续场景
exit()
# 或 Ctrl+D
```

## 快速迭代模式

```python
class DevelopScene(InteractiveScene):
    def construct(self):
        # 不常更改的设置
        axes = Axes()
        self.add(axes)

        # 开发断点
        self.embed()

        # 正在迭代的代码放在这里
        # （或在 shell 中使用 checkpoint_paste()）
```

## 录制模式

当你想要捕获交互式操作时：

```python
# 开始录制
checkpoint_paste(record=True)

# 所有动画现在都被录制
# 完成后，视频将被保存
```

## 有用的 Shell 变量

```python
# 当前框架（相机）
self.frame

# 所有 mobject
self.mobjects

# 按类型筛选特定 mobject
[m for m in self.mobjects if isinstance(m, Circle)]

# 框架中心
self.frame.get_center()
```

## 调试技巧

```python
# 打印 mobject 信息
print(circle.get_center())
print(circle.get_height())
print(circle.get_color())

# 高亮某个 mobject
circle.set_color(YELLOW)
self.wait(0.1)

# 检查场景中的内容
print(len(self.mobjects))
```

## 退出并继续

```python
# 交互式会话后，继续场景
exit()  # 或 Ctrl+D

# 场景从暂停处继续执行
```

## 最佳实践

1. **开发时使用 `-se`** - 比重新渲染快得多
2. **将设置代码放在 embed 之前** - 复用状态
3. **使用 `checkpoint_paste(skip=True)`** - 用于快速测试
4. **使用 `checkpoint_paste(record=True)`** - 当调试完成时
5. **将代码组织成函数** - 更容易粘贴和测试
