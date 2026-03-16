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

## Backend API Template / 后端 API 模板

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

## 1. Referenced Inputs / 引用输入材料
- `docs/...`:
  - why it matters

## 2. Scope / 范围
- 目标
- 不在范围内的内容

## 3. Inputs And Constraints / 输入与约束
- 来自 planner 的约束
- 来自架构交接和引用文档的稳定边界
- 依赖模块与前置条件

要求：
- 这里直接写最终约束和最终决策结果
- 不要只写“见 planner”

## 4. API Summary / API 概览
| API | Method / 方法 | Path / 路径 | Auth / 鉴权 | Description / 描述 |
| --- | --- | --- | --- | --- |

## 5. Detailed Endpoints / 详细接口设计
### 4.1 Create XXX
- Method / Path / 方法与路径:
- Purpose / 目的:
- Request / 请求:
- Response / 响应:
- Error codes / 错误码:
- Idempotency / 幂等性:
- Business logic / 业务逻辑:
- Edge cases / 边界场景:
- Dependencies / 依赖:

## 6. Failure Handling / 失败处理
- 参数校验失败
- 依赖服务超时
- 重复提交

## 7. Open Questions / 待确认问题
- 待确认项
````

## Backend Database Template / 后端数据库模板

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

## 1. Referenced Inputs / 引用输入材料
- `docs/...`:
  - why it matters

## 2. Scope / 范围
- 本文覆盖的实体和存储职责

## 3. Entity Overview / 实体概览
| Entity / 实体 | Purpose / 目的 | Owner / 归属方 | Notes / 备注 |
| --- | --- | --- | --- |

## 4. Schema Design / 结构设计
### 3.1 `users`
| Field / 字段 | Type / 类型 | Nullable / 可空 | Default / 默认值 | Description / 描述 |
| --- | --- | --- | --- | --- |

- Primary key / 主键:
- Unique constraints / 唯一约束:
- Indexes / 索引:
- Write path / 写入路径:
- Read path / 读取路径:

## 5. State And Consistency / 状态与一致性
- 核心状态流转
- 事务边界
- 最终一致性点

## 6. Migration And Backfill / 迁移与回填
- 建表 / 加字段 / 回填方案

## 7. Risks And Trade-offs / 风险与权衡
- 热点
- 膨胀
- 查询复杂度
````

## Backend Middleware Template / 后端中间件模板

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

## 1. Referenced Inputs / 引用输入材料
- `docs/...`:
  - why it matters

## 2. Scope / 范围
- 涉及的中间件能力

## 3. Middleware Summary / 中间件概览
| Type / 类型 | Resource / 资源 | Purpose / 目的 | Producer / 生产方 | Consumer / 消费方 |
| --- | --- | --- | --- | --- |

## 4. Event / Cache / Search Detail / 事件、缓存与搜索设计
### 3.1 `user.created`
- Trigger / 触发条件:
- Payload / 载荷:
- Ordering / 顺序性:
- Retry / 重试:
- Dead letter / 死信处理:
- Idempotency / 幂等性:
- Monitoring / 监控:

## 5. Failure Handling / 失败处理
- 消息堆积
- 缓存击穿
- 重复消费

## 6. Open Questions / 待确认问题
- 待确认项
````

## Frontend Page Template / 前端页面模板

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

## 1. Referenced Inputs / 引用输入材料
- `docs/...`:
  - why it matters

## 2. Scope / 范围
- 页面目标
- 角色与权限
- 对应用户旅程
- frontend surfaces / 前端交互面:

## 3. Routes / 路由设计
| Route / 路由 | Entry / 入口 | Permission / 权限 | Description / 描述 |
| --- | --- | --- | --- |

## 4. Layout And Regions / 布局与区域划分
### 4.1 Page Skeleton / 页面骨架
- 用 ASCII 文字图、线框描述或等价结构说明展示页面主布局
- 如果源交互文档提供了文字图或线框图，这里默认必须保留等价表达

### 4.2 Region Responsibilities / 区域职责
- 页面区域
- 每个区域承载的核心内容
- 固定区、滚动区、折叠区、覆盖层

### 4.3 First-screen And Variant Layouts / 首屏与变体布局
- 首屏内容
- 空态 / ready 态 / 折叠态 / 展开态 / 错误态的布局差异

