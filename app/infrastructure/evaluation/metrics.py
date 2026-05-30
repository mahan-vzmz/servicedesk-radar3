def precision_at_k(
    results,
    relevant_ids,
    k=5
):

    top_results = results[:k]

    hits = sum(

        1

        for result in top_results

        if result["item"]["id"] in relevant_ids
    )

    return hits / k


def recall_at_k(
    results,
    relevant_ids,
    k=5
):

    top_results = results[:k]

    hits = sum(

        1

        for result in top_results

        if result["item"]["id"] in relevant_ids
    )

    return hits / len(relevant_ids)


def mrr(
    results,
    relevant_ids
):

    for idx, result in enumerate(results):

        if result["item"]["id"] in relevant_ids:

            return 1 / (idx + 1)

    return 0

def mean_metric(values):

    if not values:
        return 0

    return sum(values) / len(values)