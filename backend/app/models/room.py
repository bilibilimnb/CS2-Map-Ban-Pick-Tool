from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class RoomStatus(str, enum.Enum):
    """房间状态枚举"""
    WAITING = "waiting"  # 等待中
    PREPARING = "preparing"  # 准备中
    IN_PROGRESS = "in_progress"  # BP 进行中
    COMPLETED = "completed"  # 已完成


class Room(Base):
    """房间模型"""
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_code = Column(String(10), unique=True, index=True, nullable=False)
    room_name = Column(String(100), nullable=False)
    status = Column(Enum(RoomStatus), default=RoomStatus.WAITING, nullable=False)
    max_players = Column(Integer, default=10, nullable=False)
    team_a_name = Column(String(50), default="Team A")
    team_b_name = Column(String(50), default="Team B")
    created_by = Column(Integer, nullable=True)  # 创建者用户ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # BP 流程相关字段
    bp_config = Column(JSON, nullable=True)  # BP 配置（轮次、时间等）
    bp_state = Column(JSON, nullable=True)  # BP 当前状态
    bp_result = Column(JSON, nullable=True)  # BP 结果

    # 关系
    users = relationship("User", back_populates="room", cascade="all, delete-orphan")
    bp_records = relationship("BPRecord", back_populates="room", cascade="all, delete-orphan")
