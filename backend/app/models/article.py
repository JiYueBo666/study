from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200))
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
