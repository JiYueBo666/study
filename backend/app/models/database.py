from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from ..core.config import settings
import logging

# 设置更详细的日志级别
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    # 添加echo=True来显示SQL语句
    engine = create_engine(
        settings.DATABASE_URL,
        echo=True,
        pool_pre_ping=True,  # 添加连接检查
        pool_recycle=3600,  # 设置连接回收时间
        connect_args={
            "connect_timeout": 60,
        },
    )
    Base = declarative_base()
    logger.info("数据库引擎创建成功")
except Exception as e:
    logger.error(f"数据库连接失败: {str(e)}")
    logger.error(f"使用的数据库URL: {settings.DATABASE_URL}")
    raise


def init_db():
    try:
        # 测试连接
        with engine.connect() as connection:
            logger.info("数据库连接测试成功")

        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功！")
    except Exception as e:
        logger.error(f"创建数据库表失败: {str(e)}")
        raise
