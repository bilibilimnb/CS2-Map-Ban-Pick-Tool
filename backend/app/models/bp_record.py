from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class BPOperationType(str, enum.Enum):
    """BP 操作类型枚举"""
    ROLL = "roll"  # Roll 点
    BAN = "ban"  # 禁用地图
    PICK = "pick"  # 选择地图
    AUTO = "auto"  # 自动选择（决胜图）


class BPRecord(Base):
    """BP 记录模型"""
    __tablename__ = "bp_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    round_number = Column(Integer, nullable=False)  # 轮次编号
    operation_type = Column(Enum(BPOperationType), nullable=False)  # 操作类型
    operator_team = Column(String(10), nullable=True)  # 操作队伍 "A" or "B"
    map_name = Column(String(50), nullable=True)  # 地图名称
    operation_data = Column(JSON, nullable=True)  # 操作详情数据
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    room = relationship("Room", back_populates="bp_records")


class OperationLog(Base):
    """操作日志模型"""
    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, nullable=True)  # 操作用户ID
    action = Column(String(50), nullable=False)  # 操作类型
    details = Column(JSON, nullable=True)  # 操作详情
    ip_address = Column(String(50), nullable=True)  # IP 地址
    user_agent = Column(String(255), nullable=True)  # 用户代理
    created_at = Column(DateTime(timezone=True), server_default=func.now())
