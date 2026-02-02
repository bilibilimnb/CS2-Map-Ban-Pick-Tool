from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from ..core.deps import get_db
from ..schemas.bp import BanMapRequest, PickMapRequest, StartBPRequest
from ..models import Room, User, BPRecord, MapPool, BPOperationType, UserRole

router = APIRouter()


@router.get("/{room_id}/state")
async def get_bp_state(
    room_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取BP状态"""
    # 获取房间
    room_result = await db.execute(select(Room).where(Room.id == room_id))
    room = room_result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="房间不存在",
        )
    
    # 获取地图池
    mappool_result = await db.execute(
        select(MapPool).where(MapPool.room_id == room_id)
    )
    mappool = mappool_result.scalar_one_or_none()
    
    if not mappool:
        # 如果没有地图池，使用默认地图池
        mappool_result = await db.execute(
            select(MapPool).where(MapPool.is_default == True)
        )
        mappool = mappool_result.scalar_one_or_none()
    
    # 获取BP记录
    bp_records_result = await db.execute(
        select(BPRecord)
        .where(BPRecord.room_id == room_id)
        .order_by(BPRecord.created_at)
    )
    bp_records = bp_records_result.scalars().all()
    
    # 构建返回数据
    banned_maps = []
    picked_maps = []
    decider_map = None
    
    for record in bp_records:
        if record.operation_type == BPOperationType.BAN:
            banned_maps.append({
                "map_name": record.map_name,
                "team": record.operator_team,
            })
        elif record.operation_type == BPOperationType.PICK:
            picked_maps.append({
                "map_name": record.map_name,
                "team": record.operator_team,
            })
        elif record.operation_type == BPOperationType.AUTO:
            decider_map = {
                "map_name": record.map_name,
            }
    
    return {
        "success": True,
        "data": {
            "room_id": str(room.id),
            "status": room.status,
            "bp_state": room.bp_state,
            "maps": mappool.maps if mappool else [],
            "banned_maps": banned_maps,
            "picked_maps": picked_maps,
            "decider_map": decider_map,
        },
    }


@router.post("/{room_id}/start")
async def start_bp(
    room_id: int,
    request: StartBPRequest,
    db: AsyncSession = Depends(get_db),
):
    """开始BP流程"""
    # 获取房间
    room_result = await db.execute(select(Room).where(Room.id == room_id))
    room = room_result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="房间不存在",
        )
    
    if room.status != "waiting":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="房间状态不允许开始BP",
        )
    
    # 检查是否所有玩家都已准备
    user_result = await db.execute(
        select(User).where(User.room_id == room_id)
    )
    users = user_result.scalars().all()
    
    if not all(u.is_ready for u in users):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="还有玩家未准备",
        )
    
    # 更新房间状态
    room.status = "preparing"
    room.bp_state = {
        "current_phase": "roll",
        "first_team": None,
        "timer": 15,
    }
    await db.commit()
    
    return {
        "success": True,
        "data": {
            "room_id": str(room.id),
            "status": room.status,
            "bp_state": room.bp_state,
        },
    }


@router.post("/{room_id}/ban")
async def ban_map(
    room_id: int,
    request: BanMapRequest,
    db: AsyncSession = Depends(get_db),
):
    """Ban地图"""
    # 获取房间
    room_result = await db.execute(select(Room).where(Room.id == room_id))
    room = room_result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="房间不存在",
        )
    
    if room.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前不是BP阶段",
        )
    
    # 获取用户
    user_result = await db.execute(select(User).where(User.id == request.user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    # 检查是否是该队伍的操作轮次
    current_phase = room.bp_state.get("current_phase", "")
    expected_team = room.bp_state.get("current_team", "")
    
    if user.team != expected_team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不是你的操作轮次",
        )
    
    # 获取地图池
    mappool_result = await db.execute(
        select(MapPool).where(MapPool.room_id == room_id)
    )
    mappool = mappool_result.scalar_one_or_none()
    
    if not mappool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="地图池不存在",
        )
    
    # 验证地图是否在地图池中
    map_names = [m["name"] for m in mappool.maps]
    if request.map_name not in map_names:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="地图不在地图池中",
        )
    
    # 创建BP记录
    bp_record = BPRecord(
        room_id=room_id,
        round_number=room.bp_state.get("round_number", 1),
        operation_type=BPOperationType.BAN,
        operator_team=user.team,
        map_name=request.map_name,
        operation_data={
            "user_id": request.user_id,
            "username": user.username,
        },
    )
    db.add(bp_record)
    
    # 更新房间BP状态
    update_bp_state(room, "ban", user.team, request.map_name)
    
    await db.commit()
    
    return {
        "success": True,
        "data": {
            "map_name": request.map_name,
            "team": user.team,
            "username": user.username,
            "bp_state": room.bp_state,
        },
    }


@router.post("/{room_id}/pick")
async def pick_map(
    room_id: int,
    request: PickMapRequest,
    db: AsyncSession = Depends(get_db),
):
    """Pick地图"""
    # 获取房间
    room_result = await db.execute(select(Room).where(Room.id == room_id))
    room = room_result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="房间不存在",
        )
    
    if room.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前不是BP阶段",
        )
    
    # 获取用户
    user_result = await db.execute(select(User).where(User.id == request.user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    # 检查是否是该队伍的操作轮次
    current_phase = room.bp_state.get("current_phase", "")
    expected_team = room.bp_state.get("current_team", "")
    
    if user.team != expected_team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不是你的操作轮次",
        )
    
    # 获取地图池
    mappool_result = await db.execute(
        select(MapPool).where(MapPool.room_id == room_id)
    )
    mappool = mappool_result.scalar_one_or_none()
    
    if not mappool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="地图池不存在",
        )
    
    # 验证地图是否在地图池中
    map_names = [m["name"] for m in mappool.maps]
    if request.map_name not in map_names:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="地图不在地图池中",
        )
    
    # 创建BP记录
    bp_record = BPRecord(
        room_id=room_id,
        round_number=room.bp_state.get("round_number", 1),
        operation_type=BPOperationType.PICK,
        operator_team=user.team,
        map_name=request.map_name,
        operation_data={
            "user_id": request.user_id,
            "username": user.username,
        },
    )
    db.add(bp_record)
    
    # 更新房间BP状态
    update_bp_state(room, "pick", user.team, request.map_name)
    
    await db.commit()
    
    return {
        "success": True,
        "data": {
            "map_name": request.map_name,
            "team": user.team,
            "username": user.username,
            "bp_state": room.bp_state,
        },
    }


def update_bp_state(room: Room, operation: str, team: str, map_name: str):
    """更新BP状态"""
    bp_state = room.bp_state or {}
    
    # 添加操作记录
    if "operations" not in bp_state:
        bp_state["operations"] = []
    
    bp_state["operations"].append({
        "operation": operation,
        "team": team,
        "map_name": map_name,
    })
    
    # BO3 BP流程：
    # 1. Roll (决定先后手)
    # 2. Ban A
    # 3. Ban B
    # 4. Pick A
    # 5. Pick B
    # 6. Decider (自动选择剩余地图)
    
    if operation == "roll":
        # Roll完成后，进入Ban阶段
        bp_state["current_phase"] = "ban"
        bp_state["current_team"] = bp_state["first_team"]
        bp_state["round_number"] = 1
    elif operation == "ban":
        if bp_state["current_team"] == "A":
            bp_state["current_team"] = "B"
        else:
            bp_state["current_team"] = "A"
            bp_state["round_number"] += 1
        
        # Ban两轮后进入Pick阶段
        if bp_state["round_number"] > 2:
            bp_state["current_phase"] = "pick"
            bp_state["current_team"] = bp_state["first_team"]
    elif operation == "pick":
        if bp_state["current_team"] == "A":
            bp_state["current_team"] = "B"
        else:
            # Pick完成后，进入Decider阶段
            bp_state["current_phase"] = "decider"
            bp_state["round_number"] += 1
    
    bp_state["timer"] = 15  # 重置计时器
    room.bp_state = bp_state
