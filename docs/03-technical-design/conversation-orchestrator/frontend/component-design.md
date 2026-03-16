---
version: 1.0.0
status: draft
module: conversation-orchestrator
role: frontend
dependencies:
  - chatfile-web
change_log:
  - version: 1.0.0
    date: 2026-03-16
    changes: initial version
---

# Component Design

## 1. Referenced Inputs / 引用输入材料
- `docs/03-technical-design-plans/conversation-orchestrator/design-plan.md`:
  - 固化消息和反馈交互结果。
- `docs/01-prd/ChatFile_interactive.md`:
  - 提供消息气泡、引用来源块、反馈面板和推荐问题样式。

## 2. Component Map / 组件地图
| Component / 组件 | Responsibility / 职责 | Parent / 父组件 | Depends On / 依赖 |
| --- | --- | --- | --- |
| `WelcomePanel` | 渲染摘要和推荐问题 | ConversationPane | `/welcome` API |
| `MessageList` | 渲染消息流和折叠历史 | ConversationPane | stream API |
| `AssistantMessageCard` | 渲染 AI 消息、引用和操作区 | MessageList | citation 数据 |
| `CitationList` | 展示引用来源块并派发点击事件 | AssistantMessageCard | locator 数据 |
| `FeedbackPanel` | 渲染负反馈面板 | AssistantMessageCard | feedback API |

## 3. Detailed Components / 组件详细设计
### 3.1 `WelcomePanel`
- Purpose / 目的:
  - 在对话为空时渲染摘要和 3 个推荐问题。
- Props / 输入属性:
  - `summary`
  - `suggestedQuestions`
  - `hiddenAfterFirstSend`
- Local state / 本地状态:
  - `isVisible`
- Events / 事件:
  - `questionClick(question)`

### 3.2 `AssistantMessageCard`
- Purpose / 目的:
  - 承载 AI 正文、引用来源块、反馈和复制。
- Local state / 本地状态:
  - `citationExpanded`
  - `feedbackExpanded`
  - `copying`
- Error feedback / 错误反馈:
  - 反馈提交失败时保留面板并显示 toast。

### 3.3 `CitationList`
- Purpose / 目的:
  - 展示 `[n] 页码 + 章节路径 + 摘要` 列表。
- Events / 事件:
  - `citationHover`
  - `citationClick`
- Validation / 校验:
  - 无引用时不渲染。

### 3.4 `FeedbackPanel`
- Purpose / 目的:
  - 支持多选标签和最多 200 字补充说明。
- Validation / 校验:
  - 评论超长时禁止提交。

## 4. State Management Strategy / 状态管理策略
- 本地状态：
  - 引用块展开、反馈面板展开、复制中。
- 全局状态：
  - 当前会话流状态、输入禁用截止时间。
- 服务端状态：
  - 摘要、推荐问题、消息完成态、反馈持久化结果。

## 5. Interaction Patterns / 交互模式
| Pattern / 模式 | Trigger / 触发条件 | Component Behavior / 组件行为 | Feedback / Motion / 反馈与动效 | Copy / Timing / 文案与时序 | Rollback / Retry / 回滚与重试 |
| --- | --- | --- | --- | --- | --- |
| 推荐问题发送 | 点击胶囊 | 将问题交给输入区并立即发起问答 | 欢迎态收起 | 首次发送后不再显示 | 发送失败时恢复欢迎态 |
| 引用块展开收起 | 点击标题或折叠控件 | 切换 `citationExpanded` | `250ms ease-in-out` | 默认展开 | 无需重试 |
| 负反馈面板 | 点击 👎 | 滑出面板 | `200ms ease-out` | 取消时恢复未选态 | 提交失败可重试 |
| 复制纯文本 | 点击 📋 | 提取正文纯文本 | toast `已复制到剪贴板` | 3 秒 | 失败提示重试 |

## 6. Accessibility And Edge Cases / 可访问性与边界场景
- 推荐问题、反馈标签、引用项都支持键盘聚焦。
- 引用 hover tooltip 在触屏设备降级为点击展示。
- 中断态消息不可复制未完成引用占位符。

## 7. Open Questions / 待确认问题
- 是否需要给每条推荐问题打点曝光顺序。

## 8. Interaction Coverage Checklist / 交互覆盖清单
| Interaction Effect / 交互效果 | Covered In / 落点位置 | Notes / 备注 |
| --- | --- | --- |
| 推荐问题自动发送并首次后收起 | 3.1 / 5 |  |
| 引用块默认展开、可折叠 | 3.2 / 3.3 / 5 |  |
| 反馈标签多选和 200 字限制 | 3.4 / 5 / 6 |  |
| 复制纯文本并 toast | 3.2 / 5 |  |

