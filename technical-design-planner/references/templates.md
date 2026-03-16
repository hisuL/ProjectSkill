# Technical Design Planner Template

按需读取本文件，为 `technical-design-planner` 生成写入计划文档时提供骨架。目标是沉淀上下文和决策，不是写正式技术设计正文。

## Planner Template / 计划模板

````markdown
---
version: 1.0.0
status: draft
module: user-domain
role: frontend
source_inputs:
  - docs/01-prd/PRD.md
  - docs/02-architecture/architecture-design.md
change_log:
  - version: 1.0.0
    date: YYYY-MM-DD
    changes: initial version
---

# Technical Design Plan

## 1. Scope / 范围
- module_id: 模块唯一标识
- role: 角色，填 `backend` / `frontend` / `both`
- goal: 本次计划要解决的目标
- out_of_scope: 明确不在这次范围内的内容

## 2. Source Inputs / 输入材料
| Source | Type | Why It Matters |
| --- | --- | --- |

字段说明：
- `Source`：来源文件
- `Type`：材料类型，例如 PRD、架构文档、交互文档、研究文档
- `Why It Matters`：为什么它会影响后续技术设计

## 2.1 Referenced Inputs For Final Doc / 最终文档引用材料
-

要求：
- 这里只保留最终技术设计文档开头应显式列出的引用材料
- 每项都要说明为什么会直接影响实现
- 不要把仅供 planner 内部推理的所有过程材料都原样搬进最终文档

## 3. Constraints Summary / 约束摘要
### 3.1 Product Constraints / 产品约束
- ...

### 3.2 Architecture Constraints / 架构约束
- ...

### 3.3 Dependency Constraints / 依赖约束
- ...

### 3.4 Delivery Constraints / 交付约束
- ...

## 4. Architecture Handoff Summary / 架构交接摘要
- module_id: 模块唯一标识
- module_name: 模块名称
- owner_domain: 所属业务域
- delivery_scope: 交付范围，填 `backend` / `frontend` / `both`
- frontend_surfaces: 前端负责的页面、区域或交互面
- ui_ownership_notes: 前端归属说明
- upstream_dependencies: 上游依赖
- downstream_dependencies: 下游依赖
- data_owner: 数据归属

### 4.1 Page Ownership / 页面体验归属
- page_owner_module:
  - 如果交互稿描述的是完整页面、工作台或主用户旅程页面，必须指定唯一归属模块
- page_owner_reason:
  - 为什么该模块必须完整承载页面骨架
- cross_module_frontend_experience_dependencies:
  - 哪些模块提供局部能力
  - 哪些能力必须在 `page_owner_module` 的 `page-design.md` 中统一描述

要求：
- 如果交互稿描述的是完整页面体验，这一节必须填写，不能省略
- 同一页面骨架只能有一个 `page_owner_module`
- 非 `page_owner_module` 的模块不应重复写完整页面骨架，只能引用该页面中的本模块职责片段

### 4.2 Dependency Contract Summary / 依赖契约摘要
| Dependency | Direction | Sync/Async | Initiator | Owner | Purpose | Delivery Prerequisite | Failure Responsibility |
| --- | --- | --- | --- | --- | --- | --- | --- |

字段说明：
- `Dependency`：依赖对象
- `Direction`：方向，流入 / 流出
- `Sync/Async`：同步 / 异步
- `Initiator`：谁发起
- `Owner`：谁负责维护这段契约
- `Purpose`：目的
- `Delivery Prerequisite`：交付前置条件
- `Failure Responsibility`：失败后谁负责兜底

### 4.3 Architecture Gaps / 架构缺口
- 缺失的交接字段:
- 前端归属冲突:
- 依赖责任不清:
- writer 不得自行假设的点:

## 5. Decision Log / 决策记录
| Decision ID | Topic | Options | Recommendation | Why |
| --- | --- | --- | --- | --- |

字段说明：
- `Decision ID`：决策编号，只给 planner 和 writer 内部用
- `Topic`：决策主题
- `Options`：候选方案
- `Recommendation`：推荐方案
- `Why`：推荐原因

## 6. Frontend Interaction Requirements / 前端交互要求
| ID | Source | Source Section | Requirement | Affected Page/Component | Trigger | State Change | Feedback / Motion | Copy / Timing | Edge Cases |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

字段说明：
- `ID`：交互要求编号
- `Source`：来源文件
- `Source Section`：来源章节、子章节或 bullet 位置
- `Requirement`：交互要求本身
- `Affected Page/Component`：影响到的页面或组件
- `Trigger`：触发条件
- `State Change`：状态变化
- `Feedback / Motion`：反馈或动效
- `Copy / Timing`：文案、持续时间、自动消失时间等
- `Edge Cases`：边界情况

