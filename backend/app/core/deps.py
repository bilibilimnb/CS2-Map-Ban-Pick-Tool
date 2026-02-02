from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from .config import get_settings
from .security import oauth2_scheme


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话"""
    from ..db.session import async_session_maker
    async with async_session_maker() as session:
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """获取当前用户"""
    from .security import get_current_user as _get_current_user
    return await _get_current_user(token, db)
