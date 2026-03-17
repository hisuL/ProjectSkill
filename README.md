# ProjectSkill

## 文档阶段结构

当前 `docs/` 目录按设计阶段拆分：

```text
docs/
├── 01-prd/                # 需求输入：PRD、调研、交互稿、图片
├── 02-architecture/       # 架构设计阶段：读取 01-prd 并产出架构设计
├── 03.1-backend-design/   # 后端详细设计阶段
├── 03.2-frontend-design/  # 前端详细设计阶段
└── 04-test/               # 预留给测试阶段
```

其中：
- `02-architecture` 只负责系统级架构设计，不承载前后端详细设计。
- `03.1-backend-design` 和 `03.2-frontend-design` 是后续阶段目录，分别用于后端和前端设计展开。
