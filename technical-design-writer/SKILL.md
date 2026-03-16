---
name: technical-design-writer
description: Use when writing module-level technical design docs from a completed technical design plan and decision log instead of re-deriving the full design from scratch / 用于基于已完成的技术设计计划和决策记录生成模块级技术设计文档，而不是重新从头推导设计
user-invocable: true
context: fork
---

# Technical Design Writer / 技术设计文档写作

基于已经完成的技术设计写入计划来生成正式技术设计文档。这个 skill 的核心约束是“消费计划产物”，而不是重新自由分析全部上下文。它的目标是把 planner 沉淀的决策、约束和交互要求稳定落到可编码文档中。

## Terms / 术语说明

- `planner`：写入计划阶段，用来沉淀约束、决策和交互要求
- `writer`：正式成文阶段，用来把计划转成最终技术设计文档
- `traceability`：追踪关系，指设计结论能追溯到哪些输入，但默认不直接暴露给最终读者
- `coverage review`：覆盖检查，确认 plan 里的要求没有漏写
- `reverse gap review`：反向漏项检查，从源交互文档反查最终文档是否漏项
- `referenced inputs`：引用输入材料，指最终文档开头列出的参考文档和其影响
- `incremental update`：增量更新，指已有文档时只改受影响章节，不整篇重写
- `open question`：待确认问题，指当前无法稳定定稿、需要保留给后续确认的点

<HARD-GATE>
Do NOT start from freeform interpretation if a planning document exists.

You MUST:
1. read the planning document first
2. treat the plan as the primary input
3. map every required decision and interaction requirement into the final docs
4. flag missing plan inputs instead of silently inventing them
5. run a coverage pass before finishing
6. run a reverse gap check against the source interaction spec when the plan includes one
7. strip planning artifacts from the final technical design docs unless the user explicitly asks to keep them
8. preserve planner-settled final decisions by translating them into direct implementation requirements in the final docs
9. preserve source layout wireframes, textual diagrams, and region-level structure when the planner marks them as fidelity-critical, instead of collapsing them into abstract summary bullets
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

1. **Read the plan first / 先读计划文档**
2. **Validate plan completeness / 校验计划完整性** - 检查决策、风险、writer 交接项和交互要求
3. **Resolve output scope / 确认输出范围** - 明确模块和角色
4. **Write only the needed docs / 只写需要的文档** - 输出到 `docs/03-technical-design/{module}/{role}/`
5. **Map frontend interaction requirements explicitly / 显式映射前端交互要求** - 写进页面和组件文档
6. **Preserve traceability internally / 内部保留追踪关系** - 用 plan 保持准确，但默认不把过程痕迹暴露到最终文档
7. **Run coverage review / 做覆盖检查** - 确认 planner 要求没有遗漏
8. **Run reverse gap review / 做反向漏项检查** - 确认源交互文档中的条目要么已映射，要么被明确排除
9. **Handle incremental updates / 处理增量更新** - 已有文档时只更新变更章节

## Writing Rules / 写作规则

### 1. Consume the Plan, Do Not Re-discover It / 消费计划，不要重新推导

写作时必须优先按计划文档的这些章节展开：
- `Constraints Summary`
- `Decision Log`
- `Frontend Interaction Requirements`
- `Risks And Open Questions`（风险与待确认问题）
- `Writer Handoff`

如果某个设计点在计划文档中不存在，不要默默补一个“看起来合理”的方案。应：
- 标记为缺失输入
- 在最终文档中保留 open question
- 必要时回到 planner 补计划

最终技术设计文档的读者是后续实现者，而不是 planner 的维护者。默认不要在正文里暴露：
- `Plan Ref`
- `Decision ID`
- `Source Section`
- `Architecture Ref`
- 其他中间过程追踪字段

这里的“不要暴露”只适用于来源标签和推理过程，不适用于 planner 已经收敛出的最终结论。

必须保留并转写这些内容：
- planner 已确认的设计结论
- planner 已收敛的交互效果
- planner 已定下的边界、限制、默认值、时序和异常策略

也就是说：
- 去掉的是“这个结论来自哪里”的标签
- 保留的是“这个结论本身”

### 2. Frontend Interaction Must Become Design Content / 前端交互必须进入设计正文

