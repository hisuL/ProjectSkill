---
version: 1.0.0
status: draft
module: conversation-orchestrator
role: both
change_log:
  - version: 1.0.0
    date: 2026-03-16
    changes: initial version
---

# Design Plan

## 1. Module Scope And Role
- `module_id`: `conversation-orchestrator`
- `role`: `both`
- 目标：完成单文档检索问答、流式输出、引用装配、多轮会话、摘要推荐和反馈。
- 范围内：
  - 按 `doc_id` 检索和低相关拒答
  - SSE/流式回答时序
  - 引用锚点与引用列表组装
  - 最近 10 轮会话窗口
  - 摘要、推荐问题、点赞点踩反馈
- 不在范围内：
  - 文档解析与向量生成
  - 完整页面骨架和 PDF 预览主布局

## 2. Referenced Inputs
- `docs/01-prd/PRD.md`
  - 规定 Top-5 检索、低相关拒答、引用锚点、多轮历史 10 轮、摘要与推荐问题、反馈标签。
- `docs/01-prd/research.md`
  - 提供 Haystack、litellm 和检索生成链路参考。
- `docs/01-prd/ChatFile_interactive.md`
  - 给出流式输出时序、引用 hover/点击、高亮联动、无结果、服务异常、反馈面板等交互。
- `docs/02-architecture/architecture-design.md`
  - 固化模块数据归属、流式响应、前后端责任和 `page_owner_module` 相关边界。

## 3. Constraints Summary
- 检索必须严格限定当前 `doc_id`，禁止跨文档召回。
- 默认返回 Top-5 chunk，低于阈值时直接拒答。
- 输出必须附带引用锚点 `[1]...[n]` 及引用列表元数据。
- 维护最近 `10 轮` 对话历史，超出部分折叠。
- 生成必须支持中断，保留已生成文本并标记“回答已中断”。
- 反馈标签至少支持：`回答不准确`、`引用错误`、`信息不完整`、`答非所问`。
- 摘要 `<= 200 字`，推荐问题固定 `3` 条。
- 页面完整骨架由 `chatfile-web` 承接，本模块只定义对话区和消息级交互结果。

## 4. Decision Log
| Decision | Final Direction | Rationale |
| --- | --- | --- |
| 检索链路 | 直接向量检索 Top-5，不引入 Rerank | 与 PRD 明确排除项一致 |
| 上下文窗口 | 截取最近 10 轮会话 + 当前问题 | 满足追问能力并控制 prompt 长度 |
| 流式协议 | 后端以 SSE 输出状态事件和 token 事件 | 对应交互稿中的检索态、生成态和 stop |
| 引用结构 | 回答正文内嵌 `[n]`，完成态返回引用列表含页码、章节路径、摘要 | 支撑 hover、点击跳转和引用面板 |
| 摘要/推荐生成 | 文档 ready 后异步预生成，失败不阻塞问答 | 兼顾首屏体验和主链路稳定性 |
| 反馈存储 | 正负反馈都写消息级记录，负反馈带多选标签和补充文本 | 支撑后续质量回看 |

## 5. Frontend Interaction Requirements
### 对话区与消息交互
- `CO-FR-01`
  - 原始要求摘要：用户发送后先出现“正在检索相关内容...”，再切换到“正在生成回答...”
  - 影响区域：对话区消息流
  - 触发条件：发送消息后
  - 状态变化：输入框禁用，发送按钮变停止按钮
  - 反馈方式：阶段状态文案 + 流式气泡
  - 动效或过渡：状态切换后进入逐 token 渲染
- `CO-FR-02`
  - 原始要求摘要：生成过程中支持 stop，中断后保留已生成文本并标记“回答已中断”
  - 影响区域：AI 消息气泡
  - 触发条件：用户点击停止
  - 状态变化：流结束但消息非完成态
  - 反馈方式：灰色中断提示
- `CO-FR-03`
  - 原始要求摘要：引用标记 hover 显示摘要前 80 字，点击触发 PDF 跳页并高亮
  - 影响区域：消息正文、引用列表
  - 触发条件：hover / click 引用
  - 状态变化：引用列表与 PDF 预览区联动
  - 反馈方式：蓝色链接、tooltip、跳转事件
- `CO-FR-04`
  - 原始要求摘要：引用来源块默认展开，可折叠/展开
  - 影响区域：AI 消息气泡底部
  - 触发条件：回答生成完成或用户切换
  - 状态变化：引用块高度展开/收起
  - 反馈方式：淡入和高度动画
- `CO-FR-05`
  - 原始要求摘要：无结果时不显示引用来源和复制按钮，但保留反馈按钮
  - 影响区域：AI 消息气泡
  - 触发条件：低相关拒答
