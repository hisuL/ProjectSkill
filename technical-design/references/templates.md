# Technical Design Templates

按需读取本文件，为 `technical-design` skill 生成技术设计文档时提供章节骨架。不要机械照抄，应该根据模块实际情况删减。

## Backend API Template

````markdown
---
version: 1.0.0
status: draft
module: user-domain
role: backend
dependencies:
  - notification-domain
change_log:
  - version: 1.0.0
    date: YYYY-MM-DD
    changes: initial version
---

# API Design

## 1. Scope
- 目标
- 不在范围内的内容

## 2. Inputs And Constraints
- 来自 PRD 的约束
- 来自 architecture-design 的边界
- 依赖模块与前置条件

## 3. API Summary
| API | Method | Path | Auth | Description |
| --- | --- | --- | --- | --- |

## 4. Detailed Endpoints
### 4.1 Create XXX
- Method / Path:
- Purpose:
- Request:
- Response:
- Error codes:
- Idempotency:
- Business logic:
  1. ...
  2. ...
- Edge cases:
- Dependencies:

## 5. Data Dictionary
- 枚举
- 状态机
- 错误码

## 6. Failure Handling
- 参数校验失败
- 依赖服务超时
- 重复提交

## 7. Open Questions
- 待确认项
````

## Backend Database Template

````markdown
---
version: 1.0.0
status: draft
module: user-domain
role: backend
dependencies: []
change_log:
  - version: 1.0.0
    date: YYYY-MM-DD
    changes: initial version
---

# Database Design

## 1. Scope
- 本文覆盖的实体和存储职责

## 2. Entity Overview
| Entity | Purpose | Owner | Notes |
| --- | --- | --- | --- |

## 3. Schema Design
### 3.1 `users`
| Field | Type | Nullable | Default | Description |
| --- | --- | --- | --- | --- |

- Primary key:
- Unique constraints:
- Indexes:
- Write path:
- Read path:

## 4. Relationships
- Mermaid ER diagram:
  - `USERS ||--o{ USER_SESSIONS : has`

## 5. State And Consistency
- 核心状态流转
- 事务边界
- 最终一致性点

## 6. Migration And Backfill
- 建表 / 加字段 / 回填方案

## 7. Risks And Trade-offs
- 热点
- 膨胀
- 查询复杂度
````

## Backend Middleware Template

````markdown
---
version: 1.0.0
status: draft
module: user-domain
role: backend
dependencies:
  - audit-domain
change_log:
  - version: 1.0.0
    date: YYYY-MM-DD
    changes: initial version
---

# Middleware Design

## 1. Scope
- 涉及的中间件能力

## 2. Middleware Summary
| Type | Resource | Purpose | Producer | Consumer |
| --- | --- | --- | --- | --- |

## 3. Event / Cache / Search Detail
### 3.1 `user.created`
- Trigger:
- Payload:
- Ordering:
- Retry:
- Dead letter:
- Idempotency:
- Monitoring:

## 4. Operational Rules
- TTL
- Key convention
- Topic naming
- Alert thresholds

## 5. Failure Handling
- 消息堆积
- 缓存击穿
- 重复消费

## 6. Open Questions
- 待确认项
````

## Frontend Page Template

````markdown
---
version: 1.0.0
status: draft
module: user-domain
role: frontend
dependencies:
  - user-domain
change_log:
  - version: 1.0.0
    date: YYYY-MM-DD
    changes: initial version
---

# Page Design

## 1. Scope
- 页面目标
- 角色与权限

## 2. Routes
| Route | Entry | Permission | Description |
| --- | --- | --- | --- |

## 3. Layout And Regions
- 页面区域
- 信息层级
- 首屏内容

## 4. User Flow
- Mermaid flow suggestion:
  - `A[Open Page] --> B[Load Data]`
  - `B --> C[Render Main State]`

## 5. API Interaction
| Stage | API | Trigger | Failure Handling |
| --- | --- | --- | --- |

## 6. States
- loading
- empty
- error
- success

## 7. Telemetry And Guardrails
- 埋点
- 权限兜底
- 降级策略
````

## Frontend Component Template

````markdown
---
version: 1.0.0
status: draft
module: user-domain
role: frontend
dependencies:
  - design-system
change_log:
  - version: 1.0.0
    date: YYYY-MM-DD
    changes: initial version
---

# Component Design

## 1. Component Map
| Component | Responsibility | Parent | Depends On |
| --- | --- | --- | --- |

## 2. Detailed Components
### 2.1 `UserProfileForm`
- Purpose:
- Props:
- Local state:
- Derived state:
- Events:
- Validation:
- Error feedback:

## 3. State Management Strategy
- 本地状态
- 全局状态
- 服务端状态

## 4. Interaction Patterns
- optimistic update / rollback
- debounce / throttle
- modal / drawer coordination

## 5. Accessibility And Edge Cases
- 键盘操作
- 异常输入
- 超长文本

## 6. Open Questions
- 待确认项
````
