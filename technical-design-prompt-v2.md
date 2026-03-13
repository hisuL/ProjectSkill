# Technical-Design Skill 提示词设计

## Skill 定位

基于架构设计文档和PRD文档（支持5W+字符），生成指定工作项的技术设计文档，支持并行调用。

## 📁 Skill 生成位置（必须遵守）

**此 Skill 必须生成在当前项目下**：
- 路径：`.claude/skills/technical-design/SKILL.md`
- 作用范围：仅当前项目
- 不要生成到个人目录（`~/.claude/skills/`）

**文件结构**：
```
.claude/skills/technical-design/
├── SKILL.md           # 必需 - 主要指令
├── reference.md       # 可选 - 详细参考文档
└── examples.md        # 可选 - 使用示例
```

**重要**：此 Skill 必须使用 Plan 模式执行，与用户交互确认后再生成文档。

## 执行流程

### 阶段 1：进入 Plan 模式
1. 使用 `EnterPlanMode` 工具进入计划模式
2. 读取 `docs/02-architecture/architecture-design.md`
3. 读取 `docs/01-prd/PRD.md`
4. 扫描并读取 PRD 和架构文档中所有图片引用
5. 扫描并读取 PRD 和架构文档中所有文档引用

### 阶段 2：工作项分析与确认
1. 解析工作项清单（从 architecture-design.md）
2. 识别工作项间依赖关系
3. **使用 `AskUserQuestion` 确认**：
   - 要生成哪些工作项（如果未指定 module 参数）
   - 要生成哪个角色的文档（backend/frontend/both）
   - 工作项的依赖关系是否正确，是否需要调整开发顺序

### 阶段 3：API 设计确认（backend）
1. 基于 PRD 和架构设计，提出 API 接口设计方案
2. 说明接口路径、请求参数、响应参数、业务逻辑
3. **使用 `AskUserQuestion` 确认**：
   - API 粒度是否合适（粗粒度 vs 细粒度）
   - 业务逻辑的详细程度是否满足编码需求
   - 提供 2-3 种 API 设计方案对比（如 RESTful vs GraphQL，同步 vs 异步）

### 阶段 4：数据库设计确认（backend）
1. 基于业务需求，提出数据库表结构设计方案
2. 说明字段类型、索引策略、数据关系
3. **使用 `AskUserQuestion` 确认**：
   - 表设计是否符合业务需求
   - 索引策略是否合理（查询性能 vs 写入性能）
   - 提供范式化/反范式化方案对比，分析性能、存储、维护性等维度

### 阶段 5：中间件设计确认（backend）
1. 基于架构设计，提出中间件使用方案
2. 说明消息队列 topic、缓存策略、搜索引擎配置
3. **使用 `AskUserQuestion` 确认**：
   - 中间件选型是否合适
   - 通信协议和数据格式是否清晰
   - 提供同步调用 vs 异步消息方案对比，分析一致性、性能、复杂度等维度

### 阶段 6：生成文档
1. 使用 `ExitPlanMode` 退出计划模式
2. 基于所有确认的内容，按目录结构生成技术设计文档
3. 确认文档生成完成

## ⚠️ 强制约束（必须遵守）

**执行模式约束**：
1. **必须使用 `EnterPlanMode` 进入计划模式** - 这是硬性要求，不可跳过
2. **必须分块与用户交互确认，禁止一次性生成完整文档** - 每个设计块都需要用户确认后再继续
3. **必须使用 `AskUserQuestion` 逐块确认** - 工作项选择、API设计、数据库设计、中间件设计等
4. **必须提供充分的建议和替代方案** - 不要只给一个选项，要分析利弊
5. **必须使用 `ExitPlanMode` 退出计划模式后再生成文档** - 不得在 Plan 模式内直接生成

**内容读取约束**：
1. **必须读取 PRD 中所有引用的图片**（`![](path)` 或 `<img src="path">`）
2. **必须读取 PRD 中所有引用的文档**（`[链接](path.md)` 或相对路径）
3. **必须读取架构文档中所有引用的图片和文档**
4. **必须使用 Read 工具读取引用内容** - 不得假设或跳过

**格式约束**：
1. **目录结构必须严格按照 `{module}/{role}/` 格式**
2. **必须包含 YAML frontmatter**（version、status、dependencies、change_log）
3. **业务逻辑必须足够详细** - 供编码 Agent 使用，包含异常处理和边界条件
4. **增量更新必须标记变更**（`<!-- UPDATED: 日期 -->`、`<!-- BREAKING: 说明 -->`）

## 输入输出

**输入**：
- `docs/01-prd/PRD.md`（业务需求，可能包含图片和文档引用）
- `docs/02-architecture/architecture-design.md`（架构设计，用于获取工作项清单和技术栈）
- 参数：`module`（工作项名称，可选）
- 参数：`role`（backend/frontend，可选）

**输出**：
- `docs/03-technical-design/{module}/{role}/*.md`

## 目录结构

```
docs/03-technical-design/
  ├── user-domain/
  │   ├── backend/
  │   │   ├── api-design.md
  │   │   ├── database-design.md
  │   │   └── middleware-design.md
  │   └── frontend/
  │       ├── page-design.md
  │       └── component-design.md
  └── order-domain/
      └── ...
```

**设计原因**：前后端文档在同一工作项目录下，方便排查问题时查看完整上下文。测试团队独立设计测试方案，不依赖此设计体系。

## 核心能力

### 1. 解析架构设计
- 读取 architecture-design.md
- **处理引用内容**：
  - 扫描架构文档中的图片引用和文档引用
  - 使用 Read 工具读取所有引用内容
- 提取工作项清单（解析 `module-name: 描述` 格式）
- 识别工作项间依赖关系

