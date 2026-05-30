from fastapi import APIRouter, HTTPException

from app.schemas.ticket import SimilarTicketRequest
from app.services.incident_service import IncidentService

router = APIRouter()
service = IncidentService()


@router.post("/detect")
async def detect_incident(request: SimilarTicketRequest):

    try:
        result = service.analyze_incident(
            query=request.query
        )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
