"""
数据库初始化脚本
用于创建初始管理员账户和默认地图池
"""
import sys
import os
import asyncio

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session_maker
from app.db.base import Base
from app.models import Admin, MapPool
from app.core.security import get_password_hash


async def init_db(db: AsyncSession) -> None:
    """初始化数据库数据"""
    
    # 创建默认管理员账户
    from sqlalchemy import select
    result = await db.execute(select(Admin).where(Admin.username == "admin"))
    admin = result.scalar_one_or_none()
    
    if not admin:
        admin = Admin(
            username="admin",
            password_hash=get_password_hash("admin123"),
            email="admin@example.com",
            is_active=True
        )
        db.add(admin)
        print("✓ 创建默认管理员账户 (用户名: admin, 密码: admin123)")
    else:
        print("✓ 管理员账户已存在")
    
    # 创建默认地图池
    default_maps = [
        {"name": "Dust2", "image": "/images/maps/dust2.png"},
        {"name": "Mirage", "image": "/images/maps/mirage.png"},
        {"name": "Inferno", "image": "/images/maps/inferno.png"},
        {"name": "Nuke", "image": "/images/maps/nuke.png"},
        {"name": "Overpass", "image": "/images/maps/overpass.png"},
        {"name": "Vertigo", "image": "/images/maps/vertigo.png"},
        {"name": "Ancient", "image": "/images/maps/ancient.png"},
        {"name": "Anubis", "image": "/images/maps/anubis.png"},
    ]
    
    result = await db.execute(select(MapPool).where(MapPool.is_default == True))
    default_mappool = result.scalar_one_or_none()
    
    if not default_mappool:
        # 创建默认地图池（不关联房间，作为模板）
        default_mappool = MapPool(
            room_id=0,  # 临时值，实际使用时会关联到房间
            name="默认地图池",
            maps=default_maps,
            is_default=True
        )
        db.add(default_mappool)
        print("✓ 创建默认地图池")
    else:
        print("✓ 默认地图池已存在")
    
    await db.commit()
    print("\n✓ 数据库初始化完成！")


async def main():
    """主函数"""
    print("开始初始化数据库...")
    
    # 创建所有表
    from app.db.session import engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ 数据库表创建完成")
    
    # 初始化数据
    async with async_session_maker() as db:
        await init_db(db)


if __name__ == "__main__":
    asyncio.run(main())
