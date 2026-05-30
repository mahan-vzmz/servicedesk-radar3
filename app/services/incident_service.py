from app.services.infrastructure_service import (
    InfrastructureService
)

from app.infrastructure.incidents.incident_detector import (
    IncidentDetector
)


class IncidentService:

    def __init__(self):

        self.infrastructure = (
            InfrastructureService()
        )

        self.detector = (
            IncidentDetector()
        )

    def analyze_incident(

        self,

        query: str
    ):

        results = (
            self.infrastructure
            .get_similar_tickets(

                query=query,

                top_k=10
            )
        )

        return self.detector.detect_incident(
            results
        )