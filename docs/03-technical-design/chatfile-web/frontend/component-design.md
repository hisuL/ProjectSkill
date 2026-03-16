---
version: 1.0.0
status: draft
module: chatfile-web
role: frontend
dependencies:
  - conversation-orchestrator
  - document-ingestion
change_log:
  - version: 1.0.0
    date: 2026-03-16
    changes: initial version
---

# Component Design

## 1. Referenced Inputs / 引用输入材料
- `docs/03-technical-design-plans/chatfile-web/design-plan.md`:
  - 固化整页骨架和高保真交互要求。
- `docs/01-prd/ChatFile_interactive.md`:
  - 提供上传卡、步骤条、预览器和输入栏细节。

## 2. Component Map / 组件地图
| Component / 组件 | Responsibility / 职责 | Parent / 父组件 | Depends On / 依赖 |
| --- | --- | --- | --- |
| `TopBar` | 展示产品和当前文档信息 | ChatWorkspacePage | 文档状态 |
| `UploadDropzone` | 空态上传、拖拽和校验 | ChatWorkspacePage | 上传 API |
| `ProcessingStepper` | 上传中和处理中步骤展示 | ChatWorkspacePage | 状态查询 API |
| `PreviewPanel` | PDF 预览、目录、缩放、页码导航和高亮 | ChatWorkspacePage | 预览元数据 |
| `ComposerBar` | 输入、上传/更换文档、发送/停止 | ChatWorkspacePage | 对话流 API |
| `ToastCenter` | 顶部通知 | ChatWorkspacePage | 全局 UI 事件 |

## 3. Detailed Components / 组件详细设计
### 3.1 `UploadDropzone`
- Purpose / 目的:
  - 在空态承载拖拽上传和点击上传。
- Props / 输入属性:
  - `acceptedMime=application/pdf`
  - `maxSizeBytes=104857600`
- Local state / 本地状态:
  - `isDragActive`
  - `isUploading`
- Events / 事件:
  - `fileSelected`
  - `uploadCancelled`
- Validation / 校验:
  - 类型和大小校验失败直接发 toast。

### 3.2 `ProcessingStepper`
- Purpose / 目的:
  - 展示上传中百分比和处理中步骤条。
- Derived state / 派生状态:
  - `currentStage`
  - `estimatedRemainingMs`
- Error feedback / 错误反馈:
  - 显示失败原因和查看详情入口。

### 3.3 `PreviewPanel`
- Purpose / 目的:
  - 承载 PDF 预览、缩放、目录侧栏和引用高亮。
- Local state / 本地状态:
  - `collapsed`
  - `zoomLevel`
  - `activeHighlight`
  - `tocOpen`
- Events / 事件:
  - `toggleCollapse`
  - `jumpToCitation`
  - `openToc`

### 3.4 `ComposerBar`
- Purpose / 目的:
  - 固定底部输入、上传入口和发送/停止。
- Local state / 本地状态:
  - `draft`
  - `isGenerating`
  - `charCount`
  - `disabledUntil`
- Validation / 校验:
  - 纯空白禁止发送
  - 超过 2000 字禁止发送

## 4. State Management Strategy / 状态管理策略
- 本地状态：
  - 拖拽高亮、目录开关、缩放比例、输入草稿。
- 全局状态：
  - 当前 `docId`、文档状态、预览折叠状态、输入禁用截止时间。
- 服务端状态：
  - 上传进度、处理阶段、ready 横幅数据、预览元数据、对话流状态。

## 5. Interaction Patterns / 交互模式
| Pattern / 模式 | Trigger / 触发条件 | Component Behavior / 组件行为 | Feedback / Motion / 反馈与动效 | Copy / Timing / 文案与时序 | Rollback / Retry / 回滚与重试 |
| --- | --- | --- | --- | --- | --- |
| 拖拽进入 | 文件拖入 | `UploadDropzone` 高亮 | 虚线边框呼吸 + 遮罩淡入 | 200ms | 拖出后回退 |
| 上传进度 | 上传请求进行中 | `ProcessingStepper` 显示百分比 | 线性进度条 | 实时刷新 | 取消后回空态 |
| 步骤推进 | 状态轮询变化 | 当前步骤 loading，已完成打勾 | loading 图标 + 动态省略号 | 到 ready 后切横幅 | 失败时切错误卡 |
| 预览折叠/展开 | 点击折叠按钮 | `PreviewPanel` 切宽度 | `300ms ease-in-out` | 折叠至 40px 窄条 | 引用跳转时自动展开 |
| 高亮切换 | 点击新引用 | 清旧高亮，设新高亮 | 旧高亮 200ms 淡出，新高亮 3 次呼吸 | 3 秒后变浅高亮 | 若定位失败回退到页级高亮 |
| 输入发送 | Enter 或点击发送 | `ComposerBar` 锁定输入，按钮变 stop | 无额外动效 | 完成后清空并聚焦 | 失败可重试 |
| 超长粘贴 | 粘贴超 2000 字 | 自动截断 | toast `输入内容已截断至 2000 字` | 3 秒 | 无需重试 |

## 6. Accessibility And Edge Cases / 可访问性与边界场景
- `Ctrl + K` 聚焦输入框，`Ctrl + U` 打开上传，`Ctrl + /` 打开快捷键帮助。
- 折叠预览时，展开按钮保留键盘可聚焦。
- PDF 预览失败不阻塞对话区和输入区。

## 7. Open Questions / 待确认问题
- 快捷键帮助面板是否首版即实现，还是仅保留键盘行为。

## 8. Interaction Coverage Checklist / 交互覆盖清单
| Interaction Effect / 交互效果 | Covered In / 落点位置 | Notes / 备注 |
| --- | --- | --- |
| 拖拽高亮和格式/大小校验 toast | 3.1 / 5 |  |
| 上传进度和步骤条推进 | 3.2 / 5 |  |
| 预览折叠 40px 与自动展开 | 3.3 / 5 / 6 |  |
| 引用高亮切换与 3 次呼吸 | 3.3 / 5 |  |
| 输入 2000 字限制和 stop | 3.4 / 5 |  |
| 超长粘贴自动截断 | 3.4 / 5 |  |
