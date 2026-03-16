---
version: 1.0.0
status: draft
module: chatfile-web
role: frontend
change_log:
  - version: 1.0.0
    date: 2026-03-16
    changes: initial version
---

# Design Plan

## 1. Module Scope And Role
- `module_id`: `chatfile-web`
- `role`: `frontend`
- 目标：提供上传、处理状态展示、左右分栏聊天工作台、PDF 预览、输入区和引用联动的统一前端体验。
- 范围内：
  - 全页路由、骨架和区域布局
  - 上传空态、上传中、处理中、失败态、ready 态
  - 40/60 分栏、拖拽调整、预览区折叠展开
  - PDF 预览基础操作、目录侧栏、引用跳转与高亮
  - 输入区状态机、快捷键和异常交互
- 不在范围内：
  - 文档解析业务判定
  - 检索、生成和引用装配逻辑

## 2. Referenced Inputs
- `docs/01-prd/PRD.md`
  - 定义上传、问答、引用、摘要、推荐问题的产品边界。
- `docs/01-prd/ChatFile_interactive.md`
  - 是本模块的高保真主输入，包含页面骨架、区域关系、状态变体、动效和时序。
- `docs/01-prd/research.md`
  - 提供 Next.js 调研方向和 PDF 预览需求背景。
- `docs/02-architecture/architecture-design.md`
  - 固化 `chatfile-web` 为 `page_owner_module`，并给出对后端模块的依赖契约。

## 3. Constraints Summary
- 页面骨架必须保留：
  - 顶部导航
  - 左侧对话区
  - 右侧 PDF 预览区
  - 底部固定输入区
- 默认布局比例 `40% / 60%`，最小各 `30%`，中间分割线可拖拽。
- 预览区可折叠为约 `40px` 窄条，展开/折叠动画 `300ms ease-in-out`。
- 上传区支持拖拽上传、点击上传、格式/大小校验 toast。
- ready 后顶部横幅 `3 秒自动淡出`，输入框自动聚焦。
- PDF 引用跳转需平滑滚动约 `400ms`，高亮呼吸闪烁 `3 次`，每次 `600ms`，之后保留浅高亮。
- 输入区上限 `2000` 字，`Enter` 发送，`Shift+Enter` 换行，生成中禁用并显示 stop。
- 连续 3 次服务失败后，输入区禁用 `30 秒`。

## 4. Decision Log
| Decision | Final Direction | Rationale |
| --- | --- | --- |
| 页面归属 | `chatfile-web` 作为 `page_owner_module`，完整承接页面骨架与跨区域交互链路 | 避免对话区和预览区被多个模块拆散 |
| 路由 | 首版使用单页工作台路由 `/chat` | 产品是单文档 MVP，无需复杂导航 |
| 状态驱动 | 上传和对话主体验由文档状态 + 会话状态双状态机驱动 | 对应交互稿中的完整状态变体 |
| PDF 预览实现 | 先支持页级跳转和 chunk 近似高亮，保留文本层精准定位扩展口 | 与架构开放问题一致 |
| 预览与解析并行 | 上传成功后即可加载 PDF 预览，不等待解析完成 | 减少等待感 |
| 全局通知 | 格式错误、大小超限、复制成功、反馈提交使用顶部 toast，默认停留 3 秒 | 对应交互稿统一行为 |

## 5. Frontend Interaction Requirements
### Fidelity-critical 页面骨架
- `CW-LF-01`
  - 页面必须保留顶部导航、左对话区、右 PDF 预览区、底部固定输入区四大区域。
- `CW-LF-02`
  - 默认 40/60 分栏，分割线拖拽后最小各 30%。
- `CW-LF-03`
  - 预览区折叠后为右侧窄条，点击引用时若当前折叠需先自动展开再跳转。
- `CW-LF-04`
  - 首屏空态为居中上传引导卡，不得被普通按钮替代。

### 上传与处理流程
- `CW-FR-01`
  - 拖拽进入时边框蓝色虚线 + 呼吸动效。
- `CW-FR-02`
  - 非 PDF toast `仅支持 PDF 格式文件`，3 秒自动消失。
