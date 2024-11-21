from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from ....crud import article as article_crud
from ....schemas.article import ArticleCreate, ArticleResponse
from ....db.session import get_db
from ....core.auth import get_current_user
from ....models.user import User

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=ArticleResponse)
async def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        logger.info(f"尝试创建文章: {article.title}")
        logger.info(f"当前用户: {current_user.username}")

        result = article_crud.create_article(db, article, current_user.id)
        logger.info(f"文章创建成功: {result.id}")
        return result
    except Exception as e:
        logger.error(f"创建文章失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建文章失败: {str(e)}",
        )


@router.get("/{article_id}", response_model=ArticleResponse)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = article_crud.get_article(db, article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article


@router.get("/", response_model=List[ArticleResponse])
def read_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    articles = article_crud.get_articles(db, skip=skip, limit=limit)
    return articles


@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_article = article_crud.get_article(db, article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if db_article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return article_crud.update_article(db, article_id, article.dict())


@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_article = article_crud.get_article(db, article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if db_article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    article_crud.delete_article(db, article_id)
    return {"message": "Article deleted successfully"}
