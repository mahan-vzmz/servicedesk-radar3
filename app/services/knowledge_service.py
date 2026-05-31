from app.infrastructure.retrieval.qdrant.knowledge_retriever import KnowledgeRetriever
from app.schemas.knowledge import ArticleReference, SuggestedReplyContext


class KnowledgeService:

    def __init__(self):
        self.retriever = KnowledgeRetriever()

    def search_articles(self, query: str, top_k: int = 5):
        return self.retriever.search(query=query, top_k=top_k)

    def get_reply_context(self, query: str) -> SuggestedReplyContext:

        raw_results = self.retriever.search(query=query, top_k=3)

        article_refs = [
            ArticleReference(
                article_id=     r["id"],
                title=          r["title"],
                category=       r.get("category", "general"),
                tags=           r.get("tags", []),
                semantic_score= r["semantic_score"],
                snippet=        r["content"][:150]
            )
            for r in raw_results
        ]

        return SuggestedReplyContext(
            query=                  query,
            top_article=            article_refs[0] if article_refs else None,
            all_articles=           article_refs,
            has_relevant_article=   len(article_refs) > 0
        )
