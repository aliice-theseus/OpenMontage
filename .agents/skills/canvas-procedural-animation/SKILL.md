---
name: canvas-procedural-animation
description: 使用 p5.js/canvas 进行本地程序化角色效果：粒子、天气、挤压/拉伸、行走循环和环境运动。
license: MIT
---

# Canvas 程序化动画

当使用 p5.js 或 Canvas 进行角色辅助运动时使用此技能：
雨、雪、树叶、羽毛、环境粒子、挤压/拉伸或程序化行走循环。

## 成熟模式

p5.js 运行一次 setup 并通过 `draw()` 持续重绘。在渲染预览时，保持动画状态从时间/帧值确定。

```js
function setup() {
  createCanvas(1920, 1080);
}

function draw() {
  const t = millis() / 1000;
  clear();
  drawCharacter(width / 2, height / 2 + sin(t * 8) * 8);
}
```

## 适用范围

- 粒子/天气叠加效果。
- 环境运动。
- 简单的程序化身体。
- 不需要单独创作 SVG 部件的效果。

## 避免用于

- 复杂的面部表演，其中 SVG/分层绑定部件更易于检查。
- 需要精确帧确定性的最终渲染，除非运行时暴露了帧索引控制。

## 参考资料

- p5.js `setup()` 参考：https://p5js.org/reference/p5/setup/
- p5.js `draw()` 参考：https://p5js.org/reference/p5/draw/
- p5.js 动画示例：https://p5js.org/examples/
