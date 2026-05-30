import os
from sentence_transformers import CrossEncoder

RERANKER_MODEL = os.getenv(
    "RERANKER_MODEL",
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


class CrossEncoderReranker:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print(f"Loading reranker model: {RERANKER_MODEL}")

            cls._model = CrossEncoder(
                RERANKER_MODEL
            )

        return cls._model

    @classmethod
    def rerank(
        cls,
        query,
        results
    ):

        if len(results) == 0:
            return results

        model = cls.get_model()

        sentence_pairs = []

        for result in results:

            item = result["item"]

            text = (
                item["title"]
                + " "
                + item["description"]
            )

            sentence_pairs.append(
                [query, text]
            )

        scores = model.predict(
            sentence_pairs
        )

        reranked_results = []

        for result, score in zip(results, scores):

            result["rerank_score"] = float(score)

            reranked_results.append(result)

        reranked_results.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked_results
