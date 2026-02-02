from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.deps import get_db, get_current_user

router = APIRouter()


@router.get("/me")
async def get_current_user_info(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取当前用户信息"""
    # TODO: 从数据库获取用户信息
    return {
        "success": True,
        "data": current_user,
    }
