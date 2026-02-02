from typing import Dict
from socketio import AsyncServer

from .manager import get_sio

sio = get_sio()


def register_handlers(sio: AsyncServer):
    """注册所有WebSocket事件处理器"""
    
    @sio.on('connect')
    async def handle_connect(sid: str, environ):
        await sio.emit('connected', {'sid': sid}, to=sid)
    
    @sio.on('disconnect')
    async def handle_disconnect(sid: str):
        await sio.emit('disconnected', {'sid': sid})
    
    @sio.on('join_room')
    async def handle_join_room(data: Dict, sid: str):
        room_id = data.get('room_id')
        session_id = data.get('session_id')
        await sio.enter_room(sid, room_id)
        await sio.emit('user_joined', {'room_id': room_id, 'session_id': session_id}, room=room_id)
    
    @sio.on('leave_room')
    async def handle_leave_room(data: Dict, sid: str):
        room_id = data.get('room_id')
        await sio.leave_room(sid, room_id)
        await sio.emit('user_left', {'room_id': room_id, 'session_id': data.get('session_id')}, room=room_id)
    
    @sio.on('select_team')
    async def handle_select_team(data: Dict, sid: str):
        room_id = data.get('room_id')
        await sio.emit('team_updated', data, room=room_id)
    
    @sio.on('update_name')
    async def handle_update_name(data: Dict, sid: str):
        room_id = data.get('room_id')
        await sio.emit('user_joined', data, room=room_id)
    
    @sio.on('ready')
    async def handle_ready(data: Dict, sid: str):
        room_id = data.get('room_id')
        await sio.emit('team_updated', data, room=room_id)
    
    @sio.on('ban_map')
    async def handle_ban_map(data: Dict, sid: str):
        room_id = data.get('room_id')
        await sio.emit('map_banned', data, room=room_id)
    
    @sio.on('pick_map')
    async def handle_pick_map(data: Dict, sid: str):
        room_id = data.get('room_id')
        await sio.emit('map_picked', data, room=room_id)
    
    @sio.on('send_chat')
    async def handle_send_chat(data: Dict, sid: str):
        room_id = data.get('room_id')
        await sio.emit('chat_message', data, room=room_id)
