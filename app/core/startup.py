from app.infrastructure.vector_db.qdrant_store import (

    create_collection,

    insert_ticket
)

from app.infrastructure.embeddings.embedding_service import (
    EmbeddingService
)

from app.infrastructure.data.fake_tickets import (
    tickets
)

from app.infrastructure.data.fake_articles import (
    articles
)

from app.infrastructure.vector_db.qdrant_store import (
    insert_article
)

def load_ticket_embeddings():

    print("Initializing Qdrant...")

    create_collection()

    for ticket in tickets:

        text = (

            ticket["title"] +

            " " +

            ticket["description"]
        )

        embedding = (
            EmbeddingService.generate_embedding(
                text
            )
        )

        insert_ticket(

            ticket=ticket,

            embedding=embedding
        )

    for article in articles:
        text = (

                article["title"]

                + " "

                + article["content"]
        )

        embedding = (
            EmbeddingService.generate_embedding(
                text
            )
        )

        insert_article(
            article=article,
            embedding=embedding
        )

    print("Qdrant indexing completed.")
