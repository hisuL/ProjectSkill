---
name: technical-design-writer
description: Use when writing module-level technical design docs from a completed technical design plan and decision log instead of re-deriving the full design from scratch
user-invocable: true
context: fork
---

# Technical Design Writer / 技术设计文档写作

基于已经完成的技术设计写入计划来生成正式技术设计文档。这个 skill 的核心约束是“消费计划产物”，而不是重新自由分析全部上下文。它的目标是把 planner 沉淀的决策、约束和交互要求稳定落到可编码文档中。

<HARD-GATE>
Do NOT start from freeform interpretation if a planning document exists.

You MUST:
1. read the planning document first
2. treat the plan as the primary input
3. map every required decision and interaction requirement into the final docs
4. flag missing plan inputs instead of silently inventing them
5. run a coverage pass before finishing
</HARD-GATE>

## Scope / 使用范围

**Use this skill when**:
- 已经存在 `technical-design-planner` 产出的计划文档
- 用户要把计划文档写成正式技术设计
- 需要避免因上下文变长导致的设计遗漏

**Do NOT use this skill for**:
- 还没有计划文档时直接生成正式设计
- 替代架构设计
- 重新主持分阶段设计讨论

如果缺少计划文档，可以读取原始 PRD 和架构文档做最小兜底，但必须明确说明这是降级路径，稳定性较差。

## Required Inputs / 必须输入

优先读取：
- `docs/03-technical-design-plans/{module}/design-plan.md`

必要时补读：
- `docs/01-prd/PRD.md`
- `docs/02-architecture/architecture-design.md`
- 计划文档中列出的关键引用材料

默认原则：
- 计划文档是主输入
- 原始文档只用于校验和补足，不用于推翻已沉淀决策

## Checklist / 执行清单

You MUST complete these steps in order:

1. **Read the plan first**
2. **Validate plan completeness** - check decisions, risks, writer handoff, and interaction requirements
3. **Resolve output scope** - module and role
4. **Write only the needed docs** under `docs/03-technical-design/{module}/{role}/`
5. **Map frontend interaction requirements explicitly** into page and component docs
6. **Preserve traceability** - connect key choices back to plan IDs or source sections
7. **Run coverage review** - confirm no planner requirements were dropped
8. **Handle incremental updates** - update changed sections only if docs already exist

## Writing Rules / 写作规则

### 1. Consume the Plan, Do Not Re-discover It

写作时必须优先按计划文档的这些章节展开：
- `Constraints Summary`
- `Decision Log`
- `Frontend Interaction Requirements`
- `Risks And Open Questions`
- `Writer Handoff`

如果某个设计点在计划文档中不存在，不要默默补一个“看起来合理”的方案。应：
- 标记为缺失输入
- 在最终文档中保留 open question
- 必要时回到 planner 补计划

### 2. Frontend Interaction Must Become Design Content

对于 `frontend` 或 `both`：
- 交互要求必须进入 `page-design.md` 和 / 或 `component-design.md`
- 不允许只写成一句“支持交互反馈”
- 必须落到触发条件、状态变化、反馈方式、异常处理、动效或过渡策略

至少覆盖：
- route / entry / permission
- main flow
- loading / empty / error / success
- optimistic update / rollback / retry
- modal / drawer / toast / inline feedback
- animation / transition / skeleton / progressive reveal（如果输入有要求）

### 3. Use Plan IDs for Traceability

如果 planner 中有 `Decision ID` 或交互 requirement ID，在正式文档中应显式引用，例如：
- `来源：D-03`
- `覆盖要求：F-02`

不要求机械地每段都标 ID，但关键设计块要可追溯。

### 4. Update Incrementally

如果目标文件已存在，不要整篇重写。必须：
1. 读取旧版本
2. 只更新受影响章节
3. 添加更新标记：`<!-- UPDATED: YYYY-MM-DD -->`
4. 如果是破坏性调整，添加：`<!-- BREAKING: 说明 -->`
5. 更新 frontmatter 中的 `version` 和 `change_log`

## ⚠️ Front 文档边界约束

前端相关文档只描述业务层内容，以下内容禁止出现前端文档中：
- ❌ 组件文件路径或目录结构
- ❌ 编码规范相关约束（命名规则、禁止项等）

## Output Paths / 输出路径

```text
docs/03-technical-design/{module}/backend/api-design.md
docs/03-technical-design/{module}/backend/database-design.md
docs/03-technical-design/{module}/backend/middleware-design.md
docs/03-technical-design/{module}/frontend/page-design.md
docs/03-technical-design/{module}/frontend/component-design.md
```

章节骨架见 [references/templates.md](references/templates.md)。

## Quality Bar / 质量要求

合格文档至少满足：
- 能直接支持编码
- 能看出哪些内容来自 planner
- 前端交互要求不是附注，而是正文的一部分
- 异常、边界条件、依赖关系写清楚
- 计划中的覆盖项没有遗漏

以下情况视为失败：
- 重新自由发挥，和计划文档脱节
- 漏掉 planner 中的交互要求
- 只写页面结构，不写行为和反馈
- 用泛化表述替代可执行细节
