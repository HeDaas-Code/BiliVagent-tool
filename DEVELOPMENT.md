# 开发指南

## 项目架构

### 模块说明

#### 1. bilivagent/config.py
配置管理模块，负责加载环境变量和验证配置。

#### 2. bilivagent/utils/
工具模块集合：

- **bilibili.py**: Bilibili API 封装
  - `BilibiliParser`: 解析 BV 号、获取视频信息、评论、弹幕
  - `BilibiliDownloader`: 使用 yt-dlp 下载视频

- **video.py**: 视频处理
  - `VideoProcessor`: 音频提取、随机帧提取

- **audio.py**: 音频处理
  - `SpeechRecognizer`: 使用 Vosk 进行语音识别

- **text.py**: 文本处理
  - `TextProcessor`: 文本脱敏、关键词提取、词云生成、情感分析

- **siliconflow.py**: SiliconFlow API 客户端
  - `SiliconFlowClient`: 调用 LLM 和 VLM 模型

#### 3. bilivagent/processors/
内容处理器：

- **video_content.py**: 视频内容处理流程
  - 音频提取 → 语音识别 → 生成概述 → 提取关键词 → 视频风格分析

- **text_content.py**: 文本内容处理流程
  - 文本脱敏 → 关键词提取 → 情感分析 → 生成讨论总结

#### 4. bilivagent/agents/
Agent 实现：

- **bilivagent.py**: 主 Agent
  - `BiliVagent`: 编排整个分析流程
  - 集成所有处理器
  - 生成最终报告

## 扩展开发

### 添加新的分析功能

1. 在 `bilivagent/processors/` 中创建新的处理器
2. 在 `BiliVagent.analyze_video()` 中集成新处理器
3. 在报告生成中添加新字段

### 添加新的数据源

1. 在 `bilivagent/utils/bilibili.py` 中添加新的 API 方法
2. 在相应的处理器中使用新数据

### 自定义模型

编辑 `.env` 文件中的模型配置：

```bash
LLM_MODEL=your-preferred-llm-model
VLM_MODEL=your-preferred-vlm-model
```

## API 接口说明

### SiliconFlow API

#### Chat Completion

```python
from bilivagent.utils.siliconflow import SiliconFlowClient

client = SiliconFlowClient()
messages = [
    {"role": "system", "content": "你是一个助手"},
    {"role": "user", "content": "你好"}
]
response = client.chat_completion(messages)
```

#### Vision Analysis

```python
response = client.vision_analysis(
    image_path="path/to/image.jpg",
    prompt="分析这张图片"
)
```

## 测试

### 单元测试

可以为各个模块编写单元测试：

```python
# test_text_processor.py
from bilivagent.utils.text import TextProcessor

def test_desensitize():
    processor = TextProcessor()
    text = "我的手机号是13800138000"
    result = processor.desensitize_text(text)
    assert "***" in result
    assert "13800138000" not in result
```

### 集成测试

```bash
# 测试完整流程
python main.py BV1xx411c7mD
```

## 性能优化建议

1. **并行处理**: 可以使用多线程处理评论和弹幕的文本分析
2. **缓存**: 对已分析的视频进行缓存，避免重复处理
3. **增量更新**: 只处理新增的评论和弹幕
4. **批量 API 调用**: 合并多个小的 API 请求

## 调试技巧

### 启用详细日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 跳过视频下载

当测试文本分析功能时，可以跳过视频下载：

```bash
python main.py --no-download BV1xx411c7mD
```

### 使用本地视频文件

直接修改代码指定本地视频文件路径，跳过下载步骤。

## 常见问题

### Q: 如何处理网络错误？

A: 所有网络请求都有异常处理，会打印错误信息并继续执行。可以增加重试逻辑。

### Q: 如何优化 API 调用次数？

A: 
- 减少不必要的 API 调用
- 使用更小的 max_tokens
- 批量处理内容

### Q: 如何支持其他视频网站？

A: 在 `bilivagent/utils/` 中添加新的下载器和解析器，参考 `bilibili.py` 的实现。

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 使用 Python 3.8+ 语法
- 遵循 PEP 8 代码风格
- 添加适当的注释和文档字符串
- 所有公共方法都应有类型提示

## 版本历史

- v1.0.0 (2024): 初始版本
  - 基础视频分析功能
  - SiliconFlow API 集成
  - 完整的分析流程

## 许可证

MIT License - 详见 LICENSE 文件
