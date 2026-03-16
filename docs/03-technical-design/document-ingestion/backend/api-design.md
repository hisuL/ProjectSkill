---
version: 1.0.0
status: draft
module: document-ingestion
role: backend
dependencies:
  - chatfile-web
  - conversation-orchestrator
change_log:
  - version: 1.0.0
    date: 2026-03-16
    changes: initial version
---

# API Design

## 1. Referenced Inputs / 引用输入材料
- `docs/01-prd/PRD.md`:
  - 定义文件大小、处理上限、chunk 元数据和上传状态语义。
- `docs/01-prd/ChatFile_interactive.md`:
  - 约束上传进度、步骤条、ready 横幅和失败提示所需接口字段。
- `docs/01-prd/research.md`:
  - 约束对象存储、Haystack 和标题优先切片。
- `docs/02-architecture/architecture-design.md`:
  - 固化同步 API 与异步 worker 分工。

## 2. Scope / 范围
- 提供上传、状态查询、取消处理和预览元数据接口。
- 不覆盖问答、摘要、推荐问题和反馈。

## 3. Inputs And Constraints / 输入与约束
- 单次只允许上传一个 PDF，`Content-Type` 和扩展名都必须校验。
- 文件大小上限 `100MB`，超限直接拒绝。
- 上传成功后立即创建文档记录并触发异步处理。
- 处理阶段对外暴露统一状态：`uploaded`、`parsing`、`chunking`、`indexing`、`ready`、`failed`、`cancelled`。
- 所有状态查询都必须返回前端可直接展示的失败摘要、页数、切片数、总耗时和对象存储预览地址。

## 4. API Summary / API 概览
| API | Method / 方法 | Path / 路径 | Auth / 鉴权 | Description / 描述 |
| --- | --- | --- | --- | --- |
| 上传文档 | `POST` | `/api/documents` | none | 上传 PDF，创建文档记录并投递处理任务 |
| 查询状态 | `GET` | `/api/documents/{docId}` | none | 查询文档阶段状态、统计信息和预览元数据 |
| 取消处理 | `POST` | `/api/documents/{docId}:cancel` | none | 取消上传后处理中的文档 |
| 预览签名 | `GET` | `/api/documents/{docId}/preview` | none | 返回 PDF 预览地址和基础信息 |

## 5. Detailed Endpoints / 详细接口设计
### 5.1 Upload Document
- Method / Path / 方法与路径:
  - `POST /api/documents`
- Purpose / 目的:
  - 接收单个 PDF，保存原始文件，创建文档主记录和异步任务。
- Request / 请求:
  - `multipart/form-data`
  - 字段：
    - `file`: PDF 文件
    - `clientRequestId`: 可选，幂等辅助键
- Response / 响应:
  - `202 Accepted`
  - 返回：
    - `docId`
    - `status=uploaded`
    - `fileName`
    - `fileSize`
    - `previewUrl`
    - `createdAt`
- Error codes / 错误码:
  - `400 INVALID_FILE_TYPE`
  - `400 FILE_TOO_LARGE`
  - `409 DUPLICATE_UPLOAD`
  - `500 STORAGE_WRITE_FAILED`
- Idempotency / 幂等性:
  - `clientRequestId + file_hash` 去重，同一请求重放返回已有 `docId`。
- Business logic / 业务逻辑:
  - 校验类型和大小。
  - 先写对象存储，再创建数据库记录。
  - 记录 `status=uploaded` 并投递 `document.process.requested`。
- Edge cases / 边界场景:
  - 对象存储写入成功但数据库失败时，需要补偿删除对象。
- Dependencies / 依赖:
  - `SeaweedFS`
  - `chatfile-worker`

### 5.2 Get Document Status
- Method / Path / 方法与路径:
  - `GET /api/documents/{docId}`
- Purpose / 目的:
  - 给前端步骤条、ready 横幅和失败态提供统一状态查询。
- Response / 响应:
  - `200 OK`
  - 字段：
    - `docId`
    - `status`
    - `stageProgress`: `uploaded/parsing/chunking/indexing`
    - `pageCount`
    - `chunkCount`
    - `elapsedMs`
    - `estimatedRemainingMs`
    - `failureCode`
    - `failureMessage`
    - `previewUrl`
    - `previewStatus`
- Error codes / 错误码:
  - `404 DOCUMENT_NOT_FOUND`
- Business logic / 业务逻辑:
  - 只返回当前最新阶段和汇总统计，不暴露实现内部日志。

### 5.3 Cancel Document Processing
- Method / Path / 方法与路径:
  - `POST /api/documents/{docId}:cancel`
- Purpose / 目的:
  - 取消未完成的处理流程。
- Response / 响应:
  - `200 OK`
  - `status=cancelled`
- Error codes / 错误码:
  - `409 DOCUMENT_ALREADY_READY`
  - `409 DOCUMENT_ALREADY_FAILED`
- Idempotency / 幂等性:
  - 重复调用返回当前最终状态。
- Business logic / 业务逻辑:
  - 设置取消标记，worker 在阶段切换前检查并终止。
  - 清理未完成 chunk 和 embedding。

### 5.4 Get Preview Metadata
- Method / Path / 方法与路径:
  - `GET /api/documents/{docId}/preview`
- Purpose / 目的:
  - 返回 PDF 预览所需地址、页数和目录摘要。
- Response / 响应:
  - `200 OK`
  - 字段：
    - `previewUrl`
    - `pageCount`
    - `tableOfContents`（可为空）
- Edge cases / 边界场景:
  - 解析未完成时允许返回 `previewUrl`，但 `tableOfContents` 可为空。

## 6. Failure Handling / 失败处理
- 参数校验失败：
  - 统一映射成可展示错误码和文案，避免前端自行拼接。
- 依赖服务超时：
  - 对象存储或数据库超时直接失败，不创建半成品文档记录。
- 重复提交：
  - 通过 `clientRequestId + file_hash` 返回已有文档。
- 处理中取消：
  - 以数据库取消标记为准，worker 幂等停止并清理中间产物。

## 7. Open Questions / 待确认问题
- `estimatedRemainingMs` 是否按页数经验公式给出，还是首版固定文案。
- `tableOfContents` 是否由 ingestion 解析阶段统一生成。

