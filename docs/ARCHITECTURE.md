# 架构文档 / Architecture Documentation

[中文](#中文) | [English](#english)

## 中文

### 系统架构概览

BiliVagent 采用模块化设计，基于 LangChain Agent 框架构建，主要包含以下几个层次:

```
┌─────────────────────────────────────────────────────────────┐
│                    用户接口层 / User Interface               │
│  ┌──────────────────┐      ┌──────────────────────────┐    │
│  │  命令行接口 (CLI) │      │  图形界面 (GUI - Tkinter) │    │
│  │    main.py       │      │       gui.py             │    │
│  └──────────────────┘      └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   核心 Agent 层 / Agent Layer                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            BiliVagent (bilivagent.py)                │   │
│  │  - 协调整体分析流程                                    │   │
│  │  - 调用各个处理器                                      │   │
│  │  - 生成最终报告                                        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  处理器层 / Processor Layer                  │
│  ┌─────────────────────┐    ┌──────────────────────────┐   │
│  │  视频内容处理器      │    │   文本内容处理器          │   │
│  │  VideoContentProcessor│   │ TextContentProcessor    │   │
│  │  - 视频下载          │    │ - 评论爬取               │   │
│  │  - 音频提取          │    │ - 弹幕爬取               │   │
│  │  - 语音识别          │    │ - 文本脱敏               │   │
│  │  - 帧提取分析        │    │ - 关键词提取             │   │
│  │                      │    │ - 情感分析               │   │
│  └─────────────────────┘    └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   工具层 / Utility Layer                     │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │
│  │Bilibili│ │ Video  │ │ Audio  │ │  Text  │ │Silicon │   │
│  │  API   │ │Processing│ │Process │ │Process │ │ Flow  │   │
│  │        │ │        │ │        │ │        │ │  API   │   │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  外部服务层 / External Services              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐              │
│  │Bilibili│ │SiliconFlow│ │ Vosk  │ │ yt-dlp │             │
│  │  API   │ │  LLM API  │ │ Model │ │        │             │
│  └────────┘ └────────┘ └────────┘ └────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### 核心模块说明

#### 1. 用户接口层

**CLI (main.py)**
- 命令行参数解析
- 基本的输入输出处理
- 适合脚本化和批量处理

**GUI (gui.py)**
- 基于 Tkinter 的图形界面
- 实时日志显示
- 报告可视化
- 适合交互式使用

#### 2. Agent 层

**BiliVagent (agents/bilivagent.py)**

主要职责:
- 解析视频 BV 号或 URL
- 协调视频内容和文本内容的处理
- 调用 LLM 生成最终分析报告
- 管理整体工作流程

核心方法:
```python
def analyze_video(video_url: str) -> dict:
    """主分析流程"""
    # 1. 解析 BV 号
    # 2. 获取视频信息
    # 3. 处理视频内容（下载、分析）
    # 4. 处理文本内容（评论、弹幕）
    # 5. 生成最终报告
```

#### 3. 处理器层

**VideoContentProcessor (processors/video_content.py)**

功能模块:
- **视频下载**: 使用 yt-dlp 下载视频
- **音频提取**: 使用 MoviePy 提取音频
- **语音识别**: 使用 Vosk 将音频转文字
- **内容分析**: 调用 LLM 生成概述和关键词
- **帧提取**: 随机提取视频帧
- **风格分析**: 使用 VLM 分析视频风格

**TextContentProcessor (processors/text_content.py)**

功能模块:
- **评论爬取**: 使用 bilibili-api-python 获取评论
- **弹幕爬取**: 获取视频弹幕
- **文本脱敏**: 处理敏感信息
- **关键词提取**: 使用 jieba 分词和 TF-IDF
- **情感分析**: 调用 LLM 分析情感倾向
- **讨论总结**: 生成讨论摘要

#### 4. 工具层

**Bilibili API (utils/bilibili.py)**
- 封装 bilibili-api-python
- 提供统一的 API 调用接口
- 处理认证和错误

**Video Processing (utils/video.py)**
- 视频下载
- 帧提取
- 视频信息获取

**Audio Processing (utils/audio.py)**
- 音频提取
- 格式转换
- 语音识别集成

**Text Processing (utils/text.py)**
- 文本清洗
- 脱敏处理
- 分词和关键词提取

**SiliconFlow API (utils/siliconflow.py)**
- LLM API 调用封装
- VLM API 调用封装
- 请求管理和错误处理

### 数据流

```
Video URL
    ↓
[Parse BV]
    ↓
[Fetch Metadata] ──→ metadata.json
    ↓
┌───────────────────────┬──────────────────────┐
│                       │                      │
[Download Video]   [Fetch Comments]    [Fetch Danmaku]
    ↓                   ↓                      ↓
[Extract Audio]    [Desensitize]        [Desensitize]
    ↓                   ↓                      ↓
[Speech to Text]   [Merge Text] ←─────────────┘
    ↓                   ↓
[Generate Summary] [Extract Keywords]
    ↓                   ↓
[Extract Keywords] [Sentiment Analysis]
    ↓                   ↓
[Extract Frames]   [Discussion Summary]
    ↓                   ↓
[Analyze Style]    ───→ text_analysis.json
    ↓
video_analysis.json
    │
    ↓
[Combine Results]
    ↓
final_report.json
```

### 配置管理

**Config (bilivagent/config.py)**

配置加载顺序:
1. 默认配置
2. .env 文件
3. 环境变量

支持的配置项:
- API 密钥和端点
- 模型选择
- 输出路径
- 处理参数

### 依赖关系

```
main.py / gui.py
    ↓
BiliVagent
    ↓
┌─────────────┬──────────────┐
│             │              │
VideoProcessor TextProcessor Config
    ↓              ↓           ↓
┌───┴───┬────┬────┴──┬────┬───┴────┐
│       │    │       │    │        │
Video Audio Text Bilibili SiliconFlow
Utils  Utils Utils  Utils    Utils
```

### 错误处理

系统采用分层错误处理机制:

1. **工具层**: 捕获和记录具体错误
2. **处理器层**: 处理或传播错误，提供降级方案
3. **Agent 层**: 决定是否继续或终止分析
4. **接口层**: 向用户展示友好的错误信息

### 扩展性

系统设计考虑了以下扩展点:

- **新的处理器**: 继承基础处理器类
- **新的 API 客户端**: 实现统一的接口
- **新的分析功能**: 在处理器中添加新方法
- **新的用户界面**: 复用 Agent 层逻辑

---

## English

### System Architecture Overview

BiliVagent uses a modular design based on the LangChain Agent framework, consisting of the following layers:

```
┌─────────────────────────────────────────────────────────────┐
│                         User Interface                       │
│  ┌──────────────────┐      ┌──────────────────────────┐    │
│  │  CLI Interface   │      │    GUI (Tkinter)         │    │
│  │    main.py       │      │       gui.py             │    │
│  └──────────────────┘      └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                        Agent Layer                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            BiliVagent (bilivagent.py)                │   │
│  │  - Coordinate overall analysis flow                  │   │
│  │  - Call various processors                           │   │
│  │  - Generate final report                             │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      Processor Layer                         │
│  ┌─────────────────────┐    ┌──────────────────────────┐   │
│  │  Video Content      │    │   Text Content           │   │
│  │  Processor          │    │   Processor              │   │
│  │  - Video download   │    │ - Comment crawling       │   │
│  │  - Audio extraction │    │ - Danmaku crawling       │   │
│  │  - Speech recognition│   │ - Text desensitization   │   │
│  │  - Frame analysis   │    │ - Keyword extraction     │   │
│  │                      │    │ - Sentiment analysis     │   │
│  └─────────────────────┘    └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                       Utility Layer                          │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │
│  │Bilibili│ │ Video  │ │ Audio  │ │  Text  │ │Silicon │   │
│  │  API   │ │Processing│ │Process │ │Process │ │ Flow  │   │
│  │        │ │        │ │        │ │        │ │  API   │   │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     External Services                        │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐              │
│  │Bilibili│ │SiliconFlow│ │ Vosk  │ │ yt-dlp │             │
│  │  API   │ │  LLM API  │ │ Model │ │        │             │
│  └────────┘ └────────┘ └────────┘ └────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### Core Module Description

#### 1. User Interface Layer

**CLI (main.py)**
- Command-line argument parsing
- Basic I/O handling
- Suitable for scripting and batch processing

**GUI (gui.py)**
- Tkinter-based graphical interface
- Real-time log display
- Report visualization
- Suitable for interactive use

#### 2. Agent Layer

**BiliVagent (agents/bilivagent.py)**

Main responsibilities:
- Parse video BV number or URL
- Coordinate video and text content processing
- Call LLM to generate final analysis report
- Manage overall workflow

Core methods:
```python
def analyze_video(video_url: str) -> dict:
    """Main analysis workflow"""
    # 1. Parse BV number
    # 2. Fetch video information
    # 3. Process video content (download, analyze)
    # 4. Process text content (comments, danmaku)
    # 5. Generate final report
```

#### 3. Processor Layer

**VideoContentProcessor (processors/video_content.py)**

Functional modules:
- **Video Download**: Download videos using yt-dlp
- **Audio Extraction**: Extract audio using MoviePy
- **Speech Recognition**: Convert audio to text using Vosk
- **Content Analysis**: Call LLM to generate summary and keywords
- **Frame Extraction**: Randomly extract video frames
- **Style Analysis**: Analyze video style using VLM

**TextContentProcessor (processors/text_content.py)**

Functional modules:
- **Comment Crawling**: Fetch comments using bilibili-api-python
- **Danmaku Crawling**: Fetch video danmaku
- **Text Desensitization**: Handle sensitive information
- **Keyword Extraction**: Word segmentation and TF-IDF using jieba
- **Sentiment Analysis**: Analyze sentiment using LLM
- **Discussion Summary**: Generate discussion summary

#### 4. Utility Layer

**Bilibili API (utils/bilibili.py)**
- Wrap bilibili-api-python
- Provide unified API interface
- Handle authentication and errors

**Video Processing (utils/video.py)**
- Video download
- Frame extraction
- Video information retrieval

**Audio Processing (utils/audio.py)**
- Audio extraction
- Format conversion
- Speech recognition integration

**Text Processing (utils/text.py)**
- Text cleaning
- Desensitization
- Word segmentation and keyword extraction

**SiliconFlow API (utils/siliconflow.py)**
- LLM API wrapper
- VLM API wrapper
- Request management and error handling

### Data Flow

```
Video URL
    ↓
[Parse BV]
    ↓
[Fetch Metadata] ──→ metadata.json
    ↓
┌───────────────────────┬──────────────────────┐
│                       │                      │
[Download Video]   [Fetch Comments]    [Fetch Danmaku]
    ↓                   ↓                      ↓
[Extract Audio]    [Desensitize]        [Desensitize]
    ↓                   ↓                      ↓
[Speech to Text]   [Merge Text] ←─────────────┘
    ↓                   ↓
[Generate Summary] [Extract Keywords]
    ↓                   ↓
[Extract Keywords] [Sentiment Analysis]
    ↓                   ↓
[Extract Frames]   [Discussion Summary]
    ↓                   ↓
[Analyze Style]    ───→ text_analysis.json
    ↓
video_analysis.json
    │
    ↓
[Combine Results]
    ↓
final_report.json
```

### Configuration Management

**Config (bilivagent/config.py)**

Configuration loading order:
1. Default configuration
2. .env file
3. Environment variables

Supported configuration items:
- API keys and endpoints
- Model selection
- Output paths
- Processing parameters

### Dependencies

```
main.py / gui.py
    ↓
BiliVagent
    ↓
┌─────────────┬──────────────┐
│             │              │
VideoProcessor TextProcessor Config
    ↓              ↓           ↓
┌───┴───┬────┬────┴──┬────┬───┴────┐
│       │    │       │    │        │
Video Audio Text Bilibili SiliconFlow
Utils  Utils Utils  Utils    Utils
```

### Error Handling

The system uses a layered error handling mechanism:

1. **Utility Layer**: Catch and log specific errors
2. **Processor Layer**: Handle or propagate errors, provide fallback
3. **Agent Layer**: Decide whether to continue or terminate analysis
4. **Interface Layer**: Display user-friendly error messages

### Extensibility

The system design considers the following extension points:

- **New Processors**: Inherit from base processor class
- **New API Clients**: Implement unified interface
- **New Analysis Features**: Add new methods in processors
- **New User Interfaces**: Reuse Agent layer logic
