# Project Memory

## Collaboration Defaults

- 文档与说明默认使用中文简体。
- 优先做增量修改，不要在没有明确收益时整组重写文档。
- 先判断当前修改属于哪个层级，再进入对应目录工作。

## Repo Map

- `docs/01-prd`：产品需求、调研和原始输入。
- `docs/02-architecture`：粗粒度架构设计，只定义边界、职责、协作和关键约束。
- `docs/03-technical-design-plans`：技术设计写作计划，是架构设计到技术设计之间的中间层。
- `docs/03-technical-design`：按模块展开的技术设计文档。
- `architecture-design`：架构设计 skill 说明、模板和越界约束。
- `technical-design*`：技术设计相关 skills 与模板。

## Documentation Flow

- 推荐阅读与产出顺序：`01-prd -> 02-architecture -> 03-technical-design-plans -> 03-technical-design`。
- `02-architecture` 负责稳定边界，不提前下沉到 API 字段、表结构、页面组件树。
- `03-technical-design` 消费的是模块级边界，不应重新发明架构拆分。

## Working Rules

- 修改某个目录前，先读取该目录下的 `CLAUDE.md` 或 `AGENT.md`。
- 如果只影响职责、归属、契约或流程，优先更新最小受影响文档。
- 如果需要调整 `docs/02-architecture`，优先遵守该目录下的局部记忆文件。
