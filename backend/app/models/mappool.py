from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class MapPool(Base):
    """地图池模型"""
    __tablename__ = "mappools"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)  # 地图池名称
    maps = Column(JSON, nullable=False)  # 地图列表 [{"name": "Dust2", "image": "..."}, ...]
    is_default = Column(Boolean, default=False)  # 是否为默认地图池
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
