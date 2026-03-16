---
version: 1.0.0
status: draft
module: document-ingestion
role: backend
dependencies:
  - chatfile-worker
change_log:
  - version: 1.0.0
    date: 2026-03-16
    changes: initial version
---

# Middleware Design

## 1. Referenced Inputs / 引用输入材料
- `docs/01-prd/PRD.md`:
  - 要求 5 分钟超时、解析失败可见、ready 前输入框禁用。
- `docs/01-prd/research.md`:
  - 定义解析、切片和 embedding 处理链路。
- `docs/02-architecture/architecture-design.md`:
  - 固化 `chatfile-worker` 异步执行边界。

## 2. Scope / 范围
- 设计文档处理异步任务、阶段事件、超时、取消、重试和监控。

## 3. Middleware Summary / 中间件概览
| Type / 类型 | Resource / 资源 | Purpose / 目的 | Producer / 生产方 | Consumer / 消费方 |
| --- | --- | --- | --- | --- |
| 任务事件 | `document.process.requested` | 触发解析流水线 | chatfile-app | chatfile-worker |
| 阶段事件 | `document.stage.changed` | 同步阶段推进 | chatfile-worker | chatfile-app |
| 超时扫描 | `document.timeout.check` | 兜底将超时任务置失败 | scheduler | chatfile-worker |

## 4. Event / Cache / Search Detail / 事件、缓存与搜索设计
### 4.1 `document.process.requested`
- Trigger / 触发条件:
  - 上传接口成功创建文档后。
- Payload / 载荷:
  - `docId`
  - `storageKey`
  - `fileName`
  - `requestedAt`
- Ordering / 顺序性:
  - 同一 `docId` 保证单消费者串行。
- Retry / 重试:
  - 最多 2 次，超过后转人工检查。
- Dead letter / 死信处理:
  - 记录 `failed` 并写 `failure_code=PIPELINE_DISPATCH_FAILED`
- Idempotency / 幂等性:
  - worker 以 `docId + stage` 判断是否已完成。
- Monitoring / 监控:
  - 任务入队、开始、完成、失败、超时计数。

### 4.2 `document.stage.changed`
- Trigger / 触发条件:
  - 每个阶段开始和结束时。
- Payload / 载荷:
  - `docId`
  - `stage`
  - `status`
  - `elapsedMs`
  - `chunkCount`
  - `failureCode`
- 用途:
  - 刷新状态查询结果，支持前端步骤条。

### 4.3 超时与取消控制
- 单文档总处理超时 `5 分钟`。
- 每次阶段切换前检查：
  - 是否已 `cancel_requested_at`
  - 是否超出 `deadline_at`
- 取消后动作：
  - 停止后续阶段
  - 删除未完成的 `document_processing_jobs`
  - 删除半成品 `document_chunks`

## 5. Failure Handling / 失败处理
- 消息堆积：
  - 若排队时长接近超时阈值，任务直接标记 `failed`，避免无意义执行。
- 解析器异常：
  - 分类成 `ENCRYPTED_PDF`、`SCANNED_PDF`、`PARSE_TIMEOUT`、`PARSE_FAILED`。
- embedding 失败：
  - 可重试一次；重试后仍失败则整文档失败。
- 重复消费：
  - 以 `document_processing_jobs.status` 和 `documents.status` 做幂等检查。

## 6. Open Questions / 待确认问题
- 任务队列具体实现是否沿用轻量内置方案还是直接接入成熟队列。
- `estimatedRemainingMs` 是否由 middleware 侧产生经验值。