- `CW-FR-03`
  - 超 100MB toast `文件大小超过 100MB 限制`。
- `CW-FR-04`
  - 上传中显示实时百分比和取消上传确认弹窗。
- `CW-FR-05`
  - 处理中显示四阶段步骤条与预计耗时，可取消处理。
- `CW-FR-06`
  - ready 后步骤条收起为横幅，3 秒淡出，自动切换工作台。
- `CW-FR-07`
  - 失败态展示具体原因、重新上传和查看详情。

### PDF 预览与跨区域联动
- `CW-FR-08`
  - 预览区支持缩放 50% 到 300%，默认 Fit Width。
- `CW-FR-09`
  - 目录侧栏从左滑入覆盖预览区，点击目录项后自动收起。
- `CW-FR-10`
  - 引用点击后平滑滚动、高亮、左侧竖线标识、最多 5 色循环。
- `CW-FR-11`
  - 旧高亮淡出 200ms，新高亮接管。

### 输入区与异常
- `CW-FR-12`
  - 输入区状态机需覆盖禁用、空闲、可发送、生成中、完成聚焦恢复。
- `CW-FR-13`
  - 粘贴超长文本自动截断到 2000 字并 toast 提示。
- `CW-FR-14`
  - `Esc` 在生成中时停止生成，在反馈面板打开时关闭面板。
- `CW-FR-15`
  - 服务不可用、网络中断、30 秒超时、预览加载失败都有专门错误表现与重试入口。

## 6. Risks And Open Questions
- 风险：PDF 文本层定位不稳定，可能导致高亮与正文不完全重合。
- 风险：分栏拖拽、PDF 渲染、流式对话同时存在时，页面性能可能抖动。
- 风险：输入区、对话区、预览区跨区域联动复杂，需要统一状态源。
- 待确认：暗色模式是首版上线能力还是仅保留视觉 token。
- 待确认：目录数据由后端返回还是前端从 PDF/解析结构临时生成。

## 7. Writing Outline
- `page-design.md`
  - 路由、页面骨架、区域职责、状态变体、跨区域交互链路
- `component-design.md`
  - 上传卡、步骤条、顶栏、PDF 预览器、输入栏、toast 和快捷键帮助

## 8. Coverage Checklist
- 高保真页面骨架已进入页面设计
- 上传空态/上传中/处理中/ready/失败态已进入页面设计
- 40/60 分栏、30% 最小宽度、40px 折叠窄条已进入页面设计
- PDF 跳转、高亮、目录、缩放已进入页面和组件设计
- 输入区状态机、快捷键、字数限制、超长截断已进入页面和组件设计
- 服务异常和预览失败已进入页面设计
- 关键动效参数已进入页面和组件设计

## 9. Writer Handoff
- 推荐写作顺序：
  1. `page-design.md`
  2. `component-design.md`
- writer_must_cover:
  - 完整页面骨架和区域关系
  - 上传到 ready 的状态变体
  - 引用触发的跨区域联动
  - 输入区状态机与快捷键
  - 动效关键数值
- writer_must_not_assume:
  - 不要把整页结构压缩成“左右布局 + 输入框”这类摘要
  - 不要假设多文档、登录或额外导航
- writer_open_questions:
  - 目录数据来源
  - 暗色模式是否上线
- page_owner_module: `chatfile-web`
- cross_module_frontend_experience_dependencies:
  - `document-ingestion` 提供上传/处理状态和失败摘要
  - `conversation-orchestrator` 提供消息流、引用、摘要、推荐问题和反馈结果
- writer_referenced_inputs:
  - `docs/01-prd/PRD.md`
  - `docs/01-prd/ChatFile_interactive.md`
  - `docs/01-prd/research.md`
  - `docs/02-architecture/architecture-design.md`
- writer_planning_artifacts_to_hide:
  - `Requirement ID`
  - `Plan Ref`
  - `Source Section`
- writer_final_interaction_coverage_shape:
  - 页面文档用“布局与区域 + 交互设计 + 覆盖清单”直接呈现最终效果
- writer_layout_fidelity_requirements:
  - 必须保留整页 ASCII 骨架、上传空态骨架、处理步骤条、预览区骨架和输入区状态机

