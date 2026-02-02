from typing import Dict
from socketio import AsyncServer
from fastapi import Request

from ..core.deps import get_db
from ..core.config import get_settings

sio = AsyncServer(async_mode='auto', cors_allowed_origins=get_settings().CORS_ALLOWED_ORIGINS)

# 存储房间连接
rooms: Dict[str, Dict[str, str]] = {}


def get_sio():
    """获取Socket.IO实例"""
    return sio


@sio.event
async def connect(sid: str, request: Request):
    """客户端连接"""
    # TODO: 实现连接逻辑
    pass


@sio.event
async def disconnect(sid: str):
    """客户端断开连接"""
    # TODO: 实现断开连接逻辑
    pass


@sio.event
async def join_room(data: dict, sid: str):
    """加入房间"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    
    if not room_id or not session_id:
        return
    
    # 加入房间
    await sio.enter_room(sid, room_id)
    
    # 存储连接
    if room_id not in rooms:
        rooms[room_id] = {}
    rooms[room_id][sid] = session_id


@sio.event
async def leave_room(data: dict, sid: str):
    """离开房间"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    
    if room_id in rooms:
        if sid in rooms[room_id]:
            del rooms[room_id][sid]
        
        if not rooms[room_id]:
            del rooms[room_id]


@sio.event
async def select_team(data: dict, sid: str):
    """选择队伍"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    team = data.get("team")
    
    # 广播队伍更新
    await sio.emit("team_updated", {"room_id": room_id, "team": team}, room=room_id, skip_sid=sid)


@sio.event
async def update_name(data: dict, sid: str):
    """更新名称"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    display_name = data.get("display_name")
    
    # 广播用户更新
    await sio.emit("user_joined", {"room_id": room_id, "session_id": session_id, "display_name": display_name}, room=room_id, skip_sid=sid)


@sio.event
async def ready(data: dict, sid: str):
    """准备状态更新"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    is_ready = data.get("is_ready")
    
    # 广播准备状态
    await sio.emit("team_updated", {"room_id": room_id, "session_id": session_id, "is_ready": is_ready}, room=room_id, skip_sid=sid)


@sio.event
async def ban_map(data: dict, sid: str):
    """Ban地图"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    map_id = data.get("map_id")
    
    # 广播地图被Ban
    await sio.emit("map_banned", {"room_id": room_id, "map_id": map_id, "session_id": session_id}, room=room_id)


@sio.event
async def pick_map(data: dict, sid: str):
    """Pick地图"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    map_id = data.get("map_id")
    
    # 广播地图被Pick
    await sio.emit("map_picked", {"room_id": room_id, "map_id": map_id, "session_id": session_id}, room=room_id)


@sio.event
async def send_chat(data: dict, sid: str):
    """发送聊天消息"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    content = data.get("content")
    
    # 获取用户信息
    user_name = "Unknown"
    team = "unknown"
    
    if room_id in rooms:
        for sid_info in rooms[room_id].values():
            if sid_info == session_id:
                # TODO: 从数据库获取用户信息
                user_name = "Player"
                team = "team_a"
                break
    
    # 广播聊天消息
    await sio.emit("chat_message", {
        "room_id": room_id,
        "session_id": session_id,
        "user_name": user_name,
        "team": team,
        "content": content,
        "timestamp": "2024-01-01T00:00:00Z",
    }, room=room_id)
