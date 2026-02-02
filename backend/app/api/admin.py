from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.deps import get_db, get_current_user
from ..core.security import verify_password, get_password_hash, create_access_token
from ..schemas.admin import AdminLoginRequest, AdminLoginResponse, MapPoolCreateRequest, RoomCreateRequest

router = APIRouter()


@router.post("/login")
async def login(
    request: AdminLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """管理员登录"""
    # TODO: 从数据库验证管理员
    # 临时硬编码验证
    if request.username == "admin" and request.password == "admin123":
        token = create_access_token(data={"sub": request.username})
        return AdminLoginResponse(token=token, username=request.username)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )


@router.post("/mappools")
async def create_mappool(
    request: MapPoolCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """创建地图池"""
    # TODO: 实现地图池创建逻辑
    return {"message": "地图池创建成功"}


@router.get("/mappools")
async def get_mappools(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取所有地图池"""
    # TODO: 从数据库获取地图池列表
    return [
        {
            "id": "1",
            "name": "默认地图池",
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
            "is_default": True,
        }
    ]


@router.post("/rooms")
async def create_room(
    request: RoomCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """创建房间"""
    # TODO: 实现房间创建逻辑
    return {
        "id": "room_123",
        "room_code": "ABC12345",
        "team_a_name": request.team_a_name,
        "team_b_name": request.team_b_name,
        "status": "waiting",
    }


@router.get("/rooms")
async def get_rooms(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取房间列表"""
    # TODO: 从数据库获取房间列表
    return {
        "total": 0,
        "items": [],
    }


@router.get("/rooms/{room_id}")
async def get_room_detail(
    room_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取房间详情"""
    # TODO: 从数据库获取房间详情
    return {
        "id": room_id,
        "room_code": "ABC12345",
        "team_a_name": "队伍 A",
        "team_b_name": "队伍 B",
        "status": "waiting",
        "users": {
            "team_a": [
                {"id": "user_1", "display_name": "Player1", "is_ready": True},
            ],
            "team_b": [
                {"id": "user_2", "display_name": "Player2", "is_ready": False},
            ],
        },
    }


@router.get("/rooms/{room_id}/bp-record")
async def get_bp_record(
    room_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取BP记录"""
    # TODO: 从数据库获取BP记录
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
        "operation_logs": [],
    }
