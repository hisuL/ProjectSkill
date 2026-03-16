---
version: 1.0.0
status: draft
module: conversation-orchestrator
role: backend
dependencies: []
change_log:
  - version: 1.0.0
    date: 2026-03-16
    changes: initial version
---

# Database Design

## 1. Referenced Inputs / 引用输入材料
- `docs/01-prd/PRD.md`:
  - 规定最近 10 轮、多轮追问、摘要推荐和反馈。
- `docs/01-prd/ChatFile_interactive.md`:
  - 规定中断态、无结果态、反馈面板和复制行为。
- `docs/02-architecture/architecture-design.md`:
  - 规定会话、反馈、摘要与推荐问题归属本模块。

## 2. Scope / 范围
- 覆盖会话、消息、引用快照、欢迎态和反馈记录。

## 3. Entity Overview / 实体概览
| Entity / 实体 | Purpose / 目的 | Owner / 归属方 | Notes / 备注 |
| --- | --- | --- | --- |
| `conversations` | 文档维度会话容器 | conversation-orchestrator | 单文档单会话工作台 |
| `messages` | 用户和 AI 消息 | conversation-orchestrator | 保存流式完成态 |
| `message_citations` | 引用列表快照 | conversation-orchestrator | 供 hover/跳转使用 |
| `document_welcome_payloads` | 摘要与推荐问题 | conversation-orchestrator | 可异步刷新 |
| `message_feedbacks` | 点赞点踩反馈 | conversation-orchestrator | 支持覆盖提交 |

## 4. Schema Design / 结构设计
### 4.1 `conversations`
| Field / 字段 | Type / 类型 | Nullable / 可空 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | no |  | 会话 ID |
| `document_id` | `uuid` | no |  | 关联文档 |
| `status` | `text` | no | `active` | 会话状态 |
| `history_turn_limit` | `integer` | no | 10 | 历史轮次窗口 |
| `created_at` | `timestamptz` | no | `now()` | 创建时间 |
| `updated_at` | `timestamptz` | no | `now()` | 更新时间 |

### 4.2 `messages`
| Field / 字段 | Type / 类型 | Nullable / 可空 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | no |  | 消息 ID |
| `conversation_id` | `uuid` | no |  | 所属会话 |
| `client_message_id` | `text` | yes |  | 客户端幂等键 |
| `role` | `text` | no |  | `user/assistant/system` |
| `status` | `text` | no | `completed` | `streaming/completed/interrupted/failed` |
| `content_markdown` | `text` | no |  | 消息正文 |
| `is_refusal` | `boolean` | no | `false` | 是否低相关拒答 |
| `request_id` | `text` | yes |  | 异常追踪 ID |
| `created_at` | `timestamptz` | no | `now()` | 创建时间 |

### 4.3 `message_citations`
| Field / 字段 | Type / 类型 | Nullable / 可空 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | no |  | 主键 |
| `message_id` | `uuid` | no |  | AI 消息 ID |
| `citation_no` | `integer` | no |  | `[1]` 序号 |
| `document_chunk_id` | `uuid` | no |  | 来源 chunk |
| `page_start` | `integer` | no |  | 起始页 |
| `page_end` | `integer` | no |  | 结束页 |
| `title_path_text` | `text` | no |  | 章节路径 |
| `summary_excerpt` | `text` | no |  | hover 摘要 |
| `locator_payload` | `jsonb` | yes |  | 预览区定位快照 |

### 4.4 `document_welcome_payloads`
| Field / 字段 | Type / 类型 | Nullable / 可空 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- |
| `document_id` | `uuid` | no |  | 文档 ID |
| `summary` | `text` | yes |  | <= 200 字摘要 |
| `suggested_questions` | `jsonb` | yes |  | 长度固定 3 |
| `status` | `text` | no | `pending` | `pending/ready/failed` |
| `generated_at` | `timestamptz` | yes |  | 生成时间 |

### 4.5 `message_feedbacks`
| Field / 字段 | Type / 类型 | Nullable / 可空 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- |
| `message_id` | `uuid` | no |  | 消息 ID |
| `reaction` | `text` | no |  | `up/down` |
| `labels` | `text[]` | yes |  | 负反馈标签 |
| `comment` | `text` | yes |  | 最多 200 字 |
| `updated_at` | `timestamptz` | no | `now()` | 更新时间 |

## 5. State And Consistency / 状态与一致性
- 核心状态流转：
  - `messages.status`: `streaming -> completed/interrupted/failed`
  - `document_welcome_payloads.status`: `pending -> ready/failed`
- 事务边界：
  - AI 消息正文和引用快照在完成态同一事务提交。
- 最终一致性点：
  - SSE 流中的 token 不逐条持久化，只在周期性 checkpoint 或完成态落库。

## 6. Migration And Backfill / 迁移与回填
- 首版无历史数据，直接建表。
- 若后续增加反馈分析字段，采用追加列，不回写旧反馈。

## 7. Risks And Trade-offs / 风险与权衡
- 流式过程中只在完成态持久化，断连时需依赖中断兜底保存。
- `message_citations` 保存快照会增加存储，但能保证引用回放稳定。

