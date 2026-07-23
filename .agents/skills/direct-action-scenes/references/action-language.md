# 动作语言参考

## 目录

- 动作词库
- 流派映射
- 打击感参数
- 提示结构
- 示例模板

## 动作词库

| 类别 | 中文 | 英文表达 |
|---|---|---|
| 拳法 | 直拳、勾拳、上勾拳、肘击 | `straight punch`, `hook`, `uppercut`, `elbow strike` |
| 腿法 | 侧踢、回旋踢、扫堂腿、膝撞 | `side kick`, `spinning kick`, `leg sweep`, `knee strike` |
| 防御 | 格挡、侧闪、下潜、摇避 | `block`, `dodge sideways`, `duck under`, `weave` |
| 摔投 | 过肩摔、抱摔、锁腕 | `shoulder throw`, `takedown`, `wrist lock` |
| 剑类 | 拔剑、劈砍、突刺、招架、收剑 | `drawing the sword`, `slash`, `thrust`, `parry`, `sheathing` |
| 长兵 | 横扫、点刺、舞棍 | `sweeping strike`, `jab`, `spinning the staff` |
| 枪战 | 举枪、换弹、翻滚入掩体、探身射击 | `raising the gun`, `reloading`, `combat roll to cover`, `leaning out to fire` |
| 跑酷 | 翻越、滑铲、蹬墙、跳跃抓沿 | `vaulting over`, `sliding under`, `wall run`, `leaping to grab the ledge` |

## 流派映射

| 流派 | 节奏 | 镜头 | 提示锚点 |
|---|---|---|---|
| 港式武侠 | 快、飘逸、借力 | 跟拍与局部升格 | `wuxia style, flowing elegant movements, wire-fu aesthetic` |
| 写实近战 | 短促、凶狠、明确 | 近身手持与短切 | `gritty realistic close-quarters combat, raw and heavy` |
| 日漫夸张 | 强蓄力、冲击停顿 | 急推与冲击帧 | `anime-style exaggerated action, dynamic impact frames` |
| 黑色电影 | 长对峙、骤然爆发 | 阴影中静止后突发运动 | `noir standoff, slow tension exploding into one strike` |
| 体育竞技 | 规则内攻防循环 | 环绕与裁判视角 | `boxing footwork, jab and weave rhythm` |

## 打击感参数

按以下顺序组合：

1. `anticipation`：蓄力、重心转移、视线锁定。
2. `impact`：接触点、瞬时速度变化、轻微镜震。
3. `follow-through`：对手踉跄、攻击者惯性、衣料和环境反应。

常用表达：

- `shifting her weight into the strike`
- `momentum carrying him forward`
- `the opponent staggering back to the right`
- `slow motion at the moment of impact`
- `speed ramp: fast approach, slow impact, return to real time`
- `camera shake on impact, dust bursting from the floor`

## 提示结构

### 单人

`[人物与流派] + [2–3 个连续动作] + [环境反馈] + [主镜头运动]`

### 双人

`[A 出招] + [B 闪避/格挡] + [B 反击] + [A 受力反应] + [镜头与风格]`

### 群战

`[主角锚定] + [前景一个对手的具体闭环] + [背景群体压力] + [环境反馈]`

## 示例模板

### 雨夜巷战

`Gritty close-quarters fight in a rain-soaked alley. He winds up and throws a hook; she ducks under it and answers with an elbow strike. He staggers right into trash cans as rainwater and debris burst outward. Tight handheld tracking, brief camera shake only on impact, no gore.`

### 武侠对决

`Two swordspeople face off in a misty bamboo grove. He shifts forward and thrusts; she parries, turns with the momentum, and counters with one flowing slash. Leaves spiral at the blade clash. Tracking wide to medium close-up, brief slow motion at contact, elegant wuxia style.`

### 疲惫终局

`Final exchange of a long duel. Both fighters breathe heavily with lowered, uneven guards. One slow feint draws a tired block, followed by a final speed-ramped strike; the loser stumbles back while the winner needs a full beat to regain balance. Dawn light, restrained handheld, stylized action, no gore.`
