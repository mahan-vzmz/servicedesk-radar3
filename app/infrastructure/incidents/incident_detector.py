from datetime import datetime

from app.infrastructure.thresholds import (
    INCIDENT_TIME_WINDOW_MINUTES,
    MIN_SIMILAR_TICKETS_MEDIUM,
    MIN_SIMILAR_TICKETS_HIGH,
    MIN_RERANK_SCORE
)
from app.infrastructure.incidents.incident_store import incident_store


class IncidentDetector:

    def detect_incident(self, results) -> dict:

        now     = datetime.now()
        matched = []

        for result in results:
            ticket     = result["item"]
            created_at = datetime.fromisoformat(ticket["created_at"])
            minutes_diff = (now - created_at).total_seconds() / 60

            is_recent   = minutes_diff <= INCIDENT_TIME_WINDOW_MINUTES
            is_relevant = result.get("rerank_score", 0) >= MIN_RERANK_SCORE

            if is_recent and is_relevant:
                matched.append(ticket)

        matched_count = len(matched)

        if matched_count >= MIN_SIMILAR_TICKETS_HIGH:
            severity         = "high"
            incident_detected = True
        elif matched_count >= MIN_SIMILAR_TICKETS_MEDIUM:
            severity         = "medium"
            incident_detected = True
        else:
            severity         = None
            incident_detected = False

        if not incident_detected:
            return {
                "incident_detected": False,
                "severity":          None,
                "matched_count":     matched_count,
                "matched_tickets":   matched,
                "fa_title":          None,
                "fa_reason":         None,
                "incident_id":       None,
                "is_new_incident":   False
            }

        service_hint = self._extract_service(matched)
        fa_title = f"رخداد احتمالی در سرویس {service_hint}"
        fa_reason = (
            f"تعداد {matched_count} تیکت مشابه "
            f"در {INCIDENT_TIME_WINDOW_MINUTES} دقیقه اخیر شناسایی شد. "
            f"سطح: {severity}."
        )

        incident = incident_store.create_or_update(
            service_hint=    service_hint,
            severity=        severity,
            matched_count=   matched_count,
            fa_title=        fa_title,
            fa_reason=       fa_reason,
            matched_tickets= matched
        )

        return {
            "incident_detected": True,
            "severity":          severity,
            "matched_count":     matched_count,
            "matched_tickets":   matched,
            "fa_title":          fa_title,
            "fa_reason":         fa_reason,
            "incident_id":       incident["incident_id"],
            "is_new_incident":   incident["is_new"]
        }

    def _extract_service(self, tickets: list) -> str:
        keywords = {
            "VPN":     "VPN",
            "MFA":     "MFA",
            "Outlook": "ایمیل",
            "Email":   "ایمیل",
            "Printer": "پرینتر",
            "Network": "شبکه",
            "Password":"پسورد",
            "Account": "اکانت",
            "Laptop":  "لپ‌تاپ",
            "Monitor": "مانیتور",
        }
        for ticket in tickets:
            title = ticket.get("title", "")
            for key, label in keywords.items():
                if key.lower() in title.lower():
                    return label
        return "نامشخص"
