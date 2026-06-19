---
title: BiliVagent-tool Domain Docs
type: agents-config
parent: AGENTS.md
---

# Domain Docs

**单上下文布局**——`CONTEXT.md`（根） + `docs/adr/`（入仓） + `工作Wiki/`（不入仓）。

## 何时开 ADR

- 引入新依赖
- 改变 5 阶段流水线结构
- 替换底层模型（如 SiliconFlow → OpenAI）
- GUI 重构

## 何时不开

- bug fix
- 文档更新
- 依赖小版本升级

## BiliVagent 已有 ADR 范本

- `copilot/update-project-documentation`——文档更新
- 多次架构微调（从 commit 推断）