from fastapi import APIRouter

from app.schemas.ticket import (
    SimilarTicketRequest
)

from app.services.incident_service import (
    IncidentService
)

router = APIRouter()

service = IncidentService()


@router.post("/detect")
async def detect_incident(

    request: SimilarTicketRequest
):

    result = service.analyze_incident(
        query=request.query
    )

    return result