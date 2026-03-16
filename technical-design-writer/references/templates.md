# Technical Design Writer Templates

按需读取本文件，为 `technical-design-writer` 生成正式技术设计文档时提供章节骨架。应优先遵循 planner 文档中的决策和覆盖要求。

总原则：
- 最终文档展示“最终结果”，不展示 planner 的过程痕迹
- 但 planner 已经收敛出的结论、默认值、限制、交互效果，必须直接转写进正文
- 删除的是 `Plan Ref`、`Decision ID`、`Source Section` 这类标签，不是这些标签背后的设计结论

术语说明：
- `Referenced Inputs`：引用输入材料，放在文档开头，列出参考文档及其影响
- `Scope`：本文范围，说明本文负责什么、不负责什么
- `Inputs And Constraints`：输入与约束，写清稳定边界、前置条件和设计限制
- `Interaction Coverage Checklist`：交互覆盖清单，用来确认最终交互效果是否都已写进正文
- `Open Questions`：待确认问题，不要伪造答案

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

## 1. Referenced Inputs
- `docs/...`:
  - why it matters

## 2. Scope
- 目标
- 不在范围内的内容

## 3. Inputs And Constraints
- 来自 planner 的约束
- 来自架构交接和引用文档的稳定边界
- 依赖模块与前置条件

要求：
- 这里直接写最终约束和最终决策结果
- 不要只写“见 planner”

## 4. API Summary
| API | Method | Path | Auth | Description |
| --- | --- | --- | --- | --- |

## 5. Detailed Endpoints
### 4.1 Create XXX
- Method / Path:
- Purpose:
- Request:
- Response:
- Error codes:
- Idempotency:
- Business logic:
- Edge cases:
- Dependencies:

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

## 1. Referenced Inputs
- `docs/...`:
  - why it matters

## 2. Scope
- 本文覆盖的实体和存储职责

## 3. Entity Overview
| Entity | Purpose | Owner | Notes |
| --- | --- | --- | --- |

## 4. Schema Design
### 3.1 `users`
| Field | Type | Nullable | Default | Description |
| --- | --- | --- | --- | --- |

- Primary key:
- Unique constraints:
- Indexes:
- Write path:
- Read path:

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

## 1. Referenced Inputs
- `docs/...`:
  - why it matters

## 2. Scope
- 涉及的中间件能力

## 3. Middleware Summary
| Type | Resource | Purpose | Producer | Consumer |
| --- | --- | --- | --- | --- |

## 4. Event / Cache / Search Detail
### 3.1 `user.created`
- Trigger:
- Payload:
- Ordering:
- Retry:
- Dead letter:
- Idempotency:
- Monitoring:

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

## 1. Referenced Inputs
- `docs/...`:
  - why it matters

## 2. Scope
- 页面目标
- 角色与权限
- 对应用户旅程
- frontend surfaces:

## 3. Routes
| Route | Entry | Permission | Description |
| --- | --- | --- | --- |

## 4. Layout And Regions
- 页面区域
- 信息层级
- 首屏内容

## 5. User Flow
- 主流程
- 分支流程
- 失败回路
- architecture touchpoints:

## 6. API Interaction
| Stage | API | Trigger | Failure Handling |
| --- | --- | --- | --- |

## 7. Interaction Design
| Scenario | Trigger | State Change | Feedback / Motion | Copy / Timing | Error / Edge Handling |
| --- | --- | --- | --- | --- | --- |

要求：
- 直接写最终交互效果
- 如果 planner 已经确定默认值、动画时长、自动消失时间、折叠条件，这里必须直接写出来
- 不要因为去掉追踪字段，就把这些结果删掉

## 8. States
- loading
- empty
- error
- success
- disabled
- permission denied

## 9. Telemetry And Guardrails
- 埋点
- 权限兜底
- 降级策略

## 10. Interaction Coverage Checklist
| Interaction Effect | Covered In | Notes |
| --- | --- | --- |

要求：
- 这一节直接写最终要实现的交互效果
- 不要写 `Source Section`、`Requirement ID`、`Plan Ref`
- 如果有未覆盖项，直接写缺口和原因
- 这里用于确认“最终效果是否写进正文”，不是只确认“引用过 planner”
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

## 1. Referenced Inputs
- `docs/...`:
  - why it matters

## 2. Component Map
| Component | Responsibility | Parent | Depends On |
| --- | --- | --- | --- |

## 3. Detailed Components
### 2.1 `UserProfileForm`
- Purpose:
- Props:
- Local state:
- Derived state:
- Events:
- Validation:
- Error feedback:

## 4. State Management Strategy
- 本地状态
- 全局状态
- 服务端状态

要求：
- 如果 planner 已经确定状态边界和默认行为，这里要直接写结果
- 不要只保留抽象分类而丢掉已确定的状态规则

## 5. Interaction Patterns
| Pattern | Trigger | Component Behavior | Feedback / Motion | Copy / Timing | Rollback / Retry |
| --- | --- | --- | --- | --- | --- |

要求：
- 直接写组件最终要实现的交互模式
- planner 已经确定的动效、toast、modal、自动收起、自动发送等结果必须保留
- 不能因为去掉追踪标签而把这些结果省略

## 6. Accessibility And Edge Cases
- 键盘操作
- 异常输入
- 超长文本

## 7. Open Questions
- 待确认项

## 8. Interaction Coverage Checklist
| Interaction Effect | Covered In | Notes |
| --- | --- | --- |

要求：
- 这一节直接写最终要实现的交互效果
- 不要写 `Source Section`、`Requirement ID`、`Plan Ref`
- 如果有未覆盖项，直接写缺口和原因
- 这里检查的是“效果本身是否已经进入最终文档”，不是 planner 是否存在对应字段
````
