"""
依赖模块：提供获取数据库会话的依赖项（FastAPI 依赖注入）。
"""
from typing import AsyncIterator
from .db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """按请求范围提供数据库会话，自动负责关闭。"""
    async with AsyncSessionLocal() as session:
        yield session
