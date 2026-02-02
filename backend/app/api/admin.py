from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.deps import get_db, get_current_user
from ..core.security import verify_password, get_password_hash, create_access_token
from ..schemas.admin import AdminLoginRequest, AdminLoginResponse, MapPoolCreateRequest, RoomCreateRequest
from ..models import Admin, MapPool, Room

router = APIRouter()


@router.post("/login")
async def login(
    request: AdminLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """管理员登录"""
    # 从数据库验证管理员
    result = await db.execute(select(Admin).where(Admin.username == request.username))
    admin = result.scalar_one_or_none()
    
    if not admin or not verify_password(request.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被禁用",
        )
    
    token = create_access_token(data={"sub": admin.username})
    return AdminLoginResponse(token=token, username=admin.username)


@router.post("/mappools")
async def create_mappool(
    request: MapPoolCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """创建地图池"""
    mappool = MapPool(
        room_id=0,  # 管理员创建的地图池不关联房间
        name=request.name,
        maps=request.maps,
        is_default=False
    )
    db.add(mappool)
    await db.commit()
    await db.refresh(mappool)
    return {"id": mappool.id, "name": mappool.name, "maps": mappool.maps}


@router.get("/mappools")
async def get_mappools(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取所有地图池"""
    result = await db.execute(select(MapPool))
    mappools = result.scalars().all()
    
    # 转换为前端格式
    response = []
    for mp in mappools:
        maps_dict = {}
        for i, m in enumerate(mp.maps, 1):
            maps_dict[f"map{i:02d}_name"] = m["name"]
            maps_dict[f"map{i:02d}_icon"] = m.get("image", "/images/default-map-icon.png")
        
        response.append({
            "id": str(mp.id),
            "name": mp.name,
            "is_default": mp.is_default,
            **maps_dict
        })
    
    return response


@router.post("/rooms")
async def create_room(
    request: RoomCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """创建房间"""
    import random
    import string
    
    # 生成6位房间码
    room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # 检查房间码是否已存在
    existing = await db.execute(select(Room).where(Room.room_code == room_code))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="房间码已存在，请重试",
        )
    
    room = Room(
        room_code=room_code,
        room_name=request.room_name or f"房间 {room_code}",
        team_a_name=request.team_a_name or "Team A",
        team_b_name=request.team_b_name or "Team B",
        max_players=request.max_players or 10,
        status="waiting",
        bp_config=request.bp_config or {},
        bp_state={"current_phase": "waiting"},
    )
    db.add(room)
    await db.commit()
    await db.refresh(room)
    
    return {
        "id": str(room.id),
        "room_code": room.room_code,
        "team_a_name": room.team_a_name,
        "team_b_name": room.team_b_name,
        "status": room.status,
    }


@router.get("/rooms")
async def get_rooms(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取房间列表"""
    result = await db.execute(select(Room).offset(skip).limit(limit))
    rooms = result.scalars().all()
    
    # 获取总数
    count_result = await db.execute(select(Room))
    total = len(count_result.scalars().all())
    
    items = []
    for room in rooms:
        items.append({
            "id": str(room.id),
            "room_code": room.room_code,
            "room_name": room.room_name,
            "team_a_name": room.team_a_name,
            "team_b_name": room.team_b_name,
            "status": room.status,
            "created_at": room.created_at.isoformat() if room.created_at else None,
        })
    
    return {
        "total": total,
        "items": items,
    }


@router.get("/rooms/{room_id}")
async def get_room_detail(
    room_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取房间详情"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="房间不存在",
        )
    
    # 获取房间内的用户
    from ..models import User
    user_result = await db.execute(select(User).where(User.room_id == room_id))
    users = user_result.scalars().all()
    
    team_a_users = []
    team_b_users = []
    
    for user in users:
        user_data = {
            "id": str(user.id),
            "display_name": user.username,
            "is_ready": user.is_ready,
        }
        if user.team == "A":
            team_a_users.append(user_data)
        elif user.team == "B":
            team_b_users.append(user_data)
    
    return {
        "id": str(room.id),
        "room_code": room.room_code,
        "room_name": room.room_name,
        "team_a_name": room.team_a_name,
        "team_b_name": room.team_b_name,
        "status": room.status,
        "users": {
            "team_a": team_a_users,
            "team_b": team_b_users,
        },
        "bp_result": room.bp_result,
    }


@router.get("/rooms/{room_id}/bp-record")
async def get_bp_record(
    room_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取BP记录"""
    from ..models import BPRecord
    
    result = await db.execute(
        select(BPRecord)
        .where(BPRecord.room_id == room_id)
        .order_by(BPRecord.created_at)
    )
    bp_records = result.scalars().all()
    
    # 构建返回数据
    response = {
        "id": f"bp_{room_id}",
        "room_id": str(room_id),
        "operation_logs": [],
    }
    
    for record in bp_records:
        phase_key = f"phase_{record.round_number}"
        if record.operation_type == "ban":
            phase_key += "_ban"
        elif record.operation_type == "pick":
            phase_key += "_pick"
        elif record.operation_type == "roll":
            phase_key = "roll"
        elif record.operation_type == "auto":
            phase_key = "decider"
        
        response[phase_key] = {
            "map_id": record.map_name,
            "team": record.operator_team,
        }
        
        response["operation_logs"].append({
            "phase": phase_key,
            "map_name": record.map_name,
            "team": record.operator_team,
            "created_at": record.created_at.isoformat() if record.created_at else None,
        })
    
    return response
