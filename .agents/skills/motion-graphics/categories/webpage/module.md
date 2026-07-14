# webpage — 类别模块（搜索驱动）

**动画化一个网页/链接**（"网站动画"用例）。搜索驱动：用户提供或命名一个 URL → 抓取/捕获它 → 动画化（滚动浏览、UI 揭示、光标演示、区域标注）。区别于对现有_视频文件_加字幕（那是 `/embedded-captions`）和带旁白的网站视频（那是 `/website-to-video`）；这里的源是一个_网页_，输出是简短、无旁白的高亮镜头。

## 素材来源（第2步）

通过 `hyperframes capture`（DOM + 截图）或提供的截图获取页面 → 冻结的项目本地图片/DOM。`asset_needs`：`{ kind: web, source: <url>, treatment: none }`。

## 词汇表 / 依赖

- 规则：`hyperframes-animation/rules/{3d-page-scroll, demo-page-scroll-spotlight, cursor-click-ripple, coordinate-target-zoom, viewport-change}`。
- 原语：滚动平移 · 聚光灯/变暗 · 光标移动 + 点击波纹 · 缩放到区域 · 标注图钉 + 标签。

## 构建（优先复用）

将捕获的页面作为基础层；动画化**滚动浏览**（在页面高度上 `translateY`）、**聚光灯**关键区域（变暗 + 高亮）、移动并点击（波纹）的**光标**、**缩放**到坐标、以及锚定到页面区域的**标注**图钉/标签。遵守 `builder-contract.md`。

**与新闻文章高亮匹配的两条规则（参见 `../news/module.md`）：**

- **高亮是扫入/动画化的，绝不预先应用** — 聚光灯框擦入（`scaleX 0→1`）、标记扫过区域、标注在缩放落地后_弹出_；页面从不是从预先标注的状态开始的。
- **锚定到真实元素位置** — `hyperframes capture` 提供页面 HTML/DOM，因此测量目标元素（`getBoundingClientRect` → 舞台本地坐标）并精确地缩放/高亮它，一步一步（"高亮真实元素"技术）。不要目测坐标。
