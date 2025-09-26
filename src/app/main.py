"""
应用入口：组装 FastAPI、注册路由、健康检查与启动/关闭事件。
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from .config import settings
from .db import init_models, AsyncSessionLocal, engine
from .routers.items import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理：启动时建表，关闭时正常回收资源。"""
    # 启动：创建表（示例方便）
    await init_models()
    yield
    # 关闭：显式释放连接池（非必须，但更干净）
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# 业务路由
app.include_router(items_router)


@app.get("/", summary="欢迎页")
async def root():
    """返回欢迎信息与指引。"""
    return {
        "message": "Hello, FastAPI on Docker Compose!",
        "docs": "/docs",
        "health": "/health",
        "examples": ["/items"],
    }


@app.get("/health", summary="健康检查")
async def health():
    """健康检查：检查应用可用与数据库连通性。"""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        # 返回基本错误信息（生产可隐藏细节）
        return {"status": "error", "detail": str(e)}
