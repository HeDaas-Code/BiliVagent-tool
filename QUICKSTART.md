# 快速开始指南

## 5 分钟快速上手

### 1. 安装 (2 分钟)

```bash
# 克隆项目
git clone https://github.com/HeDaas-Code/BiliVagent-tool.git
cd BiliVagent-tool

# 安装依赖
pip install -r requirements.txt
pip install yt-dlp

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 SILICONFLOW_API_KEY
```

### 2. 获取 API Key (1 分钟)

1. 访问 https://siliconflow.cn
2. 注册账号
3. 进入控制台创建 API Key
4. 复制 API Key 到 `.env` 文件

### 3. 运行分析 (2 分钟)

```bash
# 基本使用
python main.py BV1xx411c7mD

# 或使用完整链接
python main.py https://www.bilibili.com/video/BV1xx411c7mD
```

## 功能演示

### 示例 1: 分析科技视频

```bash
python main.py BV1uv411q7Mv
```

输出内容包括：
- ✓ 视频基本信息
- ✓ 内容概述
- ✓ 关键词提取
- ✓ 视频风格分析
- ✓ 评论情感分析
- ✓ 讨论总结

### 示例 2: 仅分析文本（不下载视频）

```bash
python main.py --no-download BV1uv411q7Mv
```

适用场景：
- 只关心评论和弹幕分析
- 网络条件不佳
- 节省存储空间

## 高级配置

### 自定义输出目录

```bash
python main.py -o ./my_reports BV1xx411c7mD
```

### 使用不同的模型

编辑 `.env`:

```bash
# 使用其他 LLM 模型
LLM_MODEL=Qwen/Qwen2.5-72B-Instruct

# 使用其他 VLM 模型  
VLM_MODEL=Qwen/Qwen2-VL-72B-Instruct
```

## 输出说明

### JSON 报告格式

```json
{
  "BV号": "BV1xx411c7mD",
  "视频标题": "标题内容",
  "概述": "视频内容概述...",
  "关键词（前十）": ["关键词1", "关键词2", ...],
  "视频风格": "画面风格描述",
  "讨论情感": "正面/负面/中性",
  "讨论关键词": ["讨论词1", "讨论词2", ...],
  "相关讨论": "讨论内容总结...",
  "元数据": {
    "分区": "科技",
    "标签": ["tag1", "tag2"],
    "UP主": "UP主名称",
    "时长": 300,
    "评论数": 100,
    "弹幕数": 500
  }
}
```

### 文件位置

- **报告文件**: `./output/{BV号}_report.json`
- **临时文件**: `./temp/` (视频、音频、截图)

## 常见场景

### 场景 1: 内容创作者分析自己的视频

```bash
# 分析视频表现
python main.py BV你的视频号

# 查看报告了解：
# - 观众对内容的反馈
# - 热门讨论点
# - 整体情感倾向
```

### 场景 2: 市场研究人员分析竞品

```bash
# 批量分析（使用脚本）
for bv in BV1xx BV2yy BV3zz; do
    python main.py $bv
    sleep 5
done

# 对比多个视频的数据
```

### 场景 3: 学术研究

```bash
# 分析特定主题的视频
python main.py BV主题视频号

# 提取关键词和讨论内容用于研究
```

## 故障排除

### 问题 1: "SILICONFLOW_API_KEY is required"

**解决方案**: 
```bash
# 确保 .env 文件存在且配置正确
cat .env | grep SILICONFLOW_API_KEY
# 应该显示: SILICONFLOW_API_KEY=sk-xxxxx
```

### 问题 2: 视频下载失败

**可能原因**:
- yt-dlp 未安装
- 网络连接问题
- 视频有地区限制

**解决方案**:
```bash
# 检查 yt-dlp
yt-dlp --version

# 如果未安装
pip install yt-dlp

# 或跳过视频下载
python main.py --no-download BV号
```

### 问题 3: 语音识别不工作

**解决方案**:
```bash
# 下载 Vosk 模型
mkdir -p models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip
unzip vosk-model-cn-0.22.zip
cd ..

# 更新 .env 中的模型路径
echo "VOSK_MODEL_PATH=./models/vosk-model-cn-0.22" >> .env
```

### 问题 4: API 调用超时

**解决方案**:
- 检查网络连接
- 增加超时时间（修改代码中的 timeout 参数）
- 稍后重试

## 性能提示

### 提升速度

1. **跳过不需要的功能**:
   - 使用 `--no-download` 跳过视频下载
   - 减少评论和弹幕的抓取数量

2. **使用更快的模型**:
   - 选择较小的 LLM 模型（如 7B 而不是 32B）

3. **本地缓存**:
   - 避免重复分析同一视频

### 节省成本

1. **减少 API 调用**:
   - 使用更短的 max_tokens
   - 只分析必要的内容

2. **批量处理**:
   - 一次性处理多个视频
   - 合理使用 API 配额

## 下一步

- 📖 阅读完整文档: [README.md](README.md)
- 🔧 开发指南: [DEVELOPMENT.md](DEVELOPMENT.md)
- 🐛 报告问题: [GitHub Issues](https://github.com/HeDaas-Code/BiliVagent-tool/issues)
- 💡 功能建议: [GitHub Discussions](https://github.com/HeDaas-Code/BiliVagent-tool/discussions)

## 获取帮助

```bash
# 查看帮助信息
python main.py --help

# 检查安装状态
python check_setup.py
```

---

**享受使用 BiliVagent-tool! 🎉**
