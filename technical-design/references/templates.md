# Technical Design Compatibility Templates

这个文件不再承载正式模板内容。

`technical-design` 现在只是兼容入口，负责把流程路由到两个新 skill：

- `technical-design-planner`
- `technical-design-writer`

## How To Use / 使用方式

如果当前目标是整理技术设计写入计划，请读取：
- `technical-design-planner/references/templates.md`

如果当前目标是基于计划文档写正式技术设计，请读取：
- `technical-design-writer/references/templates.md`

## Compatibility Rule / 兼容规则

不要再从这个文件直接生成：
- `api-design.md`
- `database-design.md`
- `middleware-design.md`
- `page-design.md`
- `component-design.md`

正确流程必须是：

```text
technical-design
  -> technical-design-planner
  -> docs/03-technical-design-plans/{module}/design-plan.md
  -> technical-design-writer
  -> docs/03-technical-design/{module}/...
```

## Why This File Still Exists / 为什么保留此文件

保留该文件是为了兼容旧路径引用，避免外部仍然读取
`technical-design/references/templates.md`
时得到过期模板。

如果读到本文件，应立即跳转到对应的新模板文件，而不是继续在此处生成文档。
