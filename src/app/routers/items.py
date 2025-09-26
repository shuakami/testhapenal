"""
业务路由：演示“创建 + 列表 + 详情”三个基础接口。
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Item
from ..schemas import ItemCreate, ItemRead
from ..dependencies import get_db_session

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("", response_model=list[ItemRead], summary="列出条目")
async def list_items(
    limit: int = Query(50, ge=1, le=200, description="返回数量上限"),
    offset: int = Query(0, ge=0, description="偏移量"),
    session: AsyncSession = Depends(get_db_session),
) -> list[ItemRead]:
    """按分页参数返回条目列表。"""
    stmt = select(Item).order_by(Item.id).limit(limit).offset(offset)
    res = await session.execute(stmt)
    rows = res.scalars().all()
    return [ItemRead.model_validate(row) for row in rows]


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED, summary="创建条目")
async def create_item(payload: ItemCreate, session: AsyncSession = Depends(get_db_session)) -> ItemRead:
    """创建新条目；名称要求唯一。"""
    obj = Item(name=payload.name, description=payload.description)
    session.add(obj)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="名称已存在，请更换后重试。",
        )
    await session.refresh(obj)
    return ItemRead.model_validate(obj)


@router.get("/{item_id}", response_model=ItemRead, summary="获取条目详情")
async def get_item(item_id: int, session: AsyncSession = Depends(get_db_session)) -> ItemRead:
    """按 ID 获取单个条目，不存在则返回 404。"""
    obj = await session.get(Item, item_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="条目不存在。")
    return ItemRead.model_validate(obj)
