---
version: 1.0.0
status: draft
module: document-ingestion
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
  - 定义文档状态、chunk 元数据和超时要求。
- `docs/01-prd/research.md`:
  - 定义 PostgreSQL + pgvector、标题优先切片。
- `docs/02-architecture/architecture-design.md`:
  - 规定原始 PDF、解析产物、chunk 和 embeddings 归属本模块。

## 2. Scope / 范围
- 覆盖文档主记录、解析产物、chunk、处理任务四类实体。

## 3. Entity Overview / 实体概览
| Entity / 实体 | Purpose / 目的 | Owner / 归属方 | Notes / 备注 |
| --- | --- | --- | --- |
| `documents` | 文档主记录与状态汇总 | document-ingestion | 主键来源于上传入口 |
| `document_artifacts` | 解析 Markdown、图片清单、目录摘要 | document-ingestion | 文件落对象存储，表里存引用 |
| `document_chunks` | 可检索 chunk 及元数据 | document-ingestion | 支撑问答检索和引用 |
| `document_processing_jobs` | 阶段任务与超时、取消控制 | document-ingestion | 支撑 worker 幂等 |

## 4. Schema Design / 结构设计
### 4.1 `documents`
| Field / 字段 | Type / 类型 | Nullable / 可空 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | no |  | 文档 ID |
| `file_name` | `text` | no |  | 原始文件名 |
| `file_size_bytes` | `bigint` | no |  | 文件大小 |
| `file_sha256` | `char(64)` | no |  | 文件内容哈希 |
| `status` | `text` | no | `uploaded` | 文档阶段状态 |
| `current_stage` | `text` | yes |  | 当前处理阶段 |
| `page_count` | `integer` | yes |  | 页数 |
| `chunk_count` | `integer` | yes | 0 | 切片数 |
| `storage_key` | `text` | no |  | 原始 PDF 对象键 |
| `preview_url_ttl_sec` | `integer` | no | 900 | 预览签名有效期 |
| `failure_code` | `text` | yes |  | 失败码 |
| `failure_message` | `text` | yes |  | 面向前端的失败摘要 |
| `cancel_requested_at` | `timestamptz` | yes |  | 取消请求时间 |
| `processing_started_at` | `timestamptz` | yes |  | 开始处理时间 |
| `ready_at` | `timestamptz` | yes |  | 完成时间 |
| `created_at` | `timestamptz` | no | `now()` | 创建时间 |
| `updated_at` | `timestamptz` | no | `now()` | 更新时间 |

- Primary key / 主键:
  - `id`
- Unique constraints / 唯一约束:
  - `file_sha256`
- Indexes / 索引:
  - `idx_documents_status_created_at(status, created_at desc)`
- Write path / 写入路径:
  - 上传入口、worker 状态推进、取消接口
- Read path / 读取路径:
  - 状态查询、预览查询

### 4.2 `document_artifacts`
| Field / 字段 | Type / 类型 | Nullable / 可空 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | no |  | 主键 |
| `document_id` | `uuid` | no |  | 所属文档 |
| `markdown_storage_key` | `text` | yes |  | 解析 Markdown 对象键 |
| `images_manifest` | `jsonb` | yes |  | 图片占位与对象键列表 |
| `toc` | `jsonb` | yes |  | 目录树 |
| `parser_name` | `text` | no |  | 解析器名称 |
| `parser_version` | `text` | no |  | 解析器版本 |
| `created_at` | `timestamptz` | no | `now()` | 创建时间 |

- Indexes / 索引:
  - `idx_document_artifacts_document_id(document_id)`

### 4.3 `document_chunks`
| Field / 字段 | Type / 类型 | Nullable / 可空 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | no |  | chunk 主键 |
| `document_id` | `uuid` | no |  | 所属文档 |
| `chunk_id` | `text` | no |  | 业务稳定 ID |
| `sequence_no` | `integer` | no |  | 文档内顺序 |
| `page_start` | `integer` | no |  | 起始页 |
| `page_end` | `integer` | no |  | 结束页 |
| `title_path` | `text[]` | no |  | 标题路径 |
| `content_markdown` | `text` | no |  | chunk 文本 |
| `locator_payload` | `jsonb` | yes |  | 高亮定位信息 |
| `token_count` | `integer` | no |  | chunk token 数 |
| `embedding` | `vector` | yes |  | pgvector 向量 |
| `created_at` | `timestamptz` | no | `now()` | 创建时间 |

- Unique constraints / 唯一约束:
  - `(document_id, chunk_id)`
- Indexes / 索引:
  - `idx_chunks_document_sequence(document_id, sequence_no)`
  - `idx_chunks_document_page(document_id, page_start)`
  - `ivfflat_chunks_embedding` on `embedding`
- Write path / 写入路径:
  - worker 切片和 embedding 阶段
- Read path / 读取路径:
  - conversation 检索、引用跳转

### 4.4 `document_processing_jobs`
| Field / 字段 | Type / 类型 | Nullable / 可空 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | no |  | 任务 ID |
| `document_id` | `uuid` | no |  | 文档 ID |
| `stage` | `text` | no |  | `parsing/chunking/indexing` |
| `status` | `text` | no | `queued` | `queued/running/succeeded/failed/cancelled` |
| `attempt` | `integer` | no | 1 | 重试次数 |
| `deadline_at` | `timestamptz` | no |  | 阶段超时截止 |
| `error_payload` | `jsonb` | yes |  | 错误详情 |
| `started_at` | `timestamptz` | yes |  | 开始时间 |
| `finished_at` | `timestamptz` | yes |  | 结束时间 |

## 5. State And Consistency / 状态与一致性
- 核心状态流转：
  - `uploaded -> parsing -> chunking -> indexing -> ready`
  - 任一阶段异常或超时转 `failed`
  - 用户取消转 `cancelled`
- 事务边界：
  - 上传入口中，对象存储写入和 `documents` 创建需具备补偿逻辑。
  - 切片写入和 `chunk_count` 更新在同一事务内提交。
- 最终一致性点：
  - `document_chunks.embedding` 允许晚于 chunk 文本写入，但 `documents.status=ready` 前必须全部完成。

## 6. Migration And Backfill / 迁移与回填
- 首版直接建表，无历史回填。
- 若后续增加 `locator_payload` 精度字段，采用增量字段迁移，不回写历史 chunk 坐标。

## 7. Risks And Trade-offs / 风险与权衡
- `file_sha256` 去重会让同内容不同文件名复用文档，需要确认是否允许。
- `embedding` 与业务表同库存储简化部署，但会增加单库负载。
- `locator_payload` 首版保留可空，接受页级定位优于精确坐标缺失。

