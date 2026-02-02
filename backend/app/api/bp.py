from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.deps import get_db, get_current_user
from ..schemas.bp import BanMapRequest, PickMapRequest

router = APIRouter()


@router.post("/{room_id}/ban")
async def ban_map(
    room_id: str,
    request: BanMapRequest,
    db: AsyncSession = Depends(get_db),
):
    """Ban地图"""
    # TODO: 实现Ban地图逻辑
    return {
        "success": True,
        "data": {
            "map_id": request.map_id,
            "team": "team_a",
            "user_name": "Player1",
        },
    }


@router.post("/{room_id}/pick")
async def pick_map(
    room_id: str,
    request: PickMapRequest,
    db: AsyncSession = Depends(get_db),
):
    """Pick地图"""
    # TODO: 实现Pick地图逻辑
    return {
        "success": True,
        "data": {
            "map_id": request.map_id,
            "team": "team_a",
            "user_name": "Player1",
        },
    }