对于 `frontend` 或 `both`：
- 交互要求必须进入 `page-design.md` 和 / 或 `component-design.md`
- 不允许只写成一句“支持交互反馈”
- 必须落到触发条件、状态变化、反馈方式、异常处理、动效或过渡策略
- 如果 planner 中的交互 requirement 是原子项，不允许在 writer 阶段重新合并成泛化描述
- 如果 planner 标记某些页面布局、ASCII 文字图、线框图或区域结构为必须保真，最终文档必须保留等价的文字图、线框描述或分区级结构说明，不能压缩成一句“采用左右布局”
- 如果产品阶段已经明确给出具体布局设计，writer 必须以“忠实转写”为默认策略；只有源材料没有给出对应设计时，才允许在稳定约束内补足

至少覆盖：
- route / entry / permission
- main flow
- loading / empty / error / success
- optimistic update / rollback / retry
- modal / drawer / toast / inline feedback
- animation / transition / skeleton / progressive reveal（如果输入有要求）
- auto-dismiss / auto-collapse / auto-send / delayed reveal（如果输入有要求）

如果 planner 中存在交互规格来源，例如 `*_interactive.md`：
- 必须逐条映射关键 requirement
- 不得只保留“大类状态切换”而丢掉具体效果
- 对未落入当前模块的 requirement，必须在反向漏项检查里说明原因

这里的“逐条映射”是 writer 的内部约束，不代表最终文档必须展示 requirement ID 或来源节号。最终文档应该直接写成实现效果本身。

例如，最终文档应该直接写：
- 默认 40/60 分栏，最小各 30%
- ready 横幅 3 秒自动淡出
- 推荐问题首次发送后收起
- 点击引用后高亮呼吸闪烁 3 次
- 页面布局文字图中左栏承载欢迎态/消息列表，右栏承载 PDF 预览，底栏固定输入区

而不是：
- `覆盖要求：F-CW-02`
- `来源：D-CW-03`

### 3. Final Docs Should Show Results, Not Planning Process / 最终文档展示结果，不展示过程

默认情况下，最终技术设计文档应直接表达：
- 页面或组件最终要实现什么
- 关键交互效果是什么
- 哪些约束来自哪些输入材料

这里的“直接表达结果”不等于“把所有内容压缩成几句摘要”。如果交互源文档里的文字图、线框图、区域结构本身就是实现沟通的重要信息，最终技术设计应保留它们的等价表达，例如：
- ASCII 文字图
- 区域级布局骨架
- 状态面板示意
- 首屏/折叠态/展开态的结构化描述

不要把它写成 planner 的回放记录。除非用户明确要求保留追踪信息，否则不要在最终文档里展示：
- `来源：D-03`
- `覆盖要求：F-02`
- `Source Section: 3.2`
- `Architecture Ref: ...`

如果引用其他文档，应该在文档开头集中列出 `Referenced Inputs`，说明这些材料为什么影响当前设计，而不是在正文里反复夹带追踪标签。

但引用材料清单也不应替代正文里的最终结论。不要把“已引用某文档”误当作“已经把该文档里的决策写进正文”。

### 4. Update Incrementally / 增量更新

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
- 能直接看懂最终设计结果
- 如果引用其他文档，文档开头有清晰的 `Referenced Inputs`
- planner 已收敛的最终决策结果已转写进正文
- 前端交互要求不是附注，而是正文的一部分
- 如果源交互文档含有关键文字图或线框结构，最终文档保留了等价的布局骨架说明，没有被压缩丢失
- 异常、边界条件、依赖关系写清楚
- 计划中的覆盖项没有遗漏
- 交互规格文档中的关键条目要么已落到正文，要么在 gap review 中被明确排除

以下情况视为失败：
- 重新自由发挥，和计划文档脱节
- 漏掉 planner 中的交互要求
- 把 planner 中的原子交互 requirement 重新压扁成大类描述
- 把交互文档中的文字图、线框图、布局骨架压成过短摘要，导致页面结构信息丢失
- 把 planner 的过程痕迹直接暴露给最终文档读者
- 为了去掉过程痕迹，把 planner 已确定的最终决策结果一并删掉
- 只写页面结构，不写行为和反馈
- 用泛化表述替代可执行细节
