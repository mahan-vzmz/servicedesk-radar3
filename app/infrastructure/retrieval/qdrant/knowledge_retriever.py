import os
from app.infrastructure.embeddings.embedding_service import EmbeddingService
from app.infrastructure.vector_db.qdrant_store import search_articles

ARTICLE_MIN_SCORE = float(
    os.getenv("ARTICLE_MIN_SCORE", "0.5")
)


class KnowledgeRetriever:

    def search(
        self,
        query: str,
        top_k: int = 5
    ):
        embedding = (
            EmbeddingService.generate_embedding(query)
        )

        results = search_articles(
            embedding=embedding,
            top_k=top_k
        )

        filtered = [
            r for r in results
            if r["semantic_score"] >= ARTICLE_MIN_SCORE
        ]

        return filtered
