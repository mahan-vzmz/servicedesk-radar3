from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

from app.infrastructure.vector_db.qdrant_clientt import (
    client
)

# =====================================
# Collections
# =====================================

TICKET_COLLECTION = "tickets"

KNOWLEDGE_COLLECTION = "knowledge_articles"


# =====================================
# Create Collections
# =====================================

def create_collection():

    collections = client.get_collections()

    collection_names = [
        collection.name
        for collection in collections.collections
    ]

    if TICKET_COLLECTION not in collection_names:

        client.create_collection(
            collection_name=TICKET_COLLECTION,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print("Tickets collection created.")

    if KNOWLEDGE_COLLECTION not in collection_names:

        client.create_collection(
            collection_name=KNOWLEDGE_COLLECTION,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print("Knowledge collection created.")


# =====================================
# Ticket Functions
# =====================================

def insert_ticket(
    ticket,
    embedding
):

    client.upsert(
        collection_name=TICKET_COLLECTION,
        points=[
            PointStruct(
                id=ticket["id"],
                vector=embedding,
                payload={
                    "title": ticket["title"],
                    "description": ticket["description"],
                    "department": ticket["department"],
                    "priority": ticket["priority"],
                    "tenant": ticket["tenant"],
                    "created_at": str(
                        ticket["created_at"]
                    )
                }
            )
        ]
    )


def search_tickets(
    embedding,
    top_k=5,
    department=None,
    tenant=None
):

    must_conditions = []

    if department:

        must_conditions.append(
            FieldCondition(
                key="department",
                match=MatchValue(
                    value=department
                )
            )
        )

    if tenant:

        must_conditions.append(
            FieldCondition(
                key="tenant",
                match=MatchValue(
                    value=tenant
                )
            )
        )

    query_filter = None

    if must_conditions:

        query_filter = Filter(
            must=must_conditions
        )

    results = client.search(
        collection_name=TICKET_COLLECTION,
        query_vector=embedding,
        query_filter=query_filter,
        limit=top_k
    )

    formatted_results = []

    for result in results:

        formatted_results.append({

            "item": {

                "id": result.id,

                "title":
                    result.payload["title"],

                "description":
                    result.payload["description"],

                "department":
                    result.payload["department"],

                "priority":
                    result.payload["priority"],

                "tenant":
                    result.payload["tenant"],

                "created_at":
                    result.payload["created_at"]
            },

            "semantic_score":
                float(result.score)
        })

    return formatted_results


# =====================================
# Knowledge Functions
# =====================================

def insert_article(
    article,
    embedding
):

    client.upsert(
        collection_name=KNOWLEDGE_COLLECTION,
        points=[
            PointStruct(
                id=article["id"],
                vector=embedding,
                payload={
                    "title": article["title"],
                    "content": article["content"]
                }
            )
        ]
    )


def search_articles(
    embedding,
    top_k=5
):

    results = client.search(
        collection_name=KNOWLEDGE_COLLECTION,
        query_vector=embedding,
        limit=top_k
    )

    formatted_results = []

    for result in results:

        formatted_results.append({

            "id":
                result.id,

            "title":
                result.payload["title"],

            "content":
                result.payload["content"],

            "semantic_score":
                float(result.score)
        })

    return formatted_results