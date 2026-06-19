---
title: BiliVagent-tool 领域术语表
type: context
status: active
last_updated: 2026-06-19
---

# CONTEXT.md — BiliVagent-tool 领域术语表

## 项目核心概念

### BiliVagent

基于 Python + LangChain 的 **Bilibili 视频智能分析工具**。输入 BV 号 → 输出多维度分析报告。

### 分析流程（5 阶段）

```
BV 号 / URL
   │
   ▼
1. 视频解析与下载（yt-dlp）
   │
   ▼
2. 评论 + 弹幕爬取
   │
   ▼
3. 视频内容分析
   ├─ 音频提取
   ├─ 语音识别（Vosk）
   └─ 内容概述 + 关键词
   │
   ▼
4. 视觉分析（抽 3 帧 → Qwen3-VL）
   │
   ▼
5. 文本分析
   ├─ 关键词提取
   ├─ 群体情感识别
   └─ 讨论总结
   │
   ▼
报告（BV号 + 标题 + ...）
```

### 模型依赖

| 用途 | 模型 | 备注 |
|---|---|---|
| 文本分析 | SiliconFlow 兼容 LLM | 必需 `.env: SILICONFLOW_API_KEY` |
| 视觉分析 | Qwen3-VL 多模态 | 通过 SiliconFlow API |
| 语音识别 | **Vosk** | 本地模型，需下载并配 `VOSK_MODEL_PATH` |

### 模块结构

```
bilivagent/
├── agents/         # BiliVagent 主类
├── processors/     # 5 阶段处理器
├── utils/
└── config.py
```

## 项目特定命名

| 术语 | 含义 |
|---|---|
| **BV 号** | Bilibili 视频 ID（`BV1xx411c7mD` 格式） |
| **yt-dlp** | 视频下载工具（替代 youtube-dl） |
| **Vosk** | 离线语音识别库 |
| **Qwen3-VL** | 通义千问多模态模型 |
| **SiliconFlow** | 国内 LLM API 服务商（OpenAI 兼容接口） |

## 不混淆概念

- **BiliVagent ≠ BiliBili 官方工具**——非官方第三方
- **Vosk ≠ Whisper**——前者离线、后者需联网/计算重
- **Qwen3-VL ≠ Qwen-VL**——版本号精确
- **bilivagent/ ≠ BiliVagent-tool**——前者是 Python 包目录，后者是仓库名

## 待补

- [ ] bilivagent/processors/ 子模块清单
- [ ] GUI 控件树（gui.py）
- [ ] LangChain 在本项目里的具体角色（推测：工具编排）