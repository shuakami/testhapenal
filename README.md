# Docker Compose + FastAPI

> **亮点**：
> - **最新稳定**：基于 `python:3.13-slim` 构建。
> - **现代框架**：使用 FastAPI + Uvicorn，Pydantic v2，SQLAlchemy 2.x（异步）。
> - **零外部依赖**：内置 **SQLite（aiosqlite 驱动）**，无需额外数据库容器，易跑易懂。
> - **容器化最佳实践**：非 root 用户运行、健康检查、`.dockerignore`、环境变量、热重载（开发）。
> - **尽量简单**：一个 `docker-compose.yml` 就能跑起来。

---

## 快速开始

### 1) 环境要求
- Docker 引擎（建议 24+）
- Docker Compose v2（使用 `docker compose` 命令）

### 2) 启动（开发模式，支持热重载）
```bash
# 进入项目根目录
docker compose up --build
```

启动成功后访问：
- API 文档（Swagger UI）：<http://localhost:8000/docs>
- 健康检查：<http://localhost:8000/health>
- 示例业务接口：
  - `GET  /items`   列表
  - `POST /items`   新建（JSON：{"name": "...", "description": "..."}）
  - `GET  /items/{id}`  详情

> 首次启动会在容器数据卷 `/data/app.db` 位置自动创建 SQLite 数据库。

### 3) 停止 / 后台运行
```bash
# 前台运行（便于查看日志）
docker compose up --build

# 后台运行
docker compose up -d --build

# 停止并清理容器（保留数据卷）
docker compose down
```

### 4) 常见操作
```bash
# 查看应用日志
docker compose logs -f app

# 进入容器交互
docker compose exec app bash
```

