# Architecture Design Writing Guide / 架构设计写作指引

这是一个轻量推荐骨架，不是强制模板。目标是帮助 `architecture-design` skill 产出稳定、清晰、不过度下沉的架构文档。

使用原则：
- 优先用它约束“该写什么、不该写什么”
- 不要求每个项目逐节照抄
- 章节可以合并、重排或省略
- 如果某节需要大量 API / 表结构细节才能成立，通常说明这部分已经越过架构边界，应交给 `technical-design`

术语说明：
- `Background And Goals`：背景与目标，说明为什么做、解决什么、不解决什么
- `Inputs And Constraints`：输入与约束，说明 PRD、调研和现实边界带来的限制
- `Business Domain Partitioning`：业务域划分，说明职责如何分组
- `Service Or Module Boundaries`：服务或模块边界，说明系统如何拆分
- `Core Flows And Failure Paths`：核心流程与异常路径，说明主链路和失败处理链路
- `Technology Choices And Rationale`：技术选型与理由，说明为什么选、为什么不选
- `Data Ownership And Storage Strategy`：数据归属与存储策略，说明谁拥有数据、如何保持一致性
- `Dependency Contract Summary`：依赖契约摘要，说明模块之间如何协作
- `Module Handoff Cards`：模块交接卡，说明后续技术设计要消费的稳定交接信息
- `Work Items`：工作项，说明后续交付如何拆分

## Recommended Sections / 推荐章节

### 1. Background And Goals / 背景与目标

回答：
- 为什么要做这个系统或阶段
- 本轮设计解决什么问题
- 不解决什么问题

### 2. Inputs And Constraints / 输入与约束

回答：
- PRD、research、引用材料带来的关键约束
- 团队能力、时间、兼容性、合规性等现实边界

### 3. Business Domain Partitioning / 业务域划分

回答：
- 系统包含哪些业务域
- 每个业务域的职责边界
- 哪些域应该拆开，哪些域应该聚合

### 4. Service Or Module Boundaries / 服务或模块边界

回答：
- 服务 / 模块怎么划分
- 谁依赖谁
- 哪些边界是稳定契约，哪些只是当前阶段性聚合

这里可以写“交互方式”和“拥有权”，但不要展开 endpoint 级接口定义。

### 5. Core Flows And Failure Paths / 核心流程与异常路径

回答：
- 系统最关键的主流程是什么
- 异常路径在哪里发生
- 哪些位置需要重试、补偿、降级、幂等

推荐使用 Mermaid，但只画对架构有影响的流程。

### 6. Technology Choices And Rationale / 技术选型与理由

回答：
- 关键技术选型是什么
- 为什么是这些选择
- 放弃了哪些备选方案以及原因

这里讨论的是架构层技术路线，不是框架级实现细节清单。

### 7. Data Ownership And Storage Strategy / 数据归属与存储策略

回答：
- 哪个域 / 服务拥有哪类数据
- 哪些数据允许复制、缓存、建立投影
- 一致性要求是什么

这里可以写“订单数据由订单服务主拥有”，但不要写表字段和索引。

### 8. Integration And External Dependencies / 集成关系与外部依赖

回答：
- 依赖了哪些外部系统或共享能力
- 集成方式是同步还是异步
- 哪些依赖会影响交付顺序

### 9. Dependency Contract Summary / 依赖契约摘要

回答：
- 每个模块依赖哪些上游 / 下游模块
- 契约是同步 API、异步事件还是共享读取模型
- 哪些契约应视为稳定边界
- 哪些契约只是阶段性适配

这里仍然只写方向、职责和拥有权，不写 endpoint 字段表或 payload schema。

为了让后续 `technical-design` 可直接消费，依赖契约摘要至少要写清：
- 调用或事件方向
- 同步 / 异步
- 发起方与拥有方
- 契约目的和职责边界
- 交付前置关系
- 失败处理责任归属

### 10. Module Handoff Cards / 模块交接卡

每个后续技术设计单元都要有一张交接卡，建议使用固定字段：

```yaml
- module_id: user-account
  module_name: User Account
  goal: 支撑用户注册、资料维护与身份状态管理
  owner_domain: user-domain
  delivery_scope: both
  frontend_surfaces:
    - 注册页
    - 个人资料页
  ui_ownership_notes:
    - 负责注册流程中的表单交互、提交反馈和资料编辑体验
  upstream_dependencies:
    - iam-gateway
  downstream_dependencies:
    - notification-center
  input_contracts:
    - IAM 网关通过同步鉴权上下文向本模块透传身份信息；IAM 网关负责身份真实性，本模块负责消费与校验业务权限
  output_contracts:
    - 通过同步查询能力向订单模块提供用户基础资料；用户模块拥有资料主数据并负责失败兜底策略
  data_owner:
    - 用户主数据
  delivery_priority: P1
  open_questions:
    - 是否需要支持游客态资料暂存
```

要求：
- `module_id` 必须唯一，使用 kebab-case 英文 slug
- `delivery_scope` 只能是 `backend`、`frontend` 或 `both`
- `frontend_surfaces` 用来标识该模块负责的页面、用户旅程或交互面
- `ui_ownership_notes` 用来说明前端交互归属和跨模块协作边界
- 这些字段要能直接被 `technical-design` 用来选模块、生成路径和确认依赖
- 如果前端归属、依赖责任或契约方向还不明确，必须在 `open_questions` 中显式写出来

字段说明：
- `goal`：该模块要解决的目标，不要写成实现步骤
- `owner_domain`：该模块归属的业务域
- `upstream_dependencies`：本模块依赖的上游模块或系统
- `downstream_dependencies`：依赖本模块输出能力的下游模块
- `input_contracts`：进入本模块的契约，写清方向、职责和拥有方
- `output_contracts`：从本模块输出的契约，写清消费方、边界和失败责任
- `data_owner`：该模块主拥有的数据
- `delivery_priority`：交付优先级，比如 `P0`、`P1`
- `open_questions`：当前还没有收敛、需要后续确认的问题

### 11. Risks, Trade-offs, And Open Questions / 风险、权衡与开放问题

回答：
- 当前设计承担了什么风险
- 做了哪些权衡
- 哪些问题尚未决策

### 12. Work Items / 工作项清单

回答：
- 后续要拆成哪些工作项
- 每个工作项的责任边界

工作项清单建议保持 `module_id: 描述` 格式，并与模块交接卡一一对应，供后续 `technical-design` 解析。

## Quality Check / 质量检查

完成草稿后，自查：
- 文档是否主要在解释边界和协作，而不是实现细节
- 是否有人只看这篇文档就能理解系统怎么拆、为什么这么拆
- 是否避免了 request/response 表、表结构字段表、组件 props/state 之类的内容
- 是否给后续 technical design 留出了明确入口
- 是否为每个技术设计单元提供了可直接消费的模块交接卡
- 模块交接卡是否写清了前端归属和依赖契约最低粒度
