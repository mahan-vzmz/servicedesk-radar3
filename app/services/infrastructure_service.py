from app.infrastructure.retrieval.hybrid.hybrid_retriever import (
    HybridRetriever
)


class InfrastructureService:

    def __init__(self):

        self.retriever = (
            HybridRetriever()
        )

    def get_similar_tickets(

        self,

        query: str,

        top_k: int,

        department=None,

        tenant=None
    ):

        return self.retriever.search(

            query=query,

            top_k=top_k,

            department=department,

            tenant=tenant
        )