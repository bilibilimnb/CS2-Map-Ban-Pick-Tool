from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.deps import get_db, get_current_user
from ..schemas.room import RoomInfo, JoinRoomRequest, UpdateReadyRequest

router = APIRouter()


@router.get("/{room_code}")
async def get_room_by_code(
    room_code: str,
    db: AsyncSession = Depends(get_db),
):
    """通过房间码获取房间信息"""
    # TODO: 从数据库查询房间
    return RoomInfo(
        id="room_123",
        room_code=room_code,
        team_a_name="队伍 A",
        team_a_icon="/assets/images/default-team-icon.png",
        team_b_name="队伍 B",
        team_b_icon="/assets/images/default-team-icon.png",
        status="waiting",
        mappool={
            "map01_name": "Mirage",
            "map01_icon": "/assets/images/default-map-icon.png",
            "map02_name": "Inferno",
            "map02_icon": "/assets/images/default-map-icon.png",
            "map03_name": "Dust2",
            "map03_icon": "/assets/images/default-map-icon.png",
            "map04_name": "Nuke",
            "map04_icon": "/assets/images/default-map-icon.png",
            "map05_name": "Anubis",
            "map05_icon": "/assets/images/default-map-icon.png",
            "map06_name": "Vertigo",
            "map06_icon": "/assets/images/default-map-icon.png",
            "map07_name": "Ancient",
            "map07_icon": "/assets/images/default-map-icon.png",
        },
    )


@router.post("/{room_id}/join")
async def join_room(
    room_id: str,
    request: JoinRoomRequest,
    db: AsyncSession = Depends(get_db),
):
    """加入房间"""
    # TODO: 实现加入房间逻辑
    return {
        "success": True,
        "data": {
            "user_id": "user_123",
        },
    }


@router.post("/{room_id}/ready")
async def update_ready(
    room_id: str,
    request: UpdateReadyRequest,
    db: AsyncSession = Depends(get_db),
):
    """更新准备状态"""
    # TODO: 实现更新准备状态逻辑
    return {
        "success": True,
        "data": {
            "user_id": request.session_id,
            "is_ready": request.is_ready,
        },
    }


@router.get("/{room_id}/users")
async def get_room_users(
    room_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取房间用户列表"""
    # TODO: 从数据库获取用户列表
    return {
        "success": True,
        "data": {
            "team_a": [
                {"id": "user_1", "display_name": "Player1", "is_ready": True},
            ],
            "team_b": [
                {"id": "user_2", "display_name": "Player2", "is_ready": False},
            ],
        },
    }


@router.post("/{room_id}/bp/start")
async def start_bp(
    room_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """开始BP流程"""
    # TODO: 验证管理员权限并开始BP
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="需要管理员权限",
        )
    
    return {
        "success": True,
        "data": {
            "roll_a": 45,
            "roll_b": 78,
            "first_pick_team": "team_b",
        },
    }


@router.get("/{room_id}/bp/status")
async def get_bp_status(
    room_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取BP状态"""
    # TODO: 从数据库获取BP状态
    return {
        "success": True,
        "data": {
            "status": "ban1",
            "current_team": "team_b",
            "current_user": "Player2",
            "remaining_time": 12,
            "banned_maps": ["map01"],
            "picked_maps": [],
            "available_maps": ["map02", "map03", "map04", "map05", "map06", "map07"],
        },
    }
