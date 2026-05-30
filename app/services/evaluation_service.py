from app.services.infrastructure_service import (
    InfrastructureService
)

from app.infrastructure.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    mrr,
    mean_metric
)

from app.infrastructure.evaluation.evaluation_dataset import (
    EVALUATION_DATASET
)


class EvaluationService:

    def __init__(self):

        self.retrieval_service = (
            InfrastructureService()
        )

    def evaluate(self):

        precisions = []
        recalls = []
        mrr_scores = []

        query_results = []

        for sample in EVALUATION_DATASET:

            query = sample["query"]

            relevant_ids = (
                sample["relevant_ids"]
            )

            results = (

                self.retrieval_service
                .get_similar_tickets(
                    query=query,
                    top_k=5
                )
            )

            p = precision_at_k(
                results,
                relevant_ids,
                5
            )

            r = recall_at_k(
                results,
                relevant_ids,
                5
            )

            m = mrr(
                results,
                relevant_ids
            )

            precisions.append(p)
            recalls.append(r)
            mrr_scores.append(m)

            query_results.append({

                "query":
                    query,

                "precision@5":
                    p,

                "recall@5":
                    r,

                "mrr":
                    m
            })

        return {

            "mean_precision@5":
                mean_metric(
                    precisions
                ),

            "mean_recall@5":
                mean_metric(
                    recalls
                ),

            "mean_mrr":
                mean_metric(
                    mrr_scores
                ),

            "queries":
                query_results
        }
