from fastapi import APIRouter, HTTPException

from app.schemas.ticket import SimilarTicketRequest
from app.services.incident_service import IncidentService
from app.infrastructure.incidents.incident_store import incident_store

router  = APIRouter()
service = IncidentService()


@router.post("/detect")
async def detect_incident(request: SimilarTicketRequest):
    try:
        return service.analyze_incident(query=request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/open")
async def list_open_incidents():
    return {"incidents": incident_store.list_open()}

@router.post("/close/{incident_id}")
async def close_incident(incident_id: str):
    success = incident_store.close(incident_id)
    if not success:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {"status": "closed", "incident_id": incident_id}
