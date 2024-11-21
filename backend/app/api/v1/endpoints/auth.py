from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import timedelta
import logging
from ....core.security import create_access_token
from ....crud import user as user_crud
from ....schemas.token import Token
from ....db.session import get_db
from ....core.config import settings

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


# 添加 JSON 请求模型
class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest, db: Session = Depends(get_db)  # 使用 JSON 模型
):
    try:
        logger.info(f"收到登录请求: username={login_data.username}")

        user = user_crud.authenticate_user(db, login_data.username, login_data.password)

        if not user:
            logger.warning(
                f"登录失败: 用户名或密码错误 (username={login_data.username})"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"用户验证成功: username={login_data.username}")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        logger.info(f"登录成功: username={login_data.username}")
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"登录过程出错: {str(e)}", exc_info=True)
        raise