### 2. 生成技术文档
- **backend**：api-design.md + database-design.md + middleware-design.md
- **frontend**：page-design.md + component-design.md

### 3. 支持并行调用
- 可指定单个工作项生成
- 可指定单个角色生成
- 多个工作项可同时调用（不同 Agent 并行）

## 文档内容要点

### API 设计（backend）
- 接口路径、请求参数、响应参数
- **业务逻辑**（重要！编码 Agent 需要这个上下文）
- 数据字典（枚举值、错误码）
- 依赖的其他工作项 API

### 数据库设计（backend）
- 表结构（字段、类型、注释）
- 索引设计
- 数据关系图（Mermaid ER 图）

### 中间件设计（backend）
- 使用的中间件（消息队列、缓存、搜索引擎等）
- 通信协议和数据格式
- 消息/事件定义
- 中间件配置要点

### 页面设计（frontend）
- 页面路由、布局
- 组件列表
- 交互流程
- API 调用

### 组件设计（frontend）
- 组件 Props、State
- 组件方法
- 状态管理

## 关键设计点

### 业务逻辑的位置
建议在 API 设计中，每个接口下面写业务逻辑：
```markdown
### 用户注册
- 接口路径：POST /api/v1/users/register
- 业务逻辑：
  1. 校验用户名唯一性
  2. 密码加密存储
  3. 调用 notification-domain 发送欢迎邮件
```

或者单独一个章节：
```markdown
## 业务逻辑
### 用户注册流程
1. 校验用户名唯一性
2. ...
```

### 工作项依赖关系
在 frontmatter 中声明：
```yaml
dependencies: [notification-domain, order-domain]
```

在文档中交叉引用：
```markdown
## 依赖关系
- 依赖 [通知域 API](../../notification-domain/backend/api-design.md)
```

### 变更标记
与架构设计相同：
- `<!-- UPDATED: 日期 -->`
- 
- `<!-- BREAKING: 说明 -->`
- `<!-- TODO: 说明 -->`

### Status 字段说明
```markdown
<!--
技术设计评审通过后，请手动修改 frontmatter 中的 status 字段：
status: draft → status: approved
-->
```

## 调用方式

### 方式 1：手动指定
```
/technical-design module=user-domain role=backend
```

### 方式 2：自动读取
```
/technical-design
```
自动读取 architecture-design.md 中的工作项清单，生成所有工作项。

### 方式 3：并行调用
多个 Agent 同时调用，每个 Agent 负责不同工作项：
- Agent 1: `/technical-design module=user-domain`
- Agent 2: `/technical-design module=order-domain`

## skill要解决的问题

1. 如何解析架构设计中的工作项清单？
   - 使用正则匹配 `module-name: 描述` 格式
   - 提取所有工作项到列表
2. 如何处理 PRD 和架构文档中的图片和文档引用？
   - 扫描 `![](...)` 和 `[](...)` 语法
   - 使用 Read 工具读取引用内容
   - 将引用内容纳入技术设计上下文
3. 如何根据工作项名称生成对应的技术文档？
   - 按 `docs/03-technical-design/{module}/{role}/` 结构创建目录
   - 根据 role 参数生成对应文档
4. 如何确保业务逻辑写得足够详细（供编码 Agent 使用）？
   - 在 API 设计中每个接口下详细描述业务逻辑
   - 包含异常处理、边界条件、依赖调用
5. 如何设计中间件的通信协议和数据格式？
   - 明确消息队列的 topic/queue 命名
   - 定义消息体结构（JSON Schema）
6. 如何建立工作项间的依赖关系？
   - 在 frontmatter 中声明 dependencies
   - 在文档中使用相对路径交叉引用
7. 如何确保前后端文档在同一目录下？
   - 严格按照 `{module}/backend/` 和 `{module}/frontend/` 结构
8. 如何确保与用户交互？
   - 必须使用 EnterPlanMode 进入计划模式
   - 使用 AskUserQuestion 确认工作项选择和角色
   - 使用 ExitPlanMode 退出并执行

---

## 🔴 执行检查清单（再次强调）

执行此 Skill 前，请确认：

**阶段 1：准备**
- [ ] 已调用 `EnterPlanMode` 工具
- [ ] 已读取 `docs/02-architecture/architecture-design.md`
- [ ] 已读取 `docs/01-prd/PRD.md`
- [ ] 已扫描并读取 PRD 中所有图片引用
- [ ] 已扫描并读取 PRD 中所有文档引用
- [ ] 已扫描并读取架构文档中所有图片引用和文档引用

**阶段 2-5：分块交互（每个阶段必须单独确认）**
- [ ] 已使用 `AskUserQuestion` 确认工作项选择和依赖关系
- [ ] 已使用 `AskUserQuestion` 确认 API 设计方案（提供粗粒度/细粒度对比）
- [ ] 已使用 `AskUserQuestion` 确认数据库设计方案（提供范式化/反范式化对比）
- [ ] 已使用 `AskUserQuestion` 确认中间件设计方案（提供同步/异步对比）

**阶段 6：生成文档**
- [ ] 已调用 `ExitPlanMode` 工具
- [ ] 目录结构符合 `{module}/{role}/` 格式
- [ ] 已添加完整的 YAML frontmatter（version、status、dependencies、change_log）
- [ ] 业务逻辑描述足够详细（包含异常处理、边界条件、依赖调用）
- [ ] 增量更新已标记变更（如适用）

**交互质量要求**：
- [ ] 每次 `AskUserQuestion` 都提供了 2-3 个选项或方案
- [ ] 每个方案都说明了利弊和适用场景
- [ ] 没有一次性生成完整文档，而是逐块确认后再继续

**违反以上任一约束，视为执行失败。**
