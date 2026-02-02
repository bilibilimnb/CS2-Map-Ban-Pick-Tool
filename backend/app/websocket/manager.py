from typing import Dict
from socketio import AsyncServer
from fastapi import Request
from datetime import datetime

from ..core.deps import get_db
from ..core.config import get_settings
from ..models import User, Room

sio = AsyncServer(async_mode='auto', cors_allowed_origins=get_settings().CORS_ALLOWED_ORIGINS)

# 存储房间连接: {room_id: {sid: user_id}}
rooms: Dict[str, Dict[str, int]] = {}


def get_sio():
    """获取Socket.IO实例"""
    return sio


async def get_user_info(db, session_id: str) -> dict:
    """获取用户信息"""
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.id == int(session_id)))
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    
    return {
        "id": str(user.id),
        "username": user.username,
        "team": user.team,
        "role": user.role.value,
        "is_ready": user.is_ready,
    }


@sio.event
async def connect(sid: str, request: Request):
    """客户端连接"""
    print(f"客户端连接: {sid}")


@sio.event
async def disconnect(sid: str):
    """客户端断开连接"""
    print(f"客户端断开连接: {sid}")
    
    # 从所有房间中移除该连接
    for room_id in list(rooms.keys()):
        if sid in rooms[room_id]:
            del rooms[room_id][sid]
            
            # 通知房间其他用户
            user_id = rooms[room_id].get(sid)
            await sio.emit("user_left", {"user_id": user_id}, room=room_id)
            
            # 如果房间为空，删除房间
            if not rooms[room_id]:
                del rooms[room_id]


@sio.event
async def join_room(data: dict, sid: str):
    """加入房间"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    
    if not room_id or not session_id:
        return
    
    # 加入Socket.IO房间
    await sio.enter_room(sid, room_id)
    
    # 存储连接
    if room_id not in rooms:
        rooms[room_id] = {}
    rooms[room_id][sid] = int(session_id)
    
    # 获取房间用户列表并广播
    from sqlalchemy.ext.asyncio import AsyncSession
    async for db in get_db():
        users = []
        for user_id in rooms[room_id].values():
            user_info = await get_user_info(db, str(user_id))
            if user_info:
                users.append(user_info)
        
        await sio.emit("room_users", {"room_id": room_id, "users": users}, room=room_id)


@sio.event
async def leave_room(data: dict, sid: str):
    """离开房间"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    
    if room_id in rooms:
        if sid in rooms[room_id]:
            user_id = rooms[room_id][sid]
            del rooms[room_id][sid]
            
            # 通知房间其他用户
            await sio.emit("user_left", {"room_id": room_id, "user_id": user_id}, room=room_id)
        
        if not rooms[room_id]:
            del rooms[room_id]


@sio.event
async def select_team(data: dict, sid: str):
    """选择队伍"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    team = data.get("team")
    
    # 广播队伍更新
    await sio.emit("team_updated", {
        "room_id": room_id,
        "session_id": session_id,
        "team": team
    }, room=room_id, skip_sid=sid)


@sio.event
async def update_name(data: dict, sid: str):
    """更新名称"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    display_name = data.get("display_name")
    
    # 广播用户更新
    await sio.emit("user_joined", {
        "room_id": room_id,
        "session_id": session_id,
        "display_name": display_name
    }, room=room_id, skip_sid=sid)


@sio.event
async def ready(data: dict, sid: str):
    """准备状态更新"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    is_ready = data.get("is_ready")
    
    # 广播准备状态
    await sio.emit("ready_updated", {
        "room_id": room_id,
        "session_id": session_id,
        "is_ready": is_ready
    }, room=room_id, skip_sid=sid)


@sio.event
async def roll(data: dict, sid: str):
    """Roll点"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    roll_value = data.get("roll_value")
    
    # 广播Roll结果
    await sio.emit("roll_result", {
        "room_id": room_id,
        "session_id": session_id,
        "roll_value": roll_value
    }, room=room_id)


@sio.event
async def ban_map(data: dict, sid: str):
    """Ban地图"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    map_name = data.get("map_name")
    team = data.get("team")
    
    # 广播地图被Ban
    await sio.emit("map_banned", {
        "room_id": room_id,
        "map_name": map_name,
        "team": team,
        "session_id": session_id
    }, room=room_id)


@sio.event
async def pick_map(data: dict, sid: str):
    """Pick地图"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    map_name = data.get("map_name")
    team = data.get("team")
    
    # 广播地图被Pick
    await sio.emit("map_picked", {
        "room_id": room_id,
        "map_name": map_name,
        "team": team,
        "session_id": session_id
    }, room=room_id)


@sio.event
async def bp_state_update(data: dict, sid: str):
    """BP状态更新"""
    room_id = data.get("room_id")
    bp_state = data.get("bp_state")
    
    # 广播BP状态更新
    await sio.emit("bp_state_updated", {
        "room_id": room_id,
        "bp_state": bp_state
    }, room=room_id)


@sio.event
async def send_chat(data: dict, sid: str):
    """发送聊天消息"""
    room_id = data.get("room_id")
    session_id = data.get("session_id")
    content = data.get("content")
    
    # 获取用户信息
    user_name = "Unknown"
    team = "unknown"
    
    if room_id in rooms and sid in rooms[room_id]:
        from sqlalchemy.ext.asyncio import AsyncSession
        async for db in get_db():
            user_info = await get_user_info(db, session_id)
            if user_info:
                user_name = user_info["username"]
                team = user_info["team"]
            break
    
    # 广播聊天消息
    await sio.emit("chat_message", {
        "room_id": room_id,
        "session_id": session_id,
        "user_name": user_name,
        "team": team,
        "content": content,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }, room=room_id)


async def broadcast_to_room(room_id: str, event: str, data: dict):
    """向房间广播消息"""
    await sio.emit(event, data, room=room_id)


async def broadcast_to_all(event: str, data: dict):
    """向所有连接广播消息"""
    await sio.emit(event, data)
