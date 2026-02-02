from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from ..core.deps import get_db
from ..schemas.user import JoinRoomRequest, SelectTeamRequest, UserResponse
from ..models import User, Room, UserRole

router = APIRouter()


@router.get("/me")
async def get_current_user_info(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户信息"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    return {
        "success": True,
        "data": {
            "id": str(user.id),
            "username": user.username,
            "role": user.role.value,
            "team": user.team,
            "is_ready": user.is_ready,
            "room_id": str(user.room_id),
        },
    }


@router.post("/join-room")
async def join_room(
    request: JoinRoomRequest,
    db: AsyncSession = Depends(get_db),
):
    """加入房间"""
    # 检查房间是否存在
    room_result = await db.execute(select(Room).where(Room.room_code == request.room_code))
    room = room_result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="房间不存在",
        )
    
    if room.status != "waiting":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="房间已开始游戏，无法加入",
        )
    
    # 检查房间人数
    user_count_result = await db.execute(
        select(User).where(User.room_id == room.id)
    )
    user_count = len(user_count_result.scalars().all())
    
    if user_count >= room.max_players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="房间已满",
        )
    
    # 创建用户
    user = User(
        room_id=room.id,
        username=request.username,
        role=UserRole.PLAYER,
        is_ready=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return {
        "success": True,
        "data": {
            "user_id": str(user.id),
            "room_id": str(room.id),
            "room_code": room.room_code,
            "room_name": room.room_name,
            "team_a_name": room.team_a_name,
            "team_b_name": room.team_b_name,
            "status": room.status,
        },
    }


@router.post("/select-team")
async def select_team(
    request: SelectTeamRequest,
    db: AsyncSession = Depends(get_db),
):
    """选择队伍"""
    # 获取用户
    user_result = await db.execute(select(User).where(User.id == request.user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    # 获取房间
    room_result = await db.execute(select(Room).where(Room.id == user.room_id))
    room = room_result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="房间不存在",
        )
    
    if room.status != "waiting":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="房间已开始游戏，无法切换队伍",
        )
    
    # 检查队伍人数
    team_users_result = await db.execute(
        select(User).where(User.room_id == room.id, User.team == request.team)
    )
    team_users = team_users_result.scalars().all()
    
    if len(team_users) >= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="队伍已满",
        )
    
    # 更新用户队伍
    user.team = request.team
    await db.commit()
    
    return {
        "success": True,
        "data": {
            "user_id": str(user.id),
            "team": user.team,
        },
    }


@router.post("/ready")
async def toggle_ready(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """切换准备状态"""
    # 获取用户
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    # 切换准备状态
    user.is_ready = not user.is_ready
    await db.commit()
    
    return {
        "success": True,
        "data": {
            "user_id": str(user.id),
            "is_ready": user.is_ready,
        },
    }


@router.post("/roll")
async def roll_dice(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Roll 点"""
    import random
    
    # 获取用户
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    # 获取房间
    room_result = await db.execute(select(Room).where(Room.id == user.room_id))
    room = room_result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="房间不存在",
        )
    
    if room.status != "preparing":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前不是 Roll 阶段",
        )
    
    # 生成 Roll 点
    roll_value = random.randint(1, 100)
    user.roll_value = roll_value
    await db.commit()
    
    return {
        "success": True,
        "data": {
            "user_id": str(user.id),
            "roll_value": roll_value,
        },
    }


@router.get("/room-users/{room_id}")
async def get_room_users(
    room_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取房间用户列表"""
    # 检查房间是否存在
    room_result = await db.execute(select(Room).where(Room.id == room_id))
    room = room_result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="房间不存在",
        )
    
    # 获取房间用户
    user_result = await db.execute(select(User).where(User.room_id == room_id))
    users = user_result.scalars().all()
    
    team_a_users = []
    team_b_users = []
    spectators = []
    
    for user in users:
        user_data = {
            "id": str(user.id),
            "username": user.username,
            "role": user.role.value,
            "is_ready": user.is_ready,
            "roll_value": user.roll_value,
        }
        
        if user.team == "A":
            team_a_users.append(user_data)
        elif user.team == "B":
            team_b_users.append(user_data)
        else:
            spectators.append(user_data)
    
    return {
        "success": True,
        "data": {
            "team_a": team_a_users,
            "team_b": team_b_users,
            "spectators": spectators,
        },
    }