- `CO-FR-06`
  - 原始要求摘要：反馈面板从消息底部滑出，支持多选标签、最多 200 字补充说明
  - 影响区域：消息反馈区
  - 触发条件：用户点踩
- `CO-FR-07`
  - 原始要求摘要：复制按钮复制纯文本，不含引用标记，成功后 toast `已复制到剪贴板`
  - 影响区域：消息操作区
  - 触发条件：点击复制

### 欢迎态与推荐问题
- `CO-FR-08`
  - 原始要求摘要：ready 后显示 `<= 200 字` 摘要，淡入展示
  - 影响区域：欢迎态摘要卡
  - 触发条件：文档 ready 且对话为空
- `CO-FR-09`
  - 原始要求摘要：3 个推荐问题为可点击胶囊按钮，点击后自动发送，首次发送后收起
  - 影响区域：欢迎态推荐区
  - 触发条件：ready 后或首次消息发送
- `CO-FR-10`
  - 原始要求摘要：历史超过 10 轮时旧消息灰化折叠，显示“查看更多历史”
  - 影响区域：消息列表
  - 触发条件：历史轮次超限

### 异常与服务状态
- `CO-FR-11`
  - 原始要求摘要：服务不可用时返回 503 和请求 ID，支持重试
  - 影响区域：错误消息卡
  - 触发条件：检索或生成服务异常
- `CO-FR-12`
  - 原始要求摘要：连续 3 次失败后禁用输入框 30 秒
  - 影响区域：输入区
  - 触发条件：连续错误计数达到阈值
- `CO-FR-13`
  - 原始要求摘要：30 秒无响应视为超时，提示简化问题后重试
  - 影响区域：错误消息卡

## 6. Risks And Open Questions
- 风险：chunk 粒度不稳定会直接影响引用准确性和拒答阈值效果。
- 风险：SSE 中断时前后端完成态可能不一致，需要消息状态机兜底。
- 风险：摘要和推荐问题异步生成失败会导致欢迎态不完整。
- 待确认：低相关阈值的具体默认值。
- 待确认：反馈是否需要记录引用编号快照以便后续分析。

## 7. Writing Outline
- `backend/api-design.md`
  - 问答流式接口、摘要推荐查询、反馈提交
- `backend/database-design.md`
  - 会话、消息、引用快照、摘要、推荐、反馈
- `backend/middleware-design.md`
  - SSE 事件流、异步摘要任务、失败与重试
- `frontend/page-design.md`
  - 仅描述对话区和欢迎态，不替代 `chatfile-web` 全页骨架
- `frontend/component-design.md`
  - 消息气泡、引用块、反馈面板、推荐问题组件

## 8. Coverage Checklist
- Top-5 检索与低相关拒答已进入 API/中间件设计
- 最近 10 轮会话窗口已进入 API/DB 设计
- stop 生成、SSE 状态事件、完成态引用已进入 API/前端设计
- 摘要与推荐问题生成已进入中间件和前端设计
- 引用 hover、点击跳转事件、无结果态差异已进入前端设计
- 反馈标签、复制纯文本、错误重试和 30 秒禁用已进入前后端设计

## 9. Writer Handoff
- 推荐写作顺序：
  1. `backend/database-design.md`
  2. `backend/api-design.md`
  3. `backend/middleware-design.md`
  4. `frontend/page-design.md`
  5. `frontend/component-design.md`
- writer_must_cover:
  - `doc_id` 隔离检索
  - SSE 阶段事件与 stop
  - 引用锚点、引用列表、无结果态
  - 10 轮历史窗口
  - 摘要、推荐问题、反馈
- writer_must_not_assume:
  - 不要新增 Rerank、Agent、多文档联查
  - 不要替代 `chatfile-web` 重新定义完整页面骨架
- writer_open_questions:
  - 低相关阈值默认值
  - 反馈分析是否需要引用快照
- page_owner_module: `chatfile-web`
- cross_module_frontend_experience_dependencies:
  - `chatfile-web` 承接完整页面骨架、输入区、PDF 预览区
  - `conversation-orchestrator` 承接消息区、欢迎态、反馈和引用联动的数据与交互结果
- writer_referenced_inputs:
  - `docs/01-prd/PRD.md`
  - `docs/01-prd/research.md`
  - `docs/01-prd/ChatFile_interactive.md`
  - `docs/02-architecture/architecture-design.md`
- writer_planning_artifacts_to_hide:
  - `Decision ID`
  - `Source Section`
  - `Requirement ID`
- writer_final_interaction_coverage_shape:
  - 以“场景/触发条件/状态变化/反馈与时序”展示消息和欢迎态交互
- writer_layout_fidelity_requirements:
  - 仅保留对话区和欢迎态的局部骨架，不得取代整页 40/60 分栏骨架

