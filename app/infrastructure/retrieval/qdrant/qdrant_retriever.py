from app.infrastructure.embeddings.embedding_service import EmbeddingService
from app.infrastructure.vector_db.qdrant_store import search_tickets
from app.infrastructure.logger import logger


class QdrantRetriever:

    def search(
        self,
        query:      str,
        top_k:      int  = 5,
        department=      None,
        tenant=          None
    ):
        embedding = EmbeddingService.generate_embedding(query)

        try:
            return search_tickets(
                embedding=    embedding,
                top_k=        top_k,
                department=   department,
                tenant=       tenant,
                exclude_closed=True     
            )

        except Exception as e:
            logger.warning(
                f"Qdrant unavailable: {e} — switching to FallbackRetriever"
            )
            from app.infrastructure.retrieval.fallback.fallback_retriever import (
                FallbackRetriever
            )
            return FallbackRetriever().search(
                query=      query,
                top_k=      top_k,
                department= department,
                tenant=     tenant
            )
