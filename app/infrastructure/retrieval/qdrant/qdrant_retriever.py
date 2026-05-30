from app.infrastructure.embeddings.embedding_service import (
    EmbeddingService
)

from app.infrastructure.vector_db.qdrant_store import (
    search_tickets
)


class QdrantRetriever:

    def search(

        self,

        query: str,

        top_k: int = 5,

        department=None,

        tenant=None
    ):

        embedding = (
            EmbeddingService.generate_embedding(
                query
            )
        )

        return search_tickets(

            embedding=embedding,

            top_k=top_k,

            department=department,

            tenant=tenant
        )