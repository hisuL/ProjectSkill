---
name: technical-design
description: Compatibility entry for producing module-level technical design docs by first creating a technical design plan, then writing final docs from that plan / 技术设计兼容入口，先生成写入计划，再基于计划产出模块级技术设计文档
user-invocable: true
context: fork
agent: Plan
---

# Technical Design / 技术设计

这是一个入口 skill，用于兼容用户直接说 `technical-design` 的调用方式。

它本身不负责承载具体业务约束、交互提取规则或正文写作细则，这些内容分别由：

1. `technical-design-planner`
2. `technical-design-writer`

负责。

这个 skill 的职责只有一件事：按正确流程触发前后两个阶段，并确保它们之间的交接完整。

## Terms / 术语说明

- `entry skill`：入口 skill，只负责流程编排，不负责承载详细业务规则
- `planner`：计划阶段，用来先生成技术设计写入计划
- `writer`：写作阶段，用来根据计划生成正式技术设计文档
- `module_id`：技术设计的最小消费单元
- `handoff`：planner 交给 writer 的结构化中间产物

## When To Use / 何时使用

**Use this skill when**:
- 用户直接说 `technical-design`
- 用户希望从 PRD / 架构文档出发，最终得到技术设计文档
- 用户没有明确说明只做 planner 还是只做 writer

**Do NOT use this skill for**:
- 替代 `technical-design-planner` 的具体分析规则
- 替代 `technical-design-writer` 的具体写作规则
- 替代架构设计
- 直接拆实现任务

## Hard Gate / 强约束

Do NOT write final technical design docs immediately after reading source docs.

You MUST:
1. enter Plan mode first
2. run `technical-design-planner` before `technical-design-writer`
3. require a completed planning document before entering writer
4. use `technical-design-writer` only after planner handoff is complete
5. run a final coverage check against the planning document before finishing

## Workflow / 流程

### Phase 1: Planning / 第一阶段：计划沉淀

调用 `technical-design-planner`：
- 读取输入材料
- 收敛模块范围
- 生成 `design-plan.md`
- 准备 writer handoff

### Phase 2: Writing / 第二阶段：正式写作

调用 `technical-design-writer`：
- 读取 `design-plan.md`
- 校验计划完整性
- 生成正式技术设计文档
- 做覆盖检查

## Required Handoff / 必须交接的内容

从 planner 到 writer，至少要有这些内容：
- 模块范围与角色
- 对应的 `module_id`
- 输入材料清单
- 约束摘要
- 决策点清单
- 风险与待确认问题
- `Frontend Interaction Requirements`（如果适用）
- `writer_must_cover`
- `writer_must_not_assume`
- `writer_open_questions`

如果这些内容不完整，不要直接进入 writer。

具体交接字段、交互提取粒度、布局保真要求等，统一以下游 skill 为准：
- `technical-design-planner`
- `technical-design-writer`

## Output Paths / 输出路径

计划文档：

```text
docs/03-technical-design-plans/{module}/design-plan.md
```

正式技术设计文档：

```text
docs/03-technical-design/{module}/backend/api-design.md
docs/03-technical-design/{module}/backend/database-design.md
docs/03-technical-design/{module}/backend/middleware-design.md
docs/03-technical-design/{module}/frontend/page-design.md
docs/03-technical-design/{module}/frontend/component-design.md
```

## Routing Rules / 路由规则

如果用户说：
- “先整理计划” 或 “先沉淀决策点”
  - 直接使用 `technical-design-planner`
- “根据计划写正式文档”
  - 直接使用 `technical-design-writer`
- “technical-design” 但没有说明阶段
  - 默认先 planner 再 writer

## Orchestration Rules / 编排规则

- `technical-design` 是流程入口，不应重复定义 planner / writer 已经拥有的详细规则
- 具体业务约束、交互提取、布局保真、正文质量要求，以下游 skill 为准
- 如果 planner 和 writer 的规则发生演进，入口 skill 不需要重复复制这些细节，只需要保证调用顺序正确

## Why This Skill Exists / 为什么保留这个 skill

保留它的原因不是为了重复定义技术设计规则，而是为了维持旧调用方式不变：

```text
用户继续说 technical-design
内部仍然先 planner，再 writer
```

也就是说，这个 skill 负责“流程入口兼容”，不是“业务规则主定义”。
