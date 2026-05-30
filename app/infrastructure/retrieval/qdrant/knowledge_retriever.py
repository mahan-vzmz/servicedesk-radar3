from app.infrastructure.embeddings.embedding_service import (
    EmbeddingService
)

from app.infrastructure.vector_db.qdrant_store import (
    search_articles
)


class KnowledgeRetriever:

    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        embedding = (
            EmbeddingService.generate_embedding(
                query
            )
        )

        return search_articles(
            embedding=embedding,
            top_k=top_k
        )