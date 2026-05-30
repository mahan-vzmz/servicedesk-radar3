from fastapi import APIRouter, HTTPException

from app.services.knowledge_service import KnowledgeService

router = APIRouter()
service = KnowledgeService()


@router.get("/search")
async def search_articles(
    query: str,
    top_k: int = 5
):

    try:
        results = service.search_articles(
            query=query,
            top_k=top_k
        )
        return {"results": results}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
