# WebSocket 事件定义

class SocketEvents:
    """Socket.IO 事件名称"""
    
    # 连接事件
    CONNECT = 'connect'
    DISCONNECT = 'disconnect'
    
    # 房间事件
    JOIN_ROOM = 'join_room'
    LEAVE_ROOM = 'leave_room'
    
    # 用户事件
    USER_JOINED = 'user_joined'
    USER_LEFT = 'user_left'
    
    # 队伍事件
    TEAM_UPDATED = 'team_updated'
    
    # BP 事件
    BP_STARTED = 'bp_started'
    BP_PHASE_CHANGED = 'bp_phase_changed'
    MAP_BANNED = 'map_banned'
    MAP_PICKED = 'map_picked'
    TIMER_TICK = 'timer_tick'
    
    # 聊天事件
    CHAT_MESSAGE = 'chat_message'
    
    # BP 结束事件
    BP_FINISHED = 'bp_finished'
