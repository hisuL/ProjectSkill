---
name: pingcode-skill
description: Use when working with PingCode projects, work items, or project members from Codex, including listing projects, reading tasks, creating projects or work items, managing members, and breaking a story into executable subtasks / 用于在 Codex 中操作 PingCode 项目、工作项和项目成员，包括列项目、查任务、建项目、建工作项、管理成员和把用户故事拆成可执行子任务
user-invocable: true
context: fork
agent: Default
---

# PingCode Skill

把 PingCode 相关操作封装成可复用的 Codex skill。

## When To Use

在这些场景使用：

- 用户要求查看 PingCode 项目或工作项
- 用户要求创建项目、需求、任务、缺陷或子任务
- 用户要求查看、添加、更新、移除项目成员
- 用户希望把一个 PingCode 用户故事拆解成多个执行子任务

不要在这些场景使用：

- 仅讨论项目管理方法论，但不需要实际调用 PingCode
- 需要访问其他平台而不是 PingCode

## Required Environment

优先使用环境变量，不要在脚本里硬编码密钥：

- `PINGCODE_BASE_URL`
  - 可选，默认 `https://open.pingcode.com`
- `PINGCODE_ACCESS_TOKEN`
  - 推荐。若已提供，脚本直接使用它调用 API
- `PINGCODE_CLIENT_ID`
  - 当没有 `PINGCODE_ACCESS_TOKEN` 时必填
- `PINGCODE_CLIENT_SECRET`
  - 当没有 `PINGCODE_ACCESS_TOKEN` 时必填

鉴权规则：

- 如果存在 `PINGCODE_ACCESS_TOKEN`，直接使用
- 否则尝试用 `PINGCODE_CLIENT_ID` + `PINGCODE_CLIENT_SECRET` 申请 token
- 如果两种方式都不满足，先提示用户补齐环境变量

## Primary Script

统一入口：

```bash
python3 pingcode-skill/scripts/pingcode_cli.py --help
```

常用子命令：

- `list-projects`
- `get-task`
- `create-project`
- `create-work-item`
- `update-work-item`
- `get-members`
- `add-member`
- `update-member`
- `remove-member`
- `breakdown-story`

浏览器授权辅助脚本：

```bash
python3 pingcode-skill/scripts/pingcode_authorize.py
```

只有在用户明确要走浏览器授权码流程时才使用它。

## Working Rules

- 先确认鉴权环境是否满足，再发起写操作
- 写操作前，向用户回显关键参数：项目、标题、工作项类型、成员或角色
- 当工作项已经存在且仅标题、描述、父子关系或状态发生变化时，优先使用 `update-work-item` 同步，而不是重复创建
- 如果是破坏性或敏感操作，例如移除成员，先明确目标 ID
- `breakdown-story` 只用于可挂子任务的父工作项；如果目标不是 `story`，直接报错并说明原因
- 默认输出简洁结果；若用户要原始响应，再加 `--raw`

## Examples

列项目：

```bash
python3 pingcode-skill/scripts/pingcode_cli.py list-projects
```

按标识符查项目：

```bash
python3 pingcode-skill/scripts/pingcode_cli.py list-projects --identifier DEMO
```

查询任务：

```bash
python3 pingcode-skill/scripts/pingcode_cli.py get-task --identifier DEMO-123
```

创建工作项：

```bash
python3 pingcode-skill/scripts/pingcode_cli.py create-work-item \
  --project-id 123456 \
  --title "实现登录页" \
  --type task \
  --description "支持用户名密码登录"
```

更新工作项：

```bash
python3 pingcode-skill/scripts/pingcode_cli.py update-work-item \
  --work-item-id 123456 \
  --title "更新后的标题" \
  --description "更新后的描述"
```

拆解用户故事：

```bash
python3 pingcode-skill/scripts/pingcode_cli.py breakdown-story --identifier DEMO-123
```

## Implementation Notes

- 具体 API 调用封装在 `scripts/pingcode_client.py`
- 如需修改接口路径或请求体，优先改共享客户端，不要复制逻辑到多个脚本
