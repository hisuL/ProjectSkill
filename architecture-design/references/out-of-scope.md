# Out Of Scope For Architecture Design / 架构设计的越界内容

下列内容不应在架构设计正文中展开。如果确实需要提及，只允许作为“后续技术设计关注点”简短列出，不要展开细节。

术语说明：
- `out of scope`：超出当前文档职责范围的内容
- `architecture docs`：架构设计文档
- `rewrite heuristics`：改写提示，帮助把越界内容收回到架构层表达
- `escape hatch`：例外兜底，只有在极少数情况下允许轻量提及

## Do Not Expand These In Architecture Docs / 架构文档中不要展开这些内容

- endpoint 级 API 设计
- request / response 参数表
- 错误码枚举明细
- 数据库表结构
- 字段类型、默认值、索引策略
- 事件 payload schema
- 页面组件树
- props / state / hooks 设计
- 实现级伪代码
- 迁移脚本或部署命令

## Allowed At Architecture Level / 架构层允许出现的内容

下面这些可以写，但只能写到原则和边界层：

- 服务之间通过同步 API 或异步事件通信
- 某个域拥有主数据，其他域只读或维护投影
- 某类能力需要缓存、搜索或消息队列支持
- 某些链路需要幂等、补偿、降级、审计
- 某个外部系统是关键依赖，需要隔离适配层

## Rewrite Heuristics / 改写提示

如果你发现自己写出了下面这种内容，应该立刻改写：

- `POST /api/v1/orders/create`
  - 改为：`订单服务对外提供订单创建能力，供交易链路同步调用`

- `orders.status varchar(32) not null`
  - 改为：`订单状态由订单服务主拥有，并对外暴露稳定状态语义`

- `request: { userId, couponId }`
  - 改为：`下单请求需要携带用户标识和优惠上下文`

## Escape Hatch / 例外兜底

如果某项目确实需要在架构文档中略提接口或数据，只能满足以下条件：
- 该内容只用于解释架构边界
- 不包含实现级字段明细
- 可以在 2-5 条原则内说清

超过这个粒度，就应该转入 `technical-design`。
