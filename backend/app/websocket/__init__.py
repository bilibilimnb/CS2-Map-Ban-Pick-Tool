from .manager import get_sio
from .handlers import register_handlers

sio = get_sio()
register_handlers(sio)

__all__ = ["get_sio", "register_handlers"]
