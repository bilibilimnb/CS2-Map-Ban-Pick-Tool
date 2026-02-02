from pydantic import BaseModel


class AdminLoginRequest(BaseModel):
    """管理员登录请求"""
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    """管理员登录响应"""
    token: str
    username: str


class MapPoolCreateRequest(BaseModel):
    """创建地图池请求"""
    name: str
    map01_name: str
    map01_icon: str
    map02_name: str
    map02_icon: str
    map03_name: str
    map03_icon: str
    map04_name: str
    map04_icon: str
    map05_name: str
    map05_icon: str
    map06_name: str
    map06_icon: str
    map07_name: str
    map07_icon: str


class RoomCreateRequest(BaseModel):
    """创建房间请求"""
    team_a_name: str
    team_a_icon: str = "/assets/images/default-team-icon.png"
    team_b_name: str
    team_b_icon: str = "/assets/images/default-team-icon.png"
    mappool_config_id: str
