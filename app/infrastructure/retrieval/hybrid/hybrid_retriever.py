from app.infrastructure.retrieval.qdrant.qdrant_retriever import QdrantRetriever
from app.infrastructure.retrieval.keyword.keyword_retriever import KeywordRetriever
from app.infrastructure.ranking.score_fusion import ScoreFusion
from app.infrastructure.reranking.cross_encoder_reranker import CrossEncoderReranker
from app.infrastructure.data.fake_tickets import tickets
from app.infrastructure.logger import logger


class HybridRetriever:

    def __init__(self):
        self.semantic_retriever = QdrantRetriever()
        self.keyword_retriever  = KeywordRetriever(tickets=tickets)

    def search(
        self,
        query:      str,
        top_k:      int  = 5,
        department=      None,
        tenant=          None,
        exclude_id=      None   
    ):
        semantic_results = self.semantic_retriever.search(
            query=      query,
            top_k=      10,
            department= department,
            tenant=     tenant
        )

        keyword_results = self.keyword_retriever.search(
            query=  query,
            top_k=  10
        )

        fused_results = ScoreFusion.fuse(
            semantic_results,
            keyword_results
        )

        reranked_results = CrossEncoderReranker.rerank(
            query=   query,
            results= fused_results
        )

        if exclude_id is not None:
            reranked_results = [
                r for r in reranked_results
                if r["item"]["id"] != exclude_id
            ]

        logger.info(
            f"Query={query} | "
            f"exclude_id={exclude_id} | "
            f"Results={len(reranked_results)}"
        )

        return reranked_results[:top_k]
