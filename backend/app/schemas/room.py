from pydantic import BaseModel


class RoomInfo(BaseModel):
    """房间信息"""
    id: str
    room_code: str
    team_a_name: str
    team_a_icon: str
    team_b_name: str
    team_b_icon: str
    status: str
    mappool: dict


class JoinRoomRequest(BaseModel):
    """加入房间请求"""
    session_id: str
    team: str | None = None
    display_name: str | None = None


class UpdateReadyRequest(BaseModel):
    """更新准备状态请求"""
    session_id: str
    is_ready: bool
