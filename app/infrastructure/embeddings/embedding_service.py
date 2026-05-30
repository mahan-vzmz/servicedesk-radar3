from sentence_transformers import SentenceTransformer


class EmbeddingService:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print("Loading embedding model...")

            cls._model = SentenceTransformer(
                r"C:\Users\Victus 16\PycharmProjects\servicedesk-radar\paraphrase-multilingual-MiniLM-L12-v2"
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



