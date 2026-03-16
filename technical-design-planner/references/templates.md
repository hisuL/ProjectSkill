# Technical Design Planner Template

按需读取本文件，为 `technical-design-planner` 生成写入计划文档时提供骨架。目标是沉淀上下文和决策，不是写正式技术设计正文。

## Planner Template

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

## 1. Scope
- module_id:
- role:
- goal:
- out_of_scope:

## 2. Source Inputs
| Source | Type | Why It Matters |
| --- | --- | --- |

## 3. Constraints Summary
### 3.1 Product Constraints
- ...

### 3.2 Architecture Constraints
- ...

### 3.3 Dependency Constraints
- ...

### 3.4 Delivery Constraints
- ...

## 4. Decision Log
| Decision ID | Topic | Options | Recommendation | Why |
| --- | --- | --- | --- | --- |

## 5. Frontend Interaction Requirements
| ID | Source | Requirement | Affected Page/Component | Trigger | State Change | Feedback / Motion | Edge Cases |
| --- | --- | --- | --- | --- | --- | --- | --- |

如果当前角色不是 frontend，也要明确写：
- 是否存在前端交互依赖
- 是否需要 writer 在跨模块章节里引用这些要求

## 6. Risks And Open Questions
| Type | Detail | Blocking | Owner |
| --- | --- | --- | --- |

## 7. Writing Outline
- backend/api-design.md:
- backend/database-design.md:
- backend/middleware-design.md:
- frontend/page-design.md:
- frontend/component-design.md:

## 8. Coverage Checklist
- [ ] PRD 约束已映射
- [ ] 引用文档约束已映射
- [ ] 前端交互要求已逐条记录
- [ ] loading / empty / error / success 已覆盖
- [ ] 权限态和边界态已覆盖
- [ ] 跨模块依赖已标注
- [ ] 未决问题已列出

## 9. Writer Handoff
- writer_must_cover:
  - ...
- writer_must_not_assume:
  - ...
- writer_open_questions:
  - ...
````
