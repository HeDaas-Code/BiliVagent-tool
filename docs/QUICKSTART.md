# 快速开始指南 / Quick Start Guide

[中文](#中文) | [English](#english)

## 中文

### 概述

这份快速开始指南将帮助你在 5 分钟内运行 BiliVagent。

### 前置要求

- Python 3.8 或更高版本
- pip 包管理器
- 网络连接

### 安装步骤

#### 1. 获取代码

```bash
git clone https://github.com/HeDaas-Code/BiliVagent-tool.git
cd BiliVagent-tool
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置 API 密钥

复制配置文件模板:
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 SiliconFlow API Key:
```bash
SILICONFLOW_API_KEY=your_api_key_here
```

**如何获取 API Key:**
1. 访问 https://siliconflow.cn
2. 注册/登录账号
3. 进入控制台创建 API Key
4. 复制 API Key 到 `.env` 文件

### 第一次运行

#### 使用图形界面（推荐）

```bash
python gui.py
```

1. 在输入框中粘贴 Bilibili 视频链接，例如:
   ```
   https://www.bilibili.com/video/BV1xx411c7mD
   ```
   或直接输入 BV 号:
   ```
   BV1xx411c7mD
   ```

2. 点击"🔍 开始分析"按钮

3. 在"运行日志"标签中查看实时进度

4. 分析完成后，切换到"分析报告"标签查看结果

5. 点击"💾 保存报告"导出结果

#### 使用命令行

```bash
python main.py BV1xx411c7mD
```

或使用完整 URL:
```bash
python main.py https://www.bilibili.com/video/BV1xx411c7mD
```

### 查看结果

分析完成后，报告会保存在 `./output/` 目录:
```bash
ls -l output/
# BV1xx411c7mD_report.json
```

### 可选配置

#### 1. 安装语音识别（可选但推荐）

下载 Vosk 中文模型以启用语音识别功能:

```bash
# 创建模型目录
mkdir -p models

# 下载模型（约 1.3GB）
wget https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip

# 解压
unzip vosk-model-cn-0.22.zip -d models/
```

#### 2. 配置视频下载工具

确保 yt-dlp 已安装:

```bash
pip install yt-dlp

# 或使用系统包管理器
# Ubuntu/Debian:
sudo apt install yt-dlp

# macOS:
brew install yt-dlp
```

### 常见问题

#### Q: 安装依赖时出错？

A: 尝试使用虚拟环境:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### Q: 提示 API Key 无效？

A: 检查 `.env` 文件:
- 确保 `SILICONFLOW_API_KEY` 已正确填写
- 不要有多余的空格或引号
- 确认 API Key 在 SiliconFlow 平台上是激活状态

#### Q: 视频下载失败？

A: 可能的原因:
- 检查网络连接
- 确认视频可访问（没有地区限制）
- 更新 yt-dlp: `pip install -U yt-dlp`
- 尝试跳过下载: `python main.py --no-download BV号`

#### Q: GUI 无法启动？

A: Linux 用户可能需要安装 Tkinter:
```bash
sudo apt-get install python3-tk
```

### 下一步

- 阅读完整的 [README.md](../README.md) 了解所有功能
- 查看 [架构文档](ARCHITECTURE.md) 理解系统设计
- 参考 [贡献指南](../CONTRIBUTING.md) 参与开发

### 示例视频

推荐使用以下类型的视频进行测试:
- 科技类教程视频（内容清晰，评论活跃）
- 知识科普视频（适合内容分析）
- 时长 5-15 分钟的视频（处理时间适中）

---

## English

### Overview

This quick start guide will help you run BiliVagent in 5 minutes.

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection

### Installation Steps

#### 1. Get the Code

```bash
git clone https://github.com/HeDaas-Code/BiliVagent-tool.git
cd BiliVagent-tool
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure API Key

Copy the configuration template:
```bash
cp .env.example .env
```

Edit the `.env` file and add your SiliconFlow API Key:
```bash
SILICONFLOW_API_KEY=your_api_key_here
```

**How to get API Key:**
1. Visit https://siliconflow.cn
2. Register/login
3. Go to console and create an API Key
4. Copy the API Key to `.env` file

### First Run

#### Using GUI (Recommended)

```bash
python gui.py
```

1. Paste a Bilibili video link in the input box, for example:
   ```
   https://www.bilibili.com/video/BV1xx411c7mD
   ```
   Or just enter the BV number:
   ```
   BV1xx411c7mD
   ```

2. Click the "🔍 Start Analysis" button

3. View real-time progress in the "Run Log" tab

4. After analysis completes, switch to "Analysis Report" tab to view results

5. Click "💾 Save Report" to export results

#### Using Command Line

```bash
python main.py BV1xx411c7mD
```

Or use the full URL:
```bash
python main.py https://www.bilibili.com/video/BV1xx411c7mD
```

### View Results

After analysis completes, the report is saved in the `./output/` directory:
```bash
ls -l output/
# BV1xx411c7mD_report.json
```

### Optional Configuration

#### 1. Install Speech Recognition (Optional but Recommended)

Download the Vosk Chinese model to enable speech recognition:

```bash
# Create model directory
mkdir -p models

# Download model (~1.3GB)
wget https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip

# Extract
unzip vosk-model-cn-0.22.zip -d models/
```

#### 2. Configure Video Download Tool

Ensure yt-dlp is installed:

```bash
pip install yt-dlp

# Or use system package manager
# Ubuntu/Debian:
sudo apt install yt-dlp

# macOS:
brew install yt-dlp
```

### Common Issues

#### Q: Error installing dependencies?

A: Try using a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### Q: API Key invalid error?

A: Check your `.env` file:
- Ensure `SILICONFLOW_API_KEY` is correctly filled
- No extra spaces or quotes
- Confirm the API Key is active on SiliconFlow platform

#### Q: Video download fails?

A: Possible reasons:
- Check network connection
- Confirm video is accessible (no regional restrictions)
- Update yt-dlp: `pip install -U yt-dlp`
- Try skipping download: `python main.py --no-download BV_number`

#### Q: GUI won't start?

A: Linux users may need to install Tkinter:
```bash
sudo apt-get install python3-tk
```

### Next Steps

- Read the complete [README_EN.md](../README_EN.md) to learn about all features
- Check [Architecture Documentation](ARCHITECTURE.md) to understand system design
- Refer to [Contributing Guide](../CONTRIBUTING_EN.md) to participate in development

### Example Videos

Recommended video types for testing:
- Technology tutorial videos (clear content, active comments)
- Educational videos (good for content analysis)
- 5-15 minute videos (moderate processing time)
