# BiliVagent-tool

中文 | [English](README_EN.md)

基于 Python 和 LangChain 的 Bilibili 视频智能分析工具

## 简介

BiliVagent 是一个智能分析 Bilibili 视频的工具，使用 SiliconFlow API 提供的大语言模型支持，能够自动完成视频下载、内容分析、评论分析等多项任务，最终生成详细的视频分析报告。

## 功能特性

### 完整的分析流程

1. **视频解析与下载**
   - 支持 BV 号和视频链接解析
   - 自动下载视频文件
   - 获取视频元数据（标题、分区、标签等）

2. **评论区与弹幕爬取**
   - 爬取视频评论
   - 爬取弹幕内容
   - 文本脱敏处理

3. **视频内容分析**
   - 音频提取
   - 语音识别（使用 Vosk 库）
   - 生成内容概述
   - 提取关键词

4. **视觉分析**
   - 随机抽取 3 帧画面
   - 使用 Qwen3-VL 多模态模型分析视频风格

5. **文本分析**
   - 关键词提取
   - 群体情感识别
   - 生成讨论总结

### 生成的分析报告包含

- BV号
- 视频标题
- 概述
- 关键词（前十）
- 视频风格
- 讨论情感
- 讨论关键词
- 相关讨论

## 图形界面

项目现已包含基于 Tkinter 的用户友好型图形界面，提供：

- **可视化输入**：轻松输入视频链接或 BV 号
- **实时进度**：实时查看分析进度
- **多标签显示**：日志和报告分标签显示
- **报告导出**：将分析报告保存为 JSON 或文本文件
- **状态指示**：清晰的分析状态视觉反馈

### 使用图形界面

```bash
python gui.py
```

图形界面提供：
- 📋 **运行日志标签**：实时分析过程日志
- 📊 **分析报告标签**：格式化的分析结果
- 💾 **保存功能**：导出报告到文件
- 🗑 **清空功能**：清空日志以进行新的分析

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/HeDaas-Code/BiliVagent-tool.git
cd BiliVagent-tool
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 安装 yt-dlp（用于视频下载）

```bash
pip install yt-dlp
```

或者使用系统包管理器安装：

```bash
# Ubuntu/Debian
sudo apt install yt-dlp

# macOS
brew install yt-dlp
```

### 4. 下载 Vosk 语音识别模型（可选）

如果需要语音识别功能，请下载中文模型：

```bash
# 创建模型目录
mkdir -p models

# 下载并解压模型
wget https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip
unzip vosk-model-cn-0.22.zip -d models/
```

