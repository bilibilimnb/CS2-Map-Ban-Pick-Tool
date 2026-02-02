from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class UserRole(str, enum.Enum):
    """用户角色枚举"""
    PLAYER = "player"  # 普通玩家
    CAPTAIN_A = "captain_a"  # A队队长
    CAPTAIN_B = "captain_b"  # B队队长
    SPECTATOR = "spectator"  # 观察者


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    username = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.PLAYER, nullable=False)
    team = Column(String(10), nullable=True)  # "A" or "B"
    roll_value = Column(Integer, nullable=True)  # Roll 点数值
    is_ready = Column(Boolean, default=False)  # 是否准备
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    room = relationship("Room", back_populates="users")
