---
name: transform-animations
description: Transform（变形）、ReplacementTransform（替换变形）和形变动画
metadata:
  tags: transform, replacementtransform, morph, transformfromcopy
---

# 变形动画

将一个 mobject 形变为另一个 mobject 的动画。

## Transform

将源 mobject 形变为目标的形状。源 mobject 会被修改。

```python
class TransformExample(Scene):
    def construct(self):
        square = Square()
        circle = Circle()

        self.play(Create(square))
        self.play(Transform(square, circle))
        # 注意：'square' 现在看起来像 'circle'，但仍然是 'square'
```

**重要：** Transform 之后，原变量仍然引用该 mobject，尽管它看起来像目标。

## ReplacementTransform

将源形变为目标并替换引用。对大多数用途来说更直观。

```python
class ReplacementTransformExample(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        triangle = Triangle()

        self.play(Create(square))
        self.play(ReplacementTransform(square, circle))
        # 'square' 被移除，'circle' 现在在场景中
        self.play(ReplacementTransform(circle, triangle))
        # 'circle' 被移除，'triangle' 现在在场景中
```

## Transform vs ReplacementTransform

```python
# Transform —— 源变量改变外观
self.play(Transform(A, B))
# A 仍在场景中（但看起来像 B）
# B 不在场景中

# ReplacementTransform —— 源被目标替换
self.play(ReplacementTransform(A, B))
# A 从场景中移除
# B 现在在场景中
```

## TransformFromCopy

创建源的副本并形变为目标。原始对象保持不变。

```python
class TransformFromCopyExample(Scene):
    def construct(self):
        square = Square().shift(LEFT * 2)
        circle = Circle().shift(RIGHT * 2)

        self.add(square)
        self.play(TransformFromCopy(square, circle))
        # square 和 circle 现在都可见
```

## TransformMatchingShapes

智能匹配并变形对应部分。

```python
class MatchingShapesExample(Scene):
    def construct(self):
        source = Text("ABC")
        target = Text("ABCD")

        self.play(Write(source))
        self.play(TransformMatchingShapes(source, target))
```

## TransformMatchingTex

通过 TeX 字符串匹配 LaTeX 部分。

```python
class MatchingTexExample(Scene):
    def construct(self):
        eq1 = MathTex("a", "^2", "+", "b", "^2")
        eq2 = MathTex("a", "^2", "+", "2ab", "+", "b", "^2")

        self.play(Write(eq1))
        self.play(TransformMatchingTex(eq1, eq2))
```

## MoveToTarget

预设目标状态并动画到该状态。

```python
class MoveToTargetExample(Scene):
    def construct(self):
        square = Square()
        self.add(square)

        # 生成并修改目标
        square.generate_target()
        square.target.shift(RIGHT * 2)
        square.target.set_color(RED)
        square.target.scale(2)

        self.play(MoveToTarget(square))
```

## 路径弧线变形

使用 `path_arc` 控制变形路径。

```python
class PathArcExample(Scene):
    def construct(self):
        dot1 = Dot(LEFT * 2)
        dot2 = Dot(RIGHT * 2)

        self.add(dot1)
        # 沿弧线变形
        self.play(Transform(dot1, dot2, path_arc=PI/2))
```

## 链式变形

```python
class ChainedExample(Scene):
    def construct(self):
        shape = Square()
        self.play(Create(shape))

        # 变形链
        for target in [Circle(), Triangle(), Star()]:
            self.play(Transform(shape, target))
            self.wait(0.5)
```

## 最佳实践

1. **使用 ReplacementTransform 保持清晰** —— 变量行为更直观
2. **使用 TransformFromCopy 保留原始对象** —— 当两者都需要可见时
3. **使用 TransformMatchingTex 处理公式** —— 匹配部分的更好对齐
4. **设置 path_arc 增加视觉趣味** —— 曲线路径更动感
