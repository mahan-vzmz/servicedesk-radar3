import os
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

from app.infrastructure.vector_db.qdrant_client import client

TICKET_COLLECTION    = "tickets"
KNOWLEDGE_COLLECTION = "knowledge_articles"

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "paraphrase-multilingual-MiniLM-L12-v2"
)



def create_collection():

    collections = client.get_collections()
    collection_names = [c.name for c in collections.collections]

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



def insert_ticket(ticket, embedding):
    """
    مشخصات 9.7: Upsert تیکت با payload کامل.
    GAP-1: embedding_model در payload ذخیره می‌شود.
    GAP-2: فیلد status ذخیره می‌شود تا فیلتر بسته/حذف‌شده ممکن باشد.
    """
    client.upsert(
        collection_name=TICKET_COLLECTION,
        points=[
            PointStruct(
                id=ticket["id"],
                vector=embedding,
                payload={
                    "title":           ticket["title"],
                    "description":     ticket["description"],
                    "department":      ticket["department"],
                    "priority":        ticket["priority"],
                    "tenant":          ticket["tenant"],
                    "status":          ticket.get("status", "open"),   # GAP-2
                    "created_at":      str(ticket["created_at"]),
                    "embedding_model": EMBEDDING_MODEL,                # GAP-1
                }
            )
        ]
    )


def search_tickets(
    embedding,
    top_k=5,
    department=None,
    tenant=None,
    exclude_closed=True     # GAP-2: فیلتر تیکت‌های بسته
):
    """
    مشخصات 9.4 و 9.7: جستجوی معنایی با فیلتر metadata.
    GAP-2: تیکت‌های closed/deleted از نتایج حذف می‌شوند.
    """
    must_conditions = []

    # GAP-2: فیلتر status — فقط تیکت‌های open در نتایج باشند
    if exclude_closed:
        must_conditions.append(
            FieldCondition(
                key="status",
                match=MatchValue(value="open")
            )
        )

    if department:
        must_conditions.append(
            FieldCondition(
                key="department",
                match=MatchValue(value=department)
            )
        )

    if tenant:
        must_conditions.append(
            FieldCondition(
                key="tenant",
                match=MatchValue(value=tenant)
            )
        )

    query_filter = None
    if must_conditions:
        query_filter = Filter(must=must_conditions)

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
                "id":              result.id,
                "title":           result.payload["title"],
                "description":     result.payload["description"],
                "department":      result.payload["department"],
                "priority":        result.payload["priority"],
                "tenant":          result.payload["tenant"],
                "status":          result.payload.get("status", "open"),
                "created_at":      result.payload["created_at"],
                "embedding_model": result.payload.get("embedding_model", "unknown"),  # GAP-1
            },
            "semantic_score": float(result.score)
        })

    return formatted_results


# ─── Knowledge Functions ──────────────────────────────────────────────────────

def insert_article(article, embedding):
    """
    مشخصات 9.5: ذخیره مقاله با payload کامل.
    GAP-1: embedding_model در payload.
    GAP-4: category و tags در payload.
    """
    client.upsert(
        collection_name=KNOWLEDGE_COLLECTION,
        points=[
            PointStruct(
                id=article["id"],
                vector=embedding,
                payload={
                    "title":           article["title"],
                    "content":         article["content"],
                    "category":        article.get("category", "general"),  # GAP-4
                    "tags":            article.get("tags", []),              # GAP-4
                    "embedding_model": EMBEDDING_MODEL,                     # GAP-1
                }
            )
        ]
    )


def search_articles(embedding, top_k=5):
    """
    مشخصات 9.5: جستجو در پایگاه دانش.
    GAP-4: category و tags در خروجی برگردانده می‌شوند.
    """
    results = client.search(
        collection_name=KNOWLEDGE_COLLECTION,
        query_vector=embedding,
        limit=top_k
    )

    formatted_results = []
    for result in results:
        formatted_results.append({
            "id":              result.id,
            "title":           result.payload["title"],
            "content":         result.payload["content"],
            "category":        result.payload.get("category", "general"),   # GAP-4
            "tags":            result.payload.get("tags", []),              # GAP-4
            "semantic_score":  float(result.score),
            "embedding_model": result.payload.get("embedding_model", "unknown"),  # GAP-1
        })

    return formatted_results
