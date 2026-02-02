from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.deps import get_db, get_current_user

router = APIRouter()


@router.get("/{room_id}")
async def get_bp_record(
    room_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取BP记录"""
    # TODO: 从数据库获取BP记录
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="需要管理员权限",
        )
    
    return {
        "id": "bp_123",
        "room_id": room_id,
        "phase_1_ban": {"map_id": "map01", "team": "team_a"},
        "phase_2_ban": {"map_id": "map02", "team": "team_b"},
        "phase_3_pick": {"map_id": "map03", "team": "team_a"},
        "phase_4_pick": {"map_id": "map04", "team": "team_b"},
        "phase_5_ban": {"map_id": "map05", "team": "team_a"},
        "phase_6_ban": {"map_id": "map06", "team": "team_b"},
        "decider": {"map_id": "map07"},
        "operation_logs": [
            {
                "phase": 1,
                "action_type": "ban",
                "map_id": "map01",
                "team": "team_a",
                "user_name": "Player1",
                "timestamp": 1704067200,
            },
        ],
    }
