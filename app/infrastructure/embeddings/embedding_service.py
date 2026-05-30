import os
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "paraphrase-multilingual-MiniLM-L12-v2"
)


class EmbeddingService:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print(f"Loading embedding model: {EMBEDDING_MODEL}")

            cls._model = SentenceTransformer(
                EMBEDDING_MODEL
            )

        return cls._model

    @classmethod
    def generate_embedding(
        cls,
        text: str
    ):

        model = cls.get_model()

        embedding = model.encode(text)

        return embedding.tolist()
