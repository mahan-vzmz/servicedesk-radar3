from app.infrastructure.retrieval.qdrant.knowledge_retriever import (
    KnowledgeRetriever
)


class KnowledgeService:

    def __init__(self):

        self.retriever = (
            KnowledgeRetriever()
        )

    def search_articles(
        self,
        query: str,
        top_k: int = 5
    ):

        return self.retriever.search(
            query=query,
            top_k=top_k
        )