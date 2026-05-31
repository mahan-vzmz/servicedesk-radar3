from pydantic import BaseModel
from typing import List


class ArticleReference(BaseModel):
  
    article_id:     int
    title:          str
    category:       str
    tags:           List[str]
    semantic_score: float
    snippet:        str     


class SuggestedReplyContext(BaseModel):

    query:                str
    top_article:          ArticleReference | None
    all_articles:         List[ArticleReference]
    has_relevant_article: bool
