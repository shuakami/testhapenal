"""
数据库模块：初始化 SQLAlchemy 异步 Engine 与 Session 工厂；
提供创建数据表的辅助函数。
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from .models import Base


# 创建异步引擎（future=True 为 SQLAlchemy 2.x 风格，echo 可开启 SQL 日志）
engine = create_async_engine(
    settings.database_url,
    echo=False,  # 教学时可改为 True 观察 SQL
    future=True,
    pool_pre_ping=True,  # 自动探活连接
)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def init_models() -> None:
    """在应用启动时创建表结构（示例方便，不替代迁移工具）。"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