如果当前角色不是 frontend，也要明确写：
- 是否存在前端交互依赖
- 是否需要 writer 在跨模块章节里引用这些要求

原子化要求：
- 不要使用 `2.x`、`3.x` 这类聚合 section 作为唯一来源定位
- 尽量精确到原始章节、子章节或 bullet
- 一个明确交互行为对应一条 requirement
- 动效、弹窗、Toast、自动淡出、自动收起、自动发送等行为要单独列项

### 6.1 Layout Fidelity Notes / 布局保真说明
- source_layout_artifacts:
  - 列出交互文档中必须保留的 ASCII 文字图、区域线框、状态面板示意
- must_preserve_structure:
  - 例如：左右 40/60 分栏、底部固定输入区、右侧折叠窄条、欢迎态摘要卡片 + 推荐问题区
- allowed_abstraction:
  - 允许简化的部分
- writer_expectation:
  - writer 必须在最终 `page-design.md` / `component-design.md` 中保留等价文字图、线框描述或分区级结构说明

要求：
- 如果源交互文档提供了文字图、线框图或区域布局示意，这一节必须填写，不能省略
- 不要只写“页面采用左右布局”这种泛化句子
- 要明确哪些结构关系一旦丢失，就会导致最终技术设计可读性下降
- 如果产品阶段已经明确给出布局骨架或区域细节，这里必须标记为“writer 不得自由发挥”

## 7. Risks And Open Questions / 风险与待确认问题
| Type | Detail | Blocking | Owner |
| --- | --- | --- | --- |

字段说明：
- `Type`：`risk` 风险 / `question` 问题
- `Detail`：详细说明
- `Blocking`：是否会阻塞后续写作或实现
- `Owner`：建议谁来确认

## 8. Writing Outline / 写作提纲
- backend/api-design.md: 要写什么
- backend/database-design.md: 要写什么
- backend/middleware-design.md: 要写什么
- frontend/page-design.md: 要写什么
- frontend/component-design.md: 要写什么

## 9. Coverage Checklist / 覆盖检查清单
- [ ] 模块交接卡摘要已整理
- [ ] 架构交接缺口已显式记录
- [ ] 依赖契约最低粒度已补齐
- [ ] PRD 约束已映射
- [ ] 引用文档约束已映射
- [ ] 前端交互要求已逐条记录
- [ ] 交互规格文档已原子化提取，没有被宽泛合并
- [ ] 交互文档中的文字图、线框和区域关系已提炼为布局保真说明
- [ ] loading / empty / error / success 已覆盖
- [ ] 权限态和边界态已覆盖
- [ ] 跨模块依赖已标注
- [ ] 未决问题已列出

## 10. Writer Handoff / 交给 Writer 的内容
- writer_must_cover:
  - ...
- writer_must_not_assume:
  - ...
- writer_open_questions:
  - ...
- page_owner_module:
  - 完整页面骨架归属模块
- cross_module_frontend_experience_dependencies:
  - 哪些模块只提供局部能力
  - 哪些页面效果必须在归属模块中统一写全
- writer_architecture_gaps_to_respect:
  - ...
- writer_referenced_inputs:
  - ...
- writer_planning_artifacts_to_hide:
  - Plan Ref
  - Decision ID
  - Source Section
  - Architecture Ref
- writer_final_interaction_coverage_shape:
  - 直接写成实现结果和交互效果清单，不写追踪字段
- writer_layout_fidelity_requirements:
  - 哪些页面/组件必须保留文字图、区域骨架或线框说明
  - 允许压缩到什么程度
  - 哪些结构绝对不能只写成一句抽象概述
  - 哪些布局点必须逐项进入 `Layout And Regions`
  - 哪些数值、时序、自动行为属于“缺一项即不通过”

## 11. Source Gap Check / 源文档漏项检查
| Source | Source Section / Bullet | Planned Requirement ID | Status | Reason If Missing |
| --- | --- | --- | --- | --- |

要求：
- 对交互规格文档中的关键 section / bullet 做反向检查
- 如果某项未进入 planner，必须写明原因
- 只有明确超出当前模块边界，才允许标记为 `out_of_scope`
- 这个章节只存在于 planner，不应原样出现在最终技术设计文档中

字段说明：
- `Planned Requirement ID`：这条源文档内容最终对应到哪个交互要求编号
- `Status`：已纳入 / 未纳入 / 超出范围
- `Reason If Missing`：如果没纳入，为什么没纳入
````
