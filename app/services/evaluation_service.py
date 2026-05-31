import numpy as np

from app.services.infrastructure_service import InfrastructureService
from app.infrastructure.embeddings.embedding_service import EmbeddingService
from app.infrastructure.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    mrr,
    mean_metric,
    mean_category_accuracy,
    similarity_quality,
    threshold_report,
)
from app.infrastructure.evaluation.evaluation_dataset import (
    EVALUATION_DATASET,
    SIMILARITY_PAIRS,
)

DEPT_TO_CATEGORY = {
    "IT":         "network",
    "Support":    "email",
    "Operations": "hardware",
    "HR":         "account",
}


class EvaluationService:

    def __init__(self):
        self.retrieval_service = InfrastructureService()

    def evaluate(self) -> dict:

        precisions, recalls, mrr_scores = [], [], []
        category_predictions = []
        query_results        = []

        for sample in EVALUATION_DATASET:
            query        = sample["query"]
            relevant_ids = sample["relevant_ids"]
            expected_cat = sample.get("category", "unknown")

            results = self.retrieval_service.get_similar_tickets(
                query=query, top_k=5
            )

            p = precision_at_k(results, relevant_ids, 5)
            r = recall_at_k(results, relevant_ids, 5)
            m = mrr(results, relevant_ids)

            precisions.append(p)
            recalls.append(r)
            mrr_scores.append(m)

            if results:
                top_dept     = results[0]["item"].get("department", "unknown")
                predicted_cat = DEPT_TO_CATEGORY.get(top_dept, "unknown")
                category_predictions.append((predicted_cat, expected_cat))

            query_results.append({
                "query":       query,
                "category":    expected_cat,
                "precision@5": round(p, 4),
                "recall@5":    round(r, 4),
                "mrr":         round(m, 4),
            })

        sim_quality = self._evaluate_similarity_quality()

        thresh_report = self._threshold_report(EVALUATION_DATASET[0])

        best_threshold = self._pick_best_threshold(thresh_report)

        return {
            "total_queries":         len(EVALUATION_DATASET),
            "mean_precision@5":      round(mean_metric(precisions), 4),
            "mean_recall@5":         round(mean_metric(recalls), 4),
            "mean_mrr":              round(mean_metric(mrr_scores), 4),
            "category_accuracy":     round(                            
                mean_category_accuracy(category_predictions), 4
            ),
            "similarity_quality":    sim_quality,                      
            "threshold_report":      thresh_report,                     
            "recommended_threshold": best_threshold,                   
            "queries":               query_results,
        }


    def _evaluate_similarity_quality(self) -> dict:

        similar_scores, dissimilar_scores = [], []

        for q_a, q_b, is_similar in SIMILARITY_PAIRS:
            vec_a = np.array(EmbeddingService.generate_embedding(q_a))
            vec_b = np.array(EmbeddingService.generate_embedding(q_b))

            norm  = np.linalg.norm(vec_a) * np.linalg.norm(vec_b) + 1e-9
            score = float(np.dot(vec_a, vec_b) / norm)

            if is_similar:
                similar_scores.append(score)
            else:
                dissimilar_scores.append(score)

        return similarity_quality(similar_scores, dissimilar_scores)


    def _threshold_report(self, sample: dict) -> list:

        results = self.retrieval_service.get_similar_tickets(
            query=sample["query"], top_k=10
        )
        return threshold_report(
            results=      results,
            relevant_ids= sample["relevant_ids"],
            k=5
        )

    def _pick_best_threshold(self, report: list) -> float:

        best_f1  = -1.0
        best_thr = 0.75

        for row in report:
            p = row["precision@k"]
            r = row["recall@k"]
            f1 = (2 * p * r / (p + r)) if (p + r) > 0 else 0.0
            if f1 > best_f1:
                best_f1  = f1
                best_thr = row["threshold"]

        return best_thr
