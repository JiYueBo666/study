from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate
from ..core.security import hash_password, verify_password
import logging

logger = logging.getLogger(__name__)


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    try:
        logger.info(f"尝试验证用户: {username}")

        # 查找用户
        user = db.query(User).filter(User.username == username).first()
        if not user:
            logger.warning(f"用户不存在: {username}")
            return False

        # 验证密码
        if not verify_password(password, user.hashed_password):
            logger.warning(f"密码错误: {username}")
            return False

        logger.info(f"用户验证成功: {username}")
        return user

    except Exception as e:
        logger.error(f"用户验证过程出错: {str(e)}", exc_info=True)
        raise
