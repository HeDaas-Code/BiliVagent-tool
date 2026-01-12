# 更新日志 / Changelog

[中文](#中文) | [English](#english)

## 中文

所有项目的重要变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

### [Unreleased]

#### 新增
- 完善的中英文双语文档
- 贡献指南（CONTRIBUTING.md）
- 更新日志（CHANGELOG.md）

### [0.2.0] - 2026-01-12

#### 新增
- 全新的图形用户界面（GUI）使用 Tkinter 实现
  - 可视化视频链接输入
  - 实时分析进度显示
  - 多标签页显示日志和报告
  - 报告导出功能（JSON/文本格式）
  - 清空日志功能
- GUI 中的状态指示和进度条
- 线程安全的输出重定向机制
- 改进的视频分析流程

#### 改进
- 优化了视频处理性能
- 改进了错误处理和用户反馈
- 增强了代码结构和模块化

#### 修复
- 修复了某些情况下进度条不更新的问题
- 修复了字符编码问题

### [0.1.0] - 2026-01-10

#### 新增
- 初始版本发布
- 基于 LangChain 的智能 Agent 架构
- Bilibili 视频下载功能（使用 yt-dlp）
- 视频内容分析
  - 音频提取和语音识别（Vosk）
  - 视频帧提取和风格分析（Qwen3-VL）
  - 内容概述生成
  - 关键词提取
- 评论和弹幕分析
  - 评论和弹幕爬取
  - 文本脱敏处理
  - 情感分析
  - 讨论总结
- 命令行界面（CLI）
- 完整的分析报告生成（JSON 格式）
- 配置文件支持（.env）
- 基础文档（README.md）

#### 技术栈
- Python 3.8+
- LangChain
- SiliconFlow API (Qwen 模型系列)
- Vosk 语音识别
- MoviePy 视频处理
- OpenCV 图像处理
- jieba 中文分词
- bilibili-api-python

---

## English

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [Unreleased]

#### Added
- Complete bilingual documentation (Chinese and English)
- Contributing guidelines (CONTRIBUTING.md)
- Changelog (CHANGELOG.md)

### [0.2.0] - 2026-01-12

#### Added
- Brand new Graphical User Interface (GUI) built with Tkinter
  - Visual video link input
  - Real-time analysis progress display
  - Multi-tab display for logs and reports
  - Report export functionality (JSON/text formats)
  - Clear log functionality
- Status indicators and progress bars in GUI
- Thread-safe output redirection mechanism
- Improved video analysis workflow

#### Improved
- Optimized video processing performance
- Enhanced error handling and user feedback
- Better code structure and modularity

#### Fixed
- Fixed progress bar not updating in certain situations
- Fixed character encoding issues

### [0.1.0] - 2026-01-10

#### Added
- Initial release
- Intelligent Agent architecture based on LangChain
- Bilibili video download functionality (using yt-dlp)
- Video content analysis
  - Audio extraction and speech recognition (Vosk)
  - Video frame extraction and style analysis (Qwen3-VL)
  - Content summary generation
  - Keyword extraction
- Comment and danmaku analysis
  - Comment and danmaku crawling
  - Text desensitization processing
  - Sentiment analysis
  - Discussion summary
- Command Line Interface (CLI)
- Complete analysis report generation (JSON format)
- Configuration file support (.env)
- Basic documentation (README.md)

#### Tech Stack
- Python 3.8+
- LangChain
- SiliconFlow API (Qwen model series)
- Vosk speech recognition
- MoviePy video processing
- OpenCV image processing
- jieba Chinese word segmentation
- bilibili-api-python

---

## 版本链接 / Version Links

- [Unreleased]: https://github.com/HeDaas-Code/BiliVagent-tool/compare/v0.2.0...HEAD
- [0.2.0]: https://github.com/HeDaas-Code/BiliVagent-tool/compare/v0.1.0...v0.2.0
- [0.1.0]: https://github.com/HeDaas-Code/BiliVagent-tool/releases/tag/v0.1.0
