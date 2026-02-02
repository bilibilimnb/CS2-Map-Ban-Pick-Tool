from pydantic import BaseModel


class BanMapRequest(BaseModel):
    """Ban地图请求"""
    session_id: str
    map_id: str


class PickMapRequest(BaseModel):
    """Pick地图请求"""
    session_id: str
    map_id: str
