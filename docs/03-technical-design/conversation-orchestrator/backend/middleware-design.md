---
version: 1.0.0
status: draft
module: conversation-orchestrator
role: backend
dependencies:
  - litellm
  - document-ingestion
change_log:
  - version: 1.0.0
    date: 2026-03-16
    changes: initial version
---

# Middleware Design

## 1. Referenced Inputs / 引用输入材料
- `docs/01-prd/PRD.md`:
  - 要求流式输出、低相关拒答、多轮历史和摘要推荐。
- `docs/01-prd/ChatFile_interactive.md`:
  - 定义 stop、错误重试、超时和欢迎态体验。
- `docs/02-architecture/architecture-design.md`:
  - 固化本模块同步流式与异步摘要的边界。

## 2. Scope / 范围
- 设计 SSE 事件流、摘要推荐异步任务、异常熔断和监控。

## 3. Middleware Summary / 中间件概览
| Type / 类型 | Resource / 资源 | Purpose / 目的 | Producer / 生产方 | Consumer / 消费方 |
| --- | --- | --- | --- | --- |
| SSE 事件流 | `conversation.stream` | 向前端推送检索、生成和完成事件 | conversation-orchestrator | chatfile-web |
| 异步任务 | `welcome.generate.requested` | 生成摘要和推荐问题 | document ready hook | worker |
| 熔断计数 | `conversation.failure.counter` | 连续失败 3 次后禁用输入区 30 秒 | conversation-orchestrator | chatfile-web |

## 4. Event / Cache / Search Detail / 事件、缓存与搜索设计
### 4.1 `conversation.stream`
- Trigger / 触发条件:
  - 用户发送消息。
- Payload / 载荷:
  - 阶段事件：`retrieving/generating`
  - token 事件：增量文本
  - 完成事件：最终正文、引用列表、消息 ID
  - 中断事件：已输出正文、`interrupted=true`
  - 失败事件：错误码、`requestId`
- Ordering / 顺序性:
  - 同一消息严格单流顺序。
- Retry / 重试:
  - SSE 不自动重放；前端走“重新生成”或“重试”。
- Monitoring / 监控:
  - 首 token 延迟、完成耗时、中断率、拒答率、错误率。

### 4.2 `welcome.generate.requested`
- Trigger / 触发条件:
  - 文档从 `indexing` 成功进入 `ready`。
- Payload / 载荷:
  - `docId`
  - `topChunks`
  - `pageCount`
- Processing / 处理:
  - 生成 `<= 200 字` 摘要和 `3` 条推荐问题。
  - 失败时仅标记 `document_welcome_payloads.status=failed`，不影响问答。

### 4.3 失败计数与输入禁用
- 后端在响应中返回 `temporaryInputDisabledUntil`。
- 连续 `3` 次 `503/timeout/network_interrupted` 后给出 `30s` 禁用窗口。

## 5. Failure Handling / 失败处理
- 消息堆积：
  - 单文档并发问答超限时直接返回 `429 TOO_MANY_ACTIVE_STREAMS`。
- 模型失败：
  - 返回 `message.failed` 和请求 ID，不降级为无引用自由回答。
- 检索低相关：
  - 直接生成拒答完成态，跳过 LLM。
- 重复消费：
  - 同一 `clientMessageId` 重试复用已有消息记录。

## 6. Open Questions / 待确认问题
- `temporaryInputDisabledUntil` 是否完全由后端统一计算。
- 摘要和推荐问题是否需要定时刷新以适配模型升级。

