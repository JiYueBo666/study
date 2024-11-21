from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ArticleBase(BaseModel):
    title: str
    content: str


class ArticleCreate(ArticleBase):
    pass


class ArticleResponse(ArticleBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
