from fastapi import APIRouter, HTTPException

from app.schemas.ticket import SimilarTicketRequest
from app.services.infrastructure_service import InfrastructureService

router = APIRouter()
service = InfrastructureService()


@router.post("/similar")
async def similar_tickets(request: SimilarTicketRequest):

    try:
        results = service.get_similar_tickets(
            query=request.query,
            top_k=request.top_k,
            department=request.department,
            tenant=request.tenant
        )
        return {"results": results}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
