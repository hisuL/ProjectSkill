# Technical Design Writer Templates

按需读取本文件，为 `technical-design-writer` 生成正式技术设计文档时提供章节骨架。应优先遵循 planner 文档中的决策和覆盖要求。

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
- plan references:
- architecture handoff references:

## 2. Inputs And Constraints
- 来自 planner 的约束
- 来自 planner 的决策点
- 来自 architecture handoff 的边界和依赖
- 依赖模块与前置条件

## 3. API Summary
| API | Method | Path | Auth | Description | Plan Ref | Architecture Ref |
| --- | --- | --- | --- | --- | --- | --- |

## 4. Detailed Endpoints
### 4.1 Create XXX
- Plan refs:
- Architecture refs:
- Method / Path:
- Purpose:
- Request:
- Response:
- Error codes:
- Idempotency:
- Business logic:
- Edge cases:
- Dependencies:

## 5. Failure Handling
- 参数校验失败
- 依赖服务超时
- 重复提交

## 6. Open Questions
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
- plan references:
- architecture handoff references:

## 2. Entity Overview
| Entity | Purpose | Owner | Notes | Plan Ref | Architecture Ref |
| --- | --- | --- | --- | --- | --- |

## 3. Schema Design
### 3.1 `users`
| Field | Type | Nullable | Default | Description |
| --- | --- | --- | --- | --- |

- Primary key:
- Unique constraints:
- Indexes:
- Write path:
- Read path:

## 4. State And Consistency
- 核心状态流转
- 事务边界
- 最终一致性点

## 5. Migration And Backfill
- 建表 / 加字段 / 回填方案

## 6. Risks And Trade-offs
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
- plan references:
- architecture handoff references:

## 2. Middleware Summary
| Type | Resource | Purpose | Producer | Consumer | Plan Ref | Architecture Ref |
| --- | --- | --- | --- | --- | --- | --- |

## 3. Event / Cache / Search Detail
### 3.1 `user.created`
- Plan refs:
- Architecture refs:
- Trigger:
- Payload:
- Ordering:
- Retry:
- Dead letter:
- Idempotency:
- Monitoring:

## 4. Failure Handling
- 消息堆积
- 缓存击穿
- 重复消费

## 5. Open Questions
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
- 对应用户旅程
- plan references:
- architecture handoff references:
- frontend surfaces:

## 2. Routes
| Route | Entry | Permission | Description | Plan Ref | Architecture Ref |
| --- | --- | --- | --- | --- | --- |

## 3. Layout And Regions
- 页面区域
- 信息层级
- 首屏内容

## 4. User Flow
- 主流程
- 分支流程
- 失败回路
- architecture touchpoints:

## 5. API Interaction
| Stage | API | Trigger | Failure Handling | Plan Ref | Architecture Ref |
| --- | --- | --- | --- | --- | --- |

## 6. Interaction Requirements Mapping
| Requirement ID | Decision Ref | Architecture Ref | Scenario | Trigger | State Change | Feedback / Motion | Error / Edge Handling |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 7. States
- loading
- empty
- error
- success
- disabled
- permission denied

## 8. Telemetry And Guardrails
- 埋点
- 权限兜底
- 降级策略

## 9. Coverage Review
- [ ] planner 中的交互要求已覆盖
- [ ] planner 中的关键决策已映射
- [ ] architecture handoff 中的前端归属已映射
- [ ] architecture gaps 中禁止假设的点未被越权补写
- [ ] loading / empty / error / success 已覆盖
- [ ] 边界场景已覆盖
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
| Component | Responsibility | Parent | Depends On | Plan Ref | Architecture Ref |
| --- | --- | --- | --- | --- | --- |

## 2. Detailed Components
### 2.1 `UserProfileForm`
- Plan refs:
- Architecture refs:
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
| Requirement ID | Decision Ref | Architecture Ref | Pattern | Trigger | Component Behavior | Feedback / Motion | Rollback / Retry |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 5. Accessibility And Edge Cases
- 键盘操作
- 异常输入
- 超长文本

## 6. Open Questions
- 待确认项

## 7. Coverage Review
- [ ] planner 中的交互要求已覆盖
- [ ] planner 中的关键决策已映射
- [ ] architecture handoff 中的前端归属已映射
- [ ] architecture gaps 中禁止假设的点未被越权补写
- [ ] loading / empty / error / success 已覆盖
- [ ] 边界场景已覆盖
````
