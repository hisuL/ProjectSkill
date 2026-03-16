---
name: technical-design
description: Compatibility entry for producing module-level technical design docs by first creating a technical design plan, then writing final docs from that plan / 技术设计兼容入口，先生成写入计划，再基于计划产出模块级技术设计文档
user-invocable: true
context: fork
agent: Plan
---

# Technical Design / 技术设计

这是一个兼容入口 skill，用于承接原来的 `technical-design` 使用方式。它本身不再承载完整流程，而是把工作显式拆成两个阶段：

1. 先用 `technical-design-planner`
2. 再用 `technical-design-writer`

这样做的目的，是把 PRD、架构设计、引用文档里的约束和前端交互要求先固化成计划文档，再基于该计划稳定生成正式技术设计，避免在长链路写作中丢上下文。

## Terms / 术语说明

- `compatibility entry`：兼容入口，指保留旧调用方式，但内部改成新流程
- `planner`：技术设计计划阶段，用来沉淀约束、决策点和交互要求
- `writer`：技术设计写作阶段，用来把 plan 转成正式文档
- `module_id`：模块唯一标识，是技术设计最小消费单元
- `handoff`：交接信息，指 planner 交给 writer 的结构化中间产物
- `coverage check`：覆盖检查，确认 plan 里的要求都进入了最终文档

## When To Use / 何时使用

**Use this skill when**:
- 用户仍然习惯直接说 `technical-design`
- 需要从 PRD 和架构设计出发，最终产出模块级技术设计文档
- 希望由兼容入口自动引导到新的两段式流程

**Do NOT use this skill for**:
- 跳过计划阶段直接写正式技术设计
- 替代架构设计
- 直接拆实现任务

## Hard Gate / 强约束

Do NOT write final technical design docs immediately after reading source docs.

You MUST:
1. enter Plan mode first
2. use `technical-design-planner` to produce `docs/03-technical-design-plans/{module}/design-plan.md`
3. treat architecture module handoff cards and dependency contract summaries as the primary boundary input
4. ensure the plan explicitly records frontend interaction requirements and decision points
5. use `technical-design-writer` to write final docs from the plan
6. run a final coverage check against the plan before finishing

## Compatibility Workflow / 兼容流程

把这个 skill 当作一个 `orchestrator`（流程编排入口）：

### Phase 1: Planning / 第一阶段：计划沉淀

调用 `technical-design-planner`，完成：
- 读取 PRD、架构文档、引用文档和图片
- 优先解析模块交接卡、依赖契约摘要和工作项清单
- 以 `module_id` 为唯一消费单元收敛模块和角色
- 提取约束、决策点、风险、未决问题
- 单独提取 `Frontend Interaction Requirements`
- 生成 `design-plan.md`（技术设计写入计划）

### Phase 2: Writing / 第二阶段：正式写作

调用 `technical-design-writer`，完成：
- 读取 `design-plan.md`
- 校验计划完整性
- 把计划中的约束和决策写入正式技术设计文档
- 把前端交互要求映射进 `page-design.md` / `component-design.md`
- 做覆盖检查，确认没有漏掉 planner 中的要求

## Required Handoff / 必须交接的内容

从 planner 到 writer，至少要有这些内容：
- 模块范围与角色
- 对应的 `module_id`
- 模块交接卡摘要
- 依赖契约摘要
- 输入材料清单
- 约束摘要
- 决策点清单
- 风险与待确认问题
- `Frontend Interaction Requirements`
- `writer_must_cover`
- `writer_must_not_assume`
- `writer_open_questions`

如果这些内容不完整，不要直接进入 writer。

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
  直接使用 `technical-design-planner`
- “根据计划写正式文档”
  直接使用 `technical-design-writer`
- “technical-design” 但没有说明阶段
  默认先 planner 再 writer

## Boundary Rules / 边界规则

`technical-design` 必须优先消费架构文档中的：
- 模块交接卡
- 依赖契约摘要
- 工作项清单

并遵守这些规则：
- 技术设计的最小单元始终是 `module_id`
- 不要把 `work item` 直接当成目录名或重新解释成新模块
- 不要按 `service` 重新拆分技术设计边界
- 如果架构交接信息不足，应回补 `architecture-design`，而不是在技术设计阶段自由重定义边界

## Why This Split Exists / 为什么拆成两段

原来的单 skill 流程容易在正式写作阶段丢掉前期已识别的约束，尤其是前端交互效果、状态反馈和引用文档中的体验要求。

现在的兼容入口必须坚持这个原则：

```text
先固化计划，再生成文档
先记录交互要求，再落前端设计
```

如果用户明确要求保留旧调用方式，这个 skill 应该维持调用体验不变，但内部仍遵循新流程。
