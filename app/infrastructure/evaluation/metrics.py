def precision_at_k(results, relevant_ids, k=5):
    hits = sum(
        1 for r in results[:k]
        if r["item"]["id"] in relevant_ids
    )
    return hits / k if k > 0 else 0.0


def recall_at_k(results, relevant_ids, k=5):
    if not relevant_ids:
        return 0.0
    hits = sum(
        1 for r in results[:k]
        if r["item"]["id"] in relevant_ids
    )
    return hits / len(relevant_ids)


def mrr(results, relevant_ids):
    for idx, result in enumerate(results):
        if result["item"]["id"] in relevant_ids:
            return 1 / (idx + 1)
    return 0.0


def mean_metric(values):
    return sum(values) / len(values) if values else 0.0

def category_accuracy(predicted_category: str, expected_category: str) -> float:
    return 1.0 if predicted_category == expected_category else 0.0


def mean_category_accuracy(predictions: list) -> float:
    if not predictions:
        return 0.0
    scores = [
        category_accuracy(pred, exp)
        for pred, exp in predictions
    ]
    return sum(scores) / len(scores)

def similarity_quality(
    similar_scores:    list,
    dissimilar_scores: list
) -> dict:

    if not similar_scores or not dissimilar_scores:
        return {
            "avg_similar_score":    0.0,
            "avg_dissimilar_score": 0.0,
            "pairs_correct":        0,
            "total_pairs":          0,
            "quality_rate":         0.0,
            "recommended_threshold": 0.75
        }

    avg_similar    = sum(similar_scores)    / len(similar_scores)
    avg_dissimilar = sum(dissimilar_scores) / len(dissimilar_scores)

    pairs = min(len(similar_scores), len(dissimilar_scores))
    correct = sum(
        1 for s, d in zip(similar_scores, dissimilar_scores)
        if s > d
    )

    return {
        "avg_similar_score":     round(avg_similar, 4),
        "avg_dissimilar_score":  round(avg_dissimilar, 4),
        "pairs_correct":         correct,
        "total_pairs":           pairs,
        "quality_rate":          round(correct / pairs, 4) if pairs > 0 else 0.0,
        "recommended_threshold": round((avg_similar + avg_dissimilar) / 2, 2)
    }



THRESHOLD_CANDIDATES = [0.70, 0.75, 0.78, 0.82]


def threshold_report(results, relevant_ids, k=5) -> list:

    report = []
    for threshold in THRESHOLD_CANDIDATES:
        filtered = [
            r for r in results
            if r.get("semantic_score", 0) >= threshold
        ]
        report.append({
            "threshold":    threshold,
            "results_kept": len(filtered),
            "precision@k":  precision_at_k(filtered, relevant_ids, k) if filtered else 0.0,
            "recall@k":     recall_at_k(filtered, relevant_ids, k) if filtered else 0.0,
            "mrr":          mrr(filtered, relevant_ids) if filtered else 0.0,
        })
    return report
