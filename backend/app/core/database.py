"""
数据库连接管理模块

使用 SQLAlchemy 管理数据库连接池
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 创建数据库引擎
engine = create_engine(
    settings.neon_db_url,
    pool_pre_ping=True,  # 在使用连接前进行健康检查
    pool_size=5,  # 连接池大小
    max_overflow=10,  # 连接池最大溢出数
)

# 创建 Session 工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 Base 类
Base = declarative_base()


def get_db():
    """
    获取数据库会话（依赖注入）

    Yields:
        数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
