from sqlalchemy.orm import Session
from ..models.article import Article
from ..schemas.article import ArticleCreate
import logging

logger = logging.getLogger(__name__)


def create_article(db: Session, article: ArticleCreate, author_id: int):
    try:
        logger.info(f"Creating article with title: {article.title}")
        logger.info(f"Author ID: {author_id}")

        db_article = Article(
            title=article.title, content=article.content, author_id=author_id
        )

        db.add(db_article)
        db.commit()
        db.refresh(db_article)

        logger.info(f"Article created successfully with ID: {db_article.id}")
        return db_article

    except Exception as e:
        logger.error(f"Error creating article: {str(e)}")
        db.rollback()
        raise


def get_article(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()


def get_articles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Article).offset(skip).limit(limit).all()


def get_user_articles(db: Session, author_id: int):
    return db.query(Article).filter(Article.author_id == author_id).all()


def update_article(db: Session, article_id: int, article_data: dict):
    db_article = db.query(Article).filter(Article.id == article_id)
    db_article.update(article_data)
    db.commit()
    return db_article.first()


def delete_article(db: Session, article_id: int):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article:
        db.delete(db_article)
        db.commit()
    return db_article
