from fastapi import APIRouter

from app.schemas.ticket import (
    SimilarTicketRequest
)

from app.services.infrastructure_service import (
    InfrastructureService
)

router = APIRouter()

service = InfrastructureService()


@router.post("/similar")
async def similar_tickets(

    request: SimilarTicketRequest
):

    results = service.get_similar_tickets(

        query=request.query,

        top_k=request.top_k,

        department=request.department,

        tenant=request.tenant
    )

    return {
        "results": results
    }