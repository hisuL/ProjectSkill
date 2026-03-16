---
version: 1.0.0
status: draft
module: document-ingestion
role: backend
change_log:
  - version: 1.0.0
    date: 2026-03-16
    changes: initial version
---

# Design Plan

## 1. Module Scope And Role
- `module_id`: `document-ingestion`
- `role`: `backend`
- 目标：完成单 PDF 上传、持久化、解析、切片、向量化、状态推进与失败处理。
- 范围内：
  - 文件校验与上传入口
  - 文档状态机与超时控制
  - Markdown 解析产物、chunk 元数据、embedding 写入
  - 给问答模块提供 `doc_id` 范围内可检索数据
- 不在范围内：
  - 多文档管理
  - OCR
  - Rerank、ES、权限体系
  - 前端页面布局与视觉呈现

## 2. Referenced Inputs
- `docs/01-prd/PRD.md`
  - 定义单文件、100MB、5 分钟处理上限、解析状态流转和 chunk 元数据要求。
- `docs/01-prd/research.md`
  - 提供 FastAPI、Haystack、SeaweedFS、PostgreSQL/pgvector、标题优先切片方案。
- `docs/01-prd/ChatFile_interactive.md`
  - 约束上传空态、进度、取消、失败原因和 ready 横幅所需的后端状态语义。
- `docs/02-architecture/architecture-design.md`
  - 固化模块边界、数据归属、交接卡、异步 worker 责任和 `document-ingestion` 输出契约。

## 3. Constraints Summary
- 仅支持单个文本型 PDF，文件大小 `<= 100MB`。
- 文档处理链路总时长上限 `5 分钟`，超时必须进入 `failed`。
- 切片策略先按 Markdown 标题层级，再回退到 `512 tokens + 50 tokens overlap`。
- 每个 chunk 必须保存 `chunk_id`、`doc_id`、`page_num`、`title_path`、文本内容和定位元数据。
- 向量检索严格依赖 `doc_id` 过滤，因此 ingestion 侧必须保证文档隔离主键稳定。
- 上传、解析、切片、向量化需要可查询的阶段状态，供前端展示步骤条和 ready 横幅。
- 首版引用定位以页码和 chunk 锚点为主，不承诺完美段落级坐标。

## 4. Decision Log
| Decision | Final Direction | Rationale |
| --- | --- | --- |
| 服务形态 | `chatfile-app` 提供同步 API，`chatfile-worker` 执行异步处理 | 满足上传快响应和处理链路解耦 |
| 原始文件存储 | 原始 PDF 与解析副产物放 `SeaweedFS` | 与架构选型一致，S3 协议易替换 |
| 主数据存储 | 文档状态、chunk、embedding 全部落 `PostgreSQL + pgvector` | MVP 降低运维复杂度 |
| 状态机 | `uploaded -> parsing -> chunking -> indexing -> ready/failed/cancelled` | 对应 PRD 和交互稿步骤条 |
| 取消策略 | 仅允许 `uploaded/parsing/chunking/indexing` 期间取消，取消后状态置 `cancelled`，清理未完成产物 | 满足上传取消和处理取消需求 |
| 失败摘要 | 持久化标准失败码和可展示文案 | 让前端可直接展示加密、超时、扫描件等错误 |
| PDF 预览元数据 | 上传成功后立即生成对象存储访问路径并返回 | 支撑“解析与预览并行” |

## 5. Backend Touchpoints To UI
- 本模块不拥有页面交互实现，但必须提供稳定状态支撑以下体验：
  - 上传进度百分比
  - 步骤条当前阶段与已完成步骤
  - 预计耗时文案所需的页数与阶段信息
  - 失败原因摘要
  - ready 横幅所需的页数、切片数、耗时
  - 取消上传/取消处理后的最终状态

## 6. Risks And Open Questions
- 风险：复杂表格和版式会导致 chunk 边界不稳，影响引用命中质量。
- 风险：单库承载关系数据和向量检索，需预留 `doc_id + embedding` 索引策略。
- 风险：取消处理中任务时，可能已有部分 chunk/embedding 落库，需要幂等清理。
- 待确认：是否首版提供解析后 Markdown 下载能力。
- 待确认：预估剩余时间采用静态经验值还是按页数动态估算。

## 7. Writing Outline
- `api-design.md`
  - 上传、状态查询、取消处理、预览元数据接口
- `database-design.md`
  - 文档、解析产物、chunk、处理任务表与状态一致性
- `middleware-design.md`
  - 异步任务、阶段事件、超时和重试策略

## 8. Coverage Checklist
- 文件类型和大小校验已落入 API 设计
- 上传到 ready 的完整状态机已落入 API/DB/中间件设计
- `5 分钟` 超时与失败码已落入中间件设计
- 标题优先 + token fallback 切片已落入中间件和数据设计
- `chunk_id/page_num/title_path` 已落入数据库设计
- 取消上传/取消处理已落入 API 和中间件设计
- 预览并行加载所需对象存储元数据已落入 API 设计

## 9. Writer Handoff
- 推荐写作顺序：
  1. `database-design.md`
  2. `middleware-design.md`
  3. `api-design.md`
- writer_must_cover:
  - 文档状态机与阶段推进
  - 文件校验、取消、失败摘要
  - chunk/embedding 结构与 `doc_id` 隔离
  - worker 超时、幂等和清理策略
- writer_must_not_assume:
  - 不要假设 OCR、Office 文档支持、ES、Rerank
  - 不要假设段落级高亮一定可精确定位
- writer_open_questions:
  - Markdown 下载能力
  - 预估耗时算法
- writer_referenced_inputs:
  - `docs/01-prd/PRD.md`
  - `docs/01-prd/research.md`
  - `docs/01-prd/ChatFile_interactive.md`
  - `docs/02-architecture/architecture-design.md`
- writer_planning_artifacts_to_hide:
  - `Decision ID`
  - `Plan Ref`
  - `Source Section`
- writer_final_interaction_coverage_shape:
  - 只保留对 UI 有影响的状态语义、错误文案来源和时序要求
- writer_layout_fidelity_requirements:
  - 无完整页面骨架要求，本模块仅需保证状态字段能支撑上传区和 ready 横幅

