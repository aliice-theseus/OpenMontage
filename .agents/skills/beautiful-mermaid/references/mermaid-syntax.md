# Mermaid 语法参考

生成有效 Mermaid 图表代码的快速参考。

## 流程图

```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

### 方向
- `TD` / `TB` - 从上到下
- `BT` - 从下到上
- `LR` - 从左到右
- `RL` - 从右到左

### 节点形状
- `A[Text]` - 矩形
- `A(Text)` - 圆角矩形
- `A([Text])` - 体育场/药丸形
- `A[[Text]]` - 子程序
- `A[(Text)]` - 圆柱体（数据库）
- `A((Text))` - 圆形
- `A>Text]` - 非对称
- `A{Text}` - 菱形（决策）
- `A{{Text}}` - 六边形
- `A[/Text/]` - 平行四边形
- `A[\Text\]` - 平行四边形替代
- `A[/Text\]` - 梯形
- `A[\Text/]` - 梯形替代

### 边样式
- `A --> B` - 箭头
- `A --- B` - 直线
- `A -.-> B` - 虚线箭头
- `A ==> B` - 粗箭头
- `A -->|text| B` - 带标签的箭头（推荐）
- `A ---|text| B` - 带标签的直线（推荐）

**重要**：始终使用管道语法 `-->|label|` 表示边标签。空格-破折号语法 `-- label -->` 可能导致渲染不完整。

### 子图
```mermaid
graph TD
    subgraph Group1 [Label]
        A --> B
    end
    subgraph Group2
        C --> D
    end
    B --> C
```

## 时序图

```mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello
    B-->>A: Hi there
    A->>+B: Start process
    B-->>-A: Done
```

### 箭头类型
- `->>` - 实线箭头
- `-->>` - 虚线箭头
- `-x` - 实线带叉
- `--x` - 虚线带叉
- `-)` - 实线开口箭头
- `--)` - 虚线开口箭头

### 激活
- `+` 在箭头后激活参与者
- `-` 在箭头后取消激活参与者

### 注释和框
```mermaid
sequenceDiagram
    Note over A,B: Shared note
    Note right of A: Side note
    rect rgb(200, 220, 255)
        A->>B: In a box
    end
```

### 循环和条件
```mermaid
sequenceDiagram
    loop Every minute
        A->>B: Ping
    end
    alt Success
        B-->>A: Pong
    else Failure
        B-->>A: Error
    end
    opt Optional
        A->>B: Extra step
    end
```

## 状态图

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing : start
    Processing --> Done : complete
    Processing --> Error : fail
    Error --> Idle : reset
    Done --> [*]
```

### 复合状态
```mermaid
stateDiagram-v2
    state Active {
        [*] --> Running
        Running --> Paused : pause
        Paused --> Running : resume
    }
    Idle --> Active : activate
    Active --> Idle : deactivate
```

### 注释
```mermaid
stateDiagram-v2
    State1 : Description here
    note right of State1
        Additional info
    end note
```

## 类图

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() void
    }
    class Dog {
        +bark() void
    }
    Animal <|-- Dog : extends
```

### 关系
- `<|--` - 继承
- `*--` - 组合
- `o--` - 聚合
- `-->` - 关联
- `--` - 链接（实线）
- `..>` - 依赖
- `..|>` - 实现
- `..` - 链接（虚线）

### 基数
```mermaid
classDiagram
    Customer "1" --> "*" Order
    Order "1" --> "1..*" LineItem
```

### 可见性
- `+` 公开
- `-` 私有
- `#` 受保护
- `~` 包/内部

## 实体关系图

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    PRODUCT }|..|{ LINE-ITEM : "ordered in"
```

### 关系类型
- `||` - 恰好一个
- `|{` - 一个或多个
- `o{` - 零个或多个
- `o|` - 零个或一个

### 标识与非标识
- `--` - 标识（实线）
- `..` - 非标识（虚线）

### 属性
```mermaid
erDiagram
    CUSTOMER {
        string id PK
        string name
        string email UK
    }
    ORDER {
        int id PK
        string customer_id FK
        date created_at
    }
```

## 样式

### CSS 类
```mermaid
graph TD
    A:::highlight --> B
    classDef highlight fill:#f96,stroke:#333
```

### 内联样式
```mermaid
graph TD
    A --> B
    style A fill:#bbf,stroke:#333
```

## 提示

1. **转义特殊字符**：对包含特殊字符的标签使用引号：`A["Label with (parens)"]`
2. **多行标签**：使用 `<br/>` 换行
3. **注释**：使用 `%%` 表示不会渲染的注释
4. **ID 与标签**：节点 ID 应简单，标签可以复杂：`node1["Complex Label Here"]`