要求：
- 不要只写“页面采用左右布局”“有欢迎态”这类过短摘要
- 如果布局结构会影响实现协作，必须保留文字图或区域级结构描述
- 可压缩的是视觉修饰，不可压缩的是区域关系、主块级内容和关键控件组合
- 如果产品文档已经明确给出布局骨架，这一节默认应忠实转写，而不是重新发明页面结构

## 5. User Flow / 用户流程
- 主流程
- 分支流程
- 失败回路
- architecture touchpoints / 架构触点:

## 6. API Interaction / API 交互
| Stage / 阶段 | API | Trigger / 触发条件 | Failure Handling / 失败处理 |
| --- | --- | --- | --- |

## 7. Interaction Design / 交互设计
| Scenario / 场景 | Trigger / 触发条件 | State Change / 状态变化 | Feedback / Motion / 反馈与动效 | Copy / Timing / 文案与时序 | Error / Edge Handling / 异常与边界处理 |
| --- | --- | --- | --- | --- | --- |

要求：
- 直接写最终交互效果
- 如果 planner 已经确定默认值、动画时长、自动消失时间、折叠条件，这里必须直接写出来
- 不要因为去掉追踪字段，就把这些结果删掉
- 如果某个交互效果依赖特定页面区域或线框结构，要和 `Layout And Regions` 的文字图/区域骨架保持一致

## 8. States / 状态设计
- loading
- empty
- error
- success
- disabled
- permission denied

## 9. Telemetry And Guardrails / 埋点与保护措施
- 埋点
- 权限兜底
- 降级策略

## 10. Interaction Coverage Checklist / 交互覆盖清单
| Interaction Effect / 交互效果 | Covered In / 落点位置 | Notes / 备注 |
| --- | --- | --- |

要求：
- 这一节直接写最终要实现的交互效果
- 不要写 `Source Section`、`Requirement ID`、`Plan Ref`
- 如果有未覆盖项，直接写缺口和原因
- 这里用于确认“最终效果是否写进正文”，不是只确认“引用过 planner”
````

## Frontend Component Template / 前端组件模板

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

## 1. Referenced Inputs / 引用输入材料
- `docs/...`:
  - why it matters

## 2. Component Map / 组件地图
| Component / 组件 | Responsibility / 职责 | Parent / 父组件 | Depends On / 依赖 |
| --- | --- | --- | --- |

## 3. Detailed Components / 组件详细设计
### 2.1 `UserProfileForm`
- Purpose / 目的:
- Props / 输入属性:
- Local state / 本地状态:
- Derived state / 派生状态:
- Events / 事件:
- Validation / 校验:
- Error feedback / 错误反馈:

## 4. State Management Strategy / 状态管理策略
- 本地状态
- 全局状态
- 服务端状态

要求：
- 如果 planner 已经确定状态边界和默认行为，这里要直接写结果
- 不要只保留抽象分类而丢掉已确定的状态规则

## 5. Interaction Patterns / 交互模式
| Pattern / 模式 | Trigger / 触发条件 | Component Behavior / 组件行为 | Feedback / Motion / 反馈与动效 | Copy / Timing / 文案与时序 | Rollback / Retry / 回滚与重试 |
| --- | --- | --- | --- | --- | --- |

要求：
- 直接写组件最终要实现的交互模式
- planner 已经确定的动效、toast、modal、自动收起、自动发送等结果必须保留
- 不能因为去掉追踪标签而把这些结果省略

## 6. Accessibility And Edge Cases / 可访问性与边界场景
- 键盘操作
- 异常输入
- 超长文本

## 7. Open Questions / 待确认问题
- 待确认项

## 8. Interaction Coverage Checklist / 交互覆盖清单
| Interaction Effect / 交互效果 | Covered In / 落点位置 | Notes / 备注 |
| --- | --- | --- |

要求：
- 这一节直接写最终要实现的交互效果
- 不要写 `Source Section`、`Requirement ID`、`Plan Ref`
- 如果有未覆盖项，直接写缺口和原因
- 这里检查的是“效果本身是否已经进入最终文档”，不是 planner 是否存在对应字段
````
