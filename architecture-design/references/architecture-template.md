# Architecture Design Writing Guide

这是一个轻量推荐骨架，不是强制模板。目标是帮助 `architecture-design` skill 产出稳定、清晰、不过度下沉的架构文档。

使用原则：
- 优先用它约束“该写什么、不该写什么”
- 不要求每个项目逐节照抄
- 章节可以合并、重排或省略
- 如果某节需要大量 API / 表结构细节才能成立，通常说明这部分已经越过架构边界，应交给 `technical-design`

## Recommended Sections

### 1. Background And Goals

回答：
- 为什么要做这个系统或阶段
- 本轮设计解决什么问题
- 不解决什么问题

### 2. Inputs And Constraints

回答：
- PRD、research、引用材料带来的关键约束
- 团队能力、时间、兼容性、合规性等现实边界

### 3. Business Domain Partitioning

回答：
- 系统包含哪些业务域
- 每个业务域的职责边界
- 哪些域应该拆开，哪些域应该聚合

### 4. Service Or Module Boundaries

回答：
- 服务 / 模块怎么划分
- 谁依赖谁
- 哪些边界是稳定契约，哪些只是当前阶段性聚合

这里可以写“交互方式”和“拥有权”，但不要展开 endpoint 级接口定义。

### 5. Core Flows And Failure Paths

回答：
- 系统最关键的主流程是什么
- 异常路径在哪里发生
- 哪些位置需要重试、补偿、降级、幂等

推荐使用 Mermaid，但只画对架构有影响的流程。

### 6. Technology Choices And Rationale

回答：
- 关键技术选型是什么
- 为什么是这些选择
- 放弃了哪些备选方案以及原因

这里讨论的是架构层技术路线，不是框架级实现细节清单。

### 7. Data Ownership And Storage Strategy

回答：
- 哪个域 / 服务拥有哪类数据
- 哪些数据允许复制、缓存、建立投影
- 一致性要求是什么

这里可以写“订单数据由订单服务主拥有”，但不要写表字段和索引。

### 8. Integration And External Dependencies

回答：
- 依赖了哪些外部系统或共享能力
- 集成方式是同步还是异步
- 哪些依赖会影响交付顺序

### 9. Risks, Trade-offs, And Open Questions

回答：
- 当前设计承担了什么风险
- 做了哪些权衡
- 哪些问题尚未决策

### 10. Work Items

回答：
- 后续要拆成哪些工作项
- 每个工作项的责任边界

工作项清单请保持 `name: 描述` 格式，供后续 `technical-design` 解析。

## Quality Check

完成草稿后，自查：
- 文档是否主要在解释边界和协作，而不是实现细节
- 是否有人只看这篇文档就能理解系统怎么拆、为什么这么拆
- 是否避免了 request/response 表、表结构字段表、组件 props/state 之类的内容
- 是否给后续 technical design 留出了明确入口
