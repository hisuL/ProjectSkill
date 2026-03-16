---
version: 1.0.0
status: draft
module: conversation-orchestrator
role: backend
dependencies:
  - document-ingestion
  - chatfile-web
change_log:
  - version: 1.0.0
    date: 2026-03-16
    changes: initial version
---

# API Design

## 1. Referenced Inputs / 引用输入材料
- `docs/01-prd/PRD.md`:
  - 定义 Top-5 检索、低相关拒答、引用锚点、多轮历史和反馈。
- `docs/01-prd/ChatFile_interactive.md`:
  - 定义流式时序、stop、复制、反馈和错误交互。
- `docs/01-prd/research.md`:
  - 提供 Haystack 和 LLM 接入方式。
- `docs/02-architecture/architecture-design.md`:
  - 固化本模块对 `document-ingestion` 和前端的输出契约。

## 2. Scope / 范围
- 提供问答流式接口、摘要推荐查询和反馈提交。
- 不覆盖 PDF 上传、状态查询和预览元数据。

## 3. Inputs And Constraints / 输入与约束
- 所有问答请求必须携带 `docId`，后端强制按 `docId` 过滤检索。
- 检索默认 Top-5，低于阈值返回拒答消息，不允许自由发挥。
- 会话窗口只保留最近 10 轮。
- 流式协议必须区分检索阶段、生成阶段、token 片段、完成态、异常态和中断态。
- 无结果消息不返回引用列表和复制内容。
- 服务异常需返回 `requestId`，供前端展示和重试。

## 4. API Summary / API 概览
| API | Method / 方法 | Path / 路径 | Auth / 鉴权 | Description / 描述 |
| --- | --- | --- | --- | --- |
| 流式问答 | `POST` | `/api/conversations/query:stream` | none | 按 `docId` 检索并流式返回回答 |
| 查询欢迎态 | `GET` | `/api/conversations/{docId}/welcome` | none | 获取摘要与推荐问题 |
| 提交反馈 | `POST` | `/api/messages/{messageId}/feedback` | none | 提交点赞点踩与标签 |
| 查询历史 | `GET` | `/api/conversations/{docId}/messages` | none | 获取最近 10 轮及折叠摘要 |

## 5. Detailed Endpoints / 详细接口设计
### 5.1 Stream Query
- Method / Path / 方法与路径:
  - `POST /api/conversations/query:stream`
- Purpose / 目的:
  - 完成单文档问答、引用装配和流式输出。
- Request / 请求:
  - JSON:
    - `docId`
    - `message`
    - `recentMessages`（客户端当前窗口内历史）
    - `clientMessageId`
- Response / 响应:
  - `text/event-stream`
  - 事件类型：
    - `status.retrieving`
    - `status.generating`
    - `message.delta`
    - `message.citation.placeholder`
    - `message.completed`
    - `message.interrupted`
    - `message.failed`
- Error codes / 错误码:
  - `404 DOCUMENT_NOT_READY`
  - `409 DOCUMENT_PROCESSING`
  - `422 EMPTY_QUERY`
  - `503 GENERATION_UNAVAILABLE`
- Business logic / 业务逻辑:
  - 验证文档状态为 `ready`
  - 读取最近 10 轮历史
  - 按 `docId` 检索 Top-5 chunk
  - 阈值不达标时直接输出拒答完成态
  - 生成阶段输出 token 流，完成后追加引用列表
- Edge cases / 边界场景:
  - stop 时输出 `message.interrupted`
  - SSE 断连时保留部分文本和消息状态

### 5.2 Get Welcome Payload
- Method / Path / 方法与路径:
  - `GET /api/conversations/{docId}/welcome`
- Purpose / 目的:
  - 返回欢迎态摘要和 3 条推荐问题。
- Response / 响应:
  - `200 OK`
  - `summary`
  - `suggestedQuestions`
  - `status=ready|pending|failed`

### 5.3 Submit Feedback
- Method / Path / 方法与路径:
  - `POST /api/messages/{messageId}/feedback`
- Request / 请求:
  - `reaction=up|down`
  - `labels[]`
  - `comment`
- Constraints / 约束:
  - 同一消息只保留一条最终反馈记录，重复提交视为覆盖。
- Error codes / 错误码:
  - `409 FEEDBACK_ALREADY_FINALIZED` 不启用；首版允许覆盖切换

### 5.4 Get Conversation Messages
- Method / Path / 方法与路径:
  - `GET /api/conversations/{docId}/messages`
- Purpose / 目的:
  - 获取最近 10 轮消息和折叠历史计数。

## 6. Failure Handling / 失败处理
- 参数校验失败：
  - 空字符串、纯空白、超过 2000 字前端拦截，后端继续兜底返回 `422`。
- 依赖服务超时：
  - 30 秒内无有效响应则返回 `message.failed`，错误码 `REQUEST_TIMEOUT`。
- 重复提交：
  - 通过 `clientMessageId` 幂等去重，避免前端重试产生重复消息。

## 7. Open Questions / 待确认问题
- SSE 的 token 事件是否需要携带服务端累计字符数。
- 低相关阈值最终取值和灰度调整方式。

