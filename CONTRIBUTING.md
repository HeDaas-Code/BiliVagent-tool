# 贡献指南

[English](CONTRIBUTING_EN.md) | 中文

感谢您对 BiliVagent-tool 项目的关注！我们欢迎任何形式的贡献。

## 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发环境设置](#开发环境设置)
- [提交规范](#提交规范)
- [代码风格](#代码风格)
- [测试](#测试)
- [文档](#文档)

## 行为准则

本项目采用贡献者公约。参与此项目即表示您同意遵守其条款。请保持友好、尊重和包容的态度。

## 如何贡献

### 报告 Bug

如果您发现了 Bug，请通过 GitHub Issues 报告：

1. 使用清晰的标题描述问题
2. 详细描述重现步骤
3. 说明预期行为和实际行为
4. 提供环境信息（操作系统、Python 版本等）
5. 如果可能，附上错误日志和截图

### 提出功能建议

我们欢迎新功能建议：

1. 检查 Issues 中是否已有类似建议
2. 创建新 Issue，使用 `enhancement` 标签
3. 清晰描述功能和使用场景
4. 说明为什么这个功能对项目有价值

### 提交代码

1. **Fork 项目**
   ```bash
   # 在 GitHub 上 Fork 项目
   git clone https://github.com/your-username/BiliVagent-tool.git
   cd BiliVagent-tool
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **进行更改**
   - 遵循代码风格指南
   - 添加必要的测试
   - 更新相关文档

4. **提交更改**
   ```bash
   git add .
   git commit -m "描述你的更改"
   ```

5. **推送到 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **创建 Pull Request**
   - 在 GitHub 上创建 PR
   - 填写 PR 模板
   - 链接相关的 Issue

## 开发环境设置

### 1. 克隆仓库

```bash
git clone https://github.com/HeDaas-Code/BiliVagent-tool.git
cd BiliVagent-tool
```

### 2. 创建虚拟环境

```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 或使用 conda
conda create -n bilivagent python=3.8
conda activate bilivagent
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

### 5. 运行测试

```bash
python -m pytest tests/
```

## 提交规范

我们使用约定式提交（Conventional Commits）规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例

```
feat(video): 添加视频质量选择功能

增加了用户可以选择下载视频质量的功能，支持 1080p, 720p, 480p

Closes #123
```

```
fix(gui): 修复进度条不更新的问题

在某些情况下进度条会卡住不动，已通过线程同步机制修复

Fixes #456
```

## 代码风格

### Python 代码规范

我们遵循 PEP 8 规范：

- 使用 4 个空格缩进
- 每行最多 88 个字符（Black 默认）
- 使用有意义的变量名
- 为函数和类添加文档字符串
- 导入顺序：标准库 → 第三方库 → 本地库

### 命名规范

- 类名：`PascalCase`
- 函数和变量：`snake_case`
- 常量：`UPPER_SNAKE_CASE`
- 私有成员：`_leading_underscore`

### 文档字符串

```python
def analyze_video(video_url: str) -> dict:
    """
    分析 Bilibili 视频并生成报告
    
    Args:
        video_url: Bilibili 视频 URL 或 BV 号
    
    Returns:
        包含分析结果的字典
    
    Raises:
        ValueError: 当视频 URL 无效时
        APIError: 当 API 调用失败时
    """
    pass
```

## 测试

### 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行特定测试文件
python -m pytest tests/test_video.py

# 查看覆盖率
python -m pytest --cov=bilivagent
```

### 编写测试

- 为新功能添加测试
- 确保测试覆盖边界情况
- 使用描述性的测试名称
- 测试应该是独立的

```python
def test_parse_bv_number_from_url():
    """测试从 URL 中解析 BV 号"""
    url = "https://www.bilibili.com/video/BV1xx411c7mD"
    result = parse_bv_number(url)
    assert result == "BV1xx411c7mD"
```

## 文档

### 更新文档

如果您的更改影响到用户使用方式，请更新相应文档：

- `README.md` / `README_EN.md`: 主要文档
- `CONTRIBUTING.md` / `CONTRIBUTING_EN.md`: 贡献指南
- `CHANGELOG.md`: 更新日志
- 代码注释和文档字符串

### 文档风格

- 使用清晰简洁的语言
- 提供代码示例
- 包含截图（如适用）
- 中英文文档保持同步

## Pull Request 流程

1. 确保代码通过所有测试
2. 更新相关文档
3. 在 PR 描述中说明更改内容
4. 链接相关 Issue
5. 等待代码审查
6. 根据反馈进行修改
7. PR 被合并后，删除分支

## 代码审查

所有提交都需要通过代码审查：

- 保持友好和建设性
- 解释"为什么"而不只是"什么"
- 尊重不同的观点和经验水平
- 及时响应反馈

## 获取帮助

如有疑问，可以：

- 查看已有的 Issues 和 Discussions
- 创建新的 Issue 询问
- 在 PR 中提出问题

## 许可证

提交代码即表示您同意将代码以 MIT 许可证授权给项目。

---

再次感谢您的贡献！🎉
