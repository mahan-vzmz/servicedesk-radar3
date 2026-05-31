import numpy as np
from app.infrastructure.embeddings.embedding_service import EmbeddingService
from app.infrastructure.data.fake_tickets import tickets
from app.infrastructure.logger import logger


class FallbackRetriever:

    def search(
        self,
        query:      str,
        top_k:      int  = 5,
        department=      None,
        tenant=          None
    ):
        logger.warning("FallbackRetriever active — Qdrant is unavailable")

        query_vec = np.array(
            EmbeddingService.generate_embedding(query)
        )

        results = []

        for ticket in tickets:

            # GAP-2: فیلتر تیکت‌های بسته
            if ticket.get("status", "open") != "open":
                continue

            # فیلتر metadata
            if department and ticket.get("department") != department:
                continue
            if tenant and ticket.get("tenant") != tenant:
                continue

            text = ticket["title"] + " " + ticket["description"]
            ticket_vec = np.array(
                EmbeddingService.generate_embedding(text)
            )

            norm = (
                np.linalg.norm(query_vec)
                * np.linalg.norm(ticket_vec)
                + 1e-9
            )
            score = float(np.dot(query_vec, ticket_vec) / norm)

            results.append({
                "item":           ticket,
                "semantic_score": score,
                "keyword_score":  0.0,
                "final_score":    score,
                "rerank_score":   score * 10
            })

        results.sort(
            key=lambda x: x["semantic_score"],
            reverse=True
        )
        return results[:top_k]
