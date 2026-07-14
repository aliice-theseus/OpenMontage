# Playwright 录制参考

## API 参考

### 浏览器上下文视频选项

```typescript
interface RecordVideoOptions {
  dir: string;                    // 输出目录（必填）
  size?: { width: number; height: number }; // 视频尺寸
}

const context = await browser.newContext({
  viewport: { width: number; height: number };
  recordVideo: RecordVideoOptions;
  // 其他有用选项：
  colorScheme?: 'light' | 'dark' | 'no-preference';
  locale?: string;  // 例如 'en-US'
  timezoneId?: string;  // 例如 'America/New_York'
  geolocation?: { latitude: number; longitude: number };
  permissions?: string[];  // 例如 ['geolocation']
  userAgent?: string;
});
```

### 浏览器启动选项

```typescript
const browser = await chromium.launch({
  slowMo?: number;           // 操作减慢毫秒数
  headless?: boolean;        // 默认 true，设为 false 可查看浏览器
  devtools?: boolean;        // 打开开发者工具
  args?: string[];           // Chromium 标志
});

// 有用的参数：
args: [
  '--start-maximized',
  '--disable-infobars',
  '--hide-scrollbars',
]
```

### 录制相关页面方法

```typescript
// 导航
await page.goto(url, { waitUntil?: 'load' | 'domcontentloaded' | 'networkidle' });
await page.goBack();
await page.goForward();
await page.reload();

// 等待
await page.waitForTimeout(ms);
await page.waitForLoadState('networkidle');
await page.waitForSelector(selector);
await page.waitForURL(urlPattern);

// 交互
await page.click(selector);
await page.dblclick(selector);
await page.fill(selector, value);
await page.type(selector, text);  // 逐个字符输入
await page.press(selector, key);  // 例如 'Enter'、'Tab'
await page.hover(selector);
await page.selectOption(selector, value);
await page.check(selector);       // 复选框
await page.uncheck(selector);

// 滚动
await page.evaluate(() => window.scrollTo(0, 500));
await page.evaluate(() => window.scrollBy(0, 200));
await page.locator(selector).scrollIntoViewIfNeeded();

// 截图（用于缩略图）
await page.screenshot({ path: 'screenshot.png' });
await page.screenshot({ path: 'full.png', fullPage: true });
```

### 录制后获取视频

```typescript
const page = await context.newPage();
// ... 执行操作 ...
await context.close();

// 获取视频路径
const video = page.video();
const path = await video?.path();

// 或保存到特定位置
await video?.saveAs('output.webm');

// 删除视频
await video?.delete();
```

## 常用选择器

```typescript
// CSS 选择器
await page.click('button');
await page.click('#submit-btn');
await page.click('.primary-button');
await page.click('[data-testid="login"]');
await page.click('button:has-text("Submit")');

// 文本选择器
await page.click('text=Click me');
await page.click('text="Exact match"');

// XPath
await page.click('xpath=//button[@type="submit"]');

// 组合
await page.click('form >> button.submit');
await page.click('div.modal >> text=Confirm');
```

## 计时工具

```typescript
// 可重用的延迟函数
const delay = (ms: number) => new Promise(r => setTimeout(r, ms));

// 带延迟的慢速输入
async function typeSlowly(page, selector, text, delayMs = 100) {
  await page.click(selector);
  for (const char of text) {
    await page.keyboard.type(char);
    await delay(delayMs);
  }
}

// 等待动画完成
async function waitForAnimation(page, selector) {
  await page.waitForFunction(
    (sel) => {
      const el = document.querySelector(sel);
      if (!el) return false;
      const style = getComputedStyle(el);
      return style.animationName === 'none' || style.animationPlayState === 'paused';
    },
    selector
  );
}
```

## 设备模拟

```typescript
import { devices } from 'playwright';

// iPhone
const context = await browser.newContext({
  ...devices['iPhone 14'],
  recordVideo: { dir: './recordings' }
});

// iPad
const context = await browser.newContext({
  ...devices['iPad Pro 11'],
  recordVideo: { dir: './recordings' }
});

// 可用设备（部分列表）：
// 'Desktop Chrome', 'Desktop Firefox', 'Desktop Safari'
// 'iPhone 14', 'iPhone 14 Pro Max', 'iPhone SE'
// 'iPad Pro 11', 'iPad Mini'
// 'Pixel 7', 'Galaxy S23'
```

