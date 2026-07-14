---
name: parameters
description: 通过添加 Zod schema 使视频参数化
metadata:
  tags: parameters, zod, schema
---

要使视频参数化，可以为合成添加一个 Zod schema。

首先，必须安装 `zod`。

搜索项目中的锁定文件，根据包管理器运行相应命令：

如果找到 `package-lock.json`，请使用以下命令：

```bash
npm i zod
```

如果找到 `bun.lockb`，请使用以下命令：

```bash
bun i zod
```

如果找到 `yarn.lock`，请使用以下命令：

```bash
yarn add zod
```

如果找到 `pnpm-lock.yaml`，请使用以下命令：

```bash
pnpm i zod
```

然后，可以在组件旁边定义一个 Zod schema：

```tsx title="src/MyComposition.tsx"
import { z } from "zod";

export const MyCompositionSchema = z.object({
  title: z.string(),
});

const MyComponent: React.FC<z.infer<typeof MyCompositionSchema>> = () => {
  return (
    <div>
      <h1>{props.title}</h1>
    </div>
  );
};
```

在根文件中，可以将 schema 传递给合成：

```tsx title="src/Root.tsx"
import { Composition } from "remotion";
import { MycComponent, MyCompositionSchema } from "./MyComposition";

export const RemotionRoot = () => {
  return (
    <Composition
      id="MyComposition"
      component={MyComponent}
      durationInFrames={100}
      fps={30}
      width={1080}
      height={1080}
      defaultProps={{ title: "Hello World" }}
      schema={MyCompositionSchema}
    />
  );
};
```

现在，用户可以在侧边栏中直观地编辑参数。

Zod 支持的所有 schema 都被 Remotion 支持。

Remotion 要求顶层类型必须是 `z.object()`，因为 React 组件的属性集合始终是一个对象。

## 颜色选择器

要添加颜色选择器，请使用 `@remotion/zod-types` 中的 `zColor()`。

如果尚未安装，请使用以下命令：

```bash
npx remotion add @remotion/zod-types # 如果项目使用 npm
bunx remotion add @remotion/zod-types # 如果项目使用 bun
yarn remotion add @remotion/zod-types # 如果项目使用 yarn
pnpm exec remotion add @remotion/zod-types # 如果项目使用 pnpm
```

然后从 `@remotion/zod-types` 导入 `zColor`：

```tsx
import { zColor } from "@remotion/zod-types";
```

然后在 schema 中使用它：

```tsx
export const MyCompositionSchema = z.object({
  color: zColor(),
});
```
