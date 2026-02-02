from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings

app = FastAPI(
    title=get_settings().APP_NAME,
    version=get_settings().APP_VERSION,
    debug=get_settings().DEBUG,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print("应用启动中...")
    # 数据库初始化由 Alembic 处理
    print("应用启动完成")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print("应用关闭中...")
    # 清理资源
    print("应用关闭完成")

# 导入路由
from .api import admin, rooms, users, bp, records

app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(rooms.router, prefix="/api/rooms", tags=["Rooms"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(bp.router, prefix="/api/bp", tags=["BP"])
app.include_router(records.router, prefix="/api/records", tags=["Records"])

# WebSocket 集成
from .websocket import socket_app

# 将 Socket.IO ASGI 应用挂载到 FastAPI
app.mount("/socket.io", socket_app)