更多模型可在 [Vosk Models](https://alphacephei.com/vosk/models) 下载。

## 配置

### 1. 创建配置文件

```bash
cp .env.example .env
```

### 2. 编辑 .env 文件

```bash
# SiliconFlow API 配置
SILICONFLOW_API_KEY=your_api_key_here
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1

# 模型配置
LLM_MODEL=Qwen/Qwen2.5-32B-Instruct
VLM_MODEL=Qwen/Qwen2-VL-7B-Instruct

# Vosk 模型路径
VOSK_MODEL_PATH=./models/vosk-model-cn-0.22

# 输出目录
OUTPUT_DIR=./output
TEMP_DIR=./temp
```

**重要：** 请在 [SiliconFlow](https://siliconflow.cn) 注册并获取 API Key。

## 使用方法

### 命令行界面

#### 基本用法

```bash
# 使用 BV 号
python main.py BV1xx411c7mD

# 使用完整链接
python main.py https://www.bilibili.com/video/BV1xx411c7mD
```

#### 命令行参数

```bash
python main.py [-h] [-o OUTPUT] [--no-download] video

位置参数:
  video                 Bilibili视频链接或BV号

可选参数:
  -h, --help            显示帮助信息
  -o OUTPUT, --output OUTPUT
                        输出目录（默认: ./output）
  --no-download         跳过视频下载（仅分析评论和弹幕）
```

### 图形界面

启动图形界面：

```bash
python gui.py
```

功能特性：
1. 在输入框中输入视频 URL 或 BV 号
2. 点击"🔍 开始分析"按钮
3. 在日志标签中查看实时进度
4. 在报告标签中查看格式化报告
5. 使用"💾 保存报告"按钮保存报告

### 示例输出

```
============================================================
BiliVagent - Bilibili Video Analysis
============================================================

[1/8] Parsing BV number...
BV号: BV1xx411c7mD

[2/8] Fetching video information...
标题: 示例视频标题
分区: 科技

[3/8] Downloading video...
Video saved to: ./temp/BV1xx411c7mD.mp4

[4/8] Processing video content...
Extracting audio from video...
Transcribing audio to text...
Generating summary from transcription...
Extracting video frames...
Analyzing video style...

[5/8] Fetching comments...
Fetched 100 comments

[6/8] Fetching danmaku...
Fetched 523 danmaku

[7/8] Processing text content (comments and danmaku)...
Desensitizing text content...
Extracting keywords from comments and danmaku...
Analyzing sentiment...
Generating discussion summary...

[8/8] Generating final report...

✓ Report saved to: ./output/BV1xx411c7mD_report.json

============================================================
分析报告
============================================================

BV号: BV1xx411c7mD
视频标题: 示例视频标题

概述:
这是一个关于...的视频

关键词（前十）:
  1. 关键词1
  2. 关键词2
  ...

视频风格: 高清画质，色彩鲜艳，构图专业

讨论情感: 正面

讨论关键词:
  1. 讨论词1
  2. 讨论词2
  ...

相关讨论:
观众主要讨论...

元数据:
  分区: 科技
  UP主: UP主名称
  评论数: 100
  弹幕数: 523
============================================================

✓ 分析完成!
```

## 技术架构

### 核心技术栈

- **Python 3.8+**: 主要编程语言
- **LangChain**: Agent 框架
- **SiliconFlow API**: 大语言模型服务
  - Qwen3-32B: 文本分析模型
  - Qwen3-VL: 视觉多模态模型
- **Vosk**: 语音识别库
- **MoviePy**: 视频音频处理
- **OpenCV**: 视频帧提取
- **jieba**: 中文分词与关键词提取
- **bilibili-api-python**: Bilibili API 接口
- **yt-dlp**: 视频下载工具
- **Tkinter**: GUI 框架

### 项目结构

```
BiliVagent-tool/
├── bilivagent/              # 主包
│   ├── __init__.py
│   ├── config.py            # 配置管理
│   ├── agents/              # Agent 实现
│   │   ├── __init__.py
│   │   └── bilivagent.py    # 主 Agent
│   ├── processors/          # 内容处理器
│   │   ├── __init__.py
│   │   ├── video_content.py # 视频内容处理
│   │   └── text_content.py  # 文本内容处理
│   └── utils/               # 工具模块
│       ├── __init__.py
│       ├── bilibili.py      # Bilibili API 封装
│       ├── video.py         # 视频处理
│       ├── audio.py         # 音频处理
│       ├── text.py          # 文本处理
│       └── siliconflow.py   # SiliconFlow API 客户端
├── models/                  # 模型文件目录
├── output/                  # 输出目录
├── temp/                    # 临时文件目录
├── main.py                  # CLI 主入口
├── gui.py                   # GUI 主入口
├── requirements.txt         # Python 依赖
├── .env.example            # 配置文件示例
├── README.md               # 中文文档
└── README_EN.md            # 英文文档
```

## 工作流程

```
Bilibili视频链接
    ↓
解析BV号
    ↓
获取视频信息（标题、分区、标签）
    ↓
视频下载 ──→ 评论区爬取 ──→ 弹幕爬取
    ↓            ↓              ↓
音频提取      脱敏处理       脱敏处理
    ↓            ↓              ↓
语音识别      文本库合并 ←────┘
    ↓            ↓
概述生成      关键词提取
    ↓            ↓
关键词云      情感分析
    ↓            ↓
视频抽帧      讨论分析
    ↓            ↓
风格分析 ←────┴────┘
    ↓
生成最终报告
```

## API 参考

### SiliconFlow API

本项目使用 SiliconFlow 提供的 API 服务：

- **API 文档**: https://docs.siliconflow.cn/
- **模型列表**: https://docs.siliconflow.cn/llms-full.txt
- **注册地址**: https://siliconflow.cn

### 使用的模型

1. **Qwen/Qwen2.5-32B-Instruct**: 用于文本分析、概述生成、关键词提取等
2. **Qwen/Qwen2-VL-7B-Instruct**: 用于视频画面分析、风格识别

## 注意事项

1. **API Key**: 使用前必须配置有效的 SiliconFlow API Key
2. **网络环境**: 需要能够访问 Bilibili 和 SiliconFlow API
3. **Vosk 模型**: 语音识别功能需要下载 Vosk 模型
4. **视频下载**: 需要安装 yt-dlp 工具
5. **存储空间**: 视频下载和处理需要足够的磁盘空间
6. **处理时间**: 完整分析一个视频可能需要几分钟时间

## 常见问题

### Q: 如何获取 SiliconFlow API Key？

A: 访问 https://siliconflow.cn 注册账号，在控制台创建 API Key。

### Q: 视频下载失败怎么办？

A: 确保已安装 yt-dlp，并检查网络连接。某些视频可能有地区限制。

### Q: 语音识别不工作？

A: 请确认已下载 Vosk 模型并正确配置 VOSK_MODEL_PATH。

### Q: 可以批量处理多个视频吗？

A: 当前版本暂不支持批量处理，建议使用脚本循环调用。

### Q: 图形界面无法启动？

A: 请确保已安装 Tkinter。在 Linux 上可能需要安装：`sudo apt-get install python3-tk`

### Q: 如何更改分析语言？

A: 分析结果的语言由 LLM 模型决定。您可以在代码中修改提示词来调整输出语言。

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

## 致谢

- [SiliconFlow](https://siliconflow.cn) 提供的 API 服务
- [Vosk](https://alphacephei.com/vosk/) 语音识别引擎
- [bilibili-api-python](https://github.com/Nemo2011/bilibili-api) Bilibili API 库
- [LangChain](https://github.com/langchain-ai/langchain) Agent 框架

## 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本历史和更新内容。
