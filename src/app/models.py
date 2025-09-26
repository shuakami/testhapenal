"""
数据模型模块：定义 SQLAlchemy ORM 模型。
"""
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Text, DateTime


class Base(DeclarativeBase):
    """所有模型的基类。"""
    pass


class Item(Base):
    """示例实体：物品/条目。"""
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False, comment="名称（唯一）")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="描述")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.utcnow, nullable=False, comment="创建时间（UTC）"
    )