## 处理常见场景

### Cookie 同意横幅

```typescript
// 选项 1：点击接受
try {
  await page.click('button:has-text("Accept")', { timeout: 3000 });
} catch {
  // 横幅不存在
}

// 选项 2：用 CSS 隐藏
await page.addStyleTag({
  content: `
    [class*="cookie"], [id*="cookie"],
    [class*="consent"], [id*="consent"],
    [class*="gdpr"], [id*="gdpr"] {
      display: none !important;
    }
  `
});
```

### 录制前登录

```typescript
// 保存认证状态
const context = await browser.newContext();
const page = await context.newPage();
await page.goto('https://app.com/login');
await page.fill('#email', 'user@example.com');
await page.fill('#password', 'password');
await page.click('button[type="submit"]');
await page.waitForURL('**/dashboard');

// 保存存储状态
await context.storageState({ path: 'auth.json' });
await context.close();

// 使用保存的认证进行录制
const recordingContext = await browser.newContext({
  storageState: 'auth.json',
  recordVideo: { dir: './recordings', size: { width: 1920, height: 1080 } }
});
```

### 处理弹窗/模态框

```typescript
// 等待模态框并交互
await page.click('button.open-modal');
await page.waitForSelector('.modal.visible');
await page.fill('.modal input', 'value');
await page.click('.modal button.submit');
await page.waitForSelector('.modal', { state: 'hidden' });
```

### 文件上传

```typescript
// 单个文件
await page.setInputFiles('input[type="file"]', 'path/to/file.pdf');

// 多个文件
await page.setInputFiles('input[type="file"]', ['file1.pdf', 'file2.pdf']);
```

## 录制脚本模板

```typescript
// scripts/record-[name].ts
import { chromium } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

const CONFIG = {
  url: 'https://example.com',
  outputName: 'demo-name',
  viewport: { width: 1920, height: 1080 },
  slowMo: 50,
};

async function record() {
  console.log(`Starting recording: ${CONFIG.outputName}`);

  const browser = await chromium.launch({
    slowMo: CONFIG.slowMo,
    headless: true,
  });

  const context = await browser.newContext({
    viewport: CONFIG.viewport,
    recordVideo: {
      dir: './temp-recordings',
      size: CONFIG.viewport,
    },
  });

  const page = await context.newPage();

  try {
    // === 录制操作开始 ===

    await page.goto(CONFIG.url);
    await page.waitForTimeout(2000);

    // 在此添加您的操作...

    await page.waitForTimeout(2000);

    // === 录制操作结束 ===

  } catch (error) {
    console.error('Recording failed:', error);
  } finally {
    await context.close();

    // 将视频移动到 public/demos
    const video = page.video();
    const videoPath = await video?.path();

    if (videoPath) {
      const destDir = './public/demos';
      fs.mkdirSync(destDir, { recursive: true });

      const destPath = path.join(destDir, `${CONFIG.outputName}.webm`);
      fs.renameSync(videoPath, destPath);
      console.log(`✓ Saved: ${destPath}`);

      // 提醒转换
      console.log(`\nConvert to MP4 for Remotion:`);
      console.log(`ffmpeg -i ${destPath} -c:v libx264 -crf 20 -movflags faststart ${destPath.replace('.webm', '.mp4')}`);
    }

    await browser.close();
  }
}

record();
```

## 时长计算

录制后，获取时长用于 Remotion 配置：

```bash
# 获取时长（秒）
ffprobe -v error -show_entries format=duration -of csv=p=0 recording.webm

# 计算帧数（30fps）
# duration_seconds * 30 = frames
```

```typescript
// 在 Node.js 中
import { execSync } from 'child_process';

function getVideoDuration(filePath: string): number {
  const output = execSync(
    `ffprobe -v error -show_entries format=duration -of csv=p=0 "${filePath}"`
  ).toString().trim();
  return parseFloat(output);
}

function getFrameCount(filePath: string, fps = 30): number {
  const duration = getVideoDuration(filePath);
  return Math.ceil(duration * fps);
}
```
