from datetime import datetime

from app.infrastructure.thresholds import (

    INCIDENT_TIME_WINDOW_MINUTES,

    MIN_SIMILAR_TICKETS,

    MIN_RERANK_SCORE
)


class IncidentDetector:

    def detect_incident(

        self,

        results
    ):

        now = datetime.now()

        matched = []

        for result in results:

            ticket = result["item"]

            created_at = datetime.fromisoformat(
                ticket["created_at"]
            )

            minutes_diff = (

                now - created_at

            ).total_seconds() / 60

            is_recent = (

                minutes_diff <=
                INCIDENT_TIME_WINDOW_MINUTES
            )

            is_relevant = (

                result.get(
                    "rerank_score",
                    0
                ) >= MIN_RERANK_SCORE
            )

            if is_recent and is_relevant:

                matched.append(ticket)

        return {

            "incident_detected":
                len(matched)
                >= MIN_SIMILAR_TICKETS,

            "matched_count":
                len(matched),

            "matched_tickets":
                matched
        }