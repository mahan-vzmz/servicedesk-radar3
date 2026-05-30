from fastapi import APIRouter

from app.services.evaluation_service import (
    EvaluationService
)

router = APIRouter()

service = EvaluationService()


@router.get("/retrieval")
async def evaluate_retrieval():

    return service.evaluate()