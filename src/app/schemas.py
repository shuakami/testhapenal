"""
模式模块：定义 Pydantic（v2）数据模型，用于请求/响应校验与序列化。
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """创建条目的请求体。"""
    name: str = Field(..., min_length=1, max_length=200, description="名称（必须唯一）")
    description: Optional[str] = Field(None, description="描述")


class ItemRead(BaseModel):
    """条目读取的响应体。"""
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True  # 允许从 ORM 对象转换
