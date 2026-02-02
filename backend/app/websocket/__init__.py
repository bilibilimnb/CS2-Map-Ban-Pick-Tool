from .manager import get_sio, sio
from .handlers import register_handlers

# 注册所有事件处理器
register_handlers(sio)

# 创建 Socket.IO ASGI 应用
socket_app = sio.asgi_app

__all__ = ["get_sio", "socket_app"]
