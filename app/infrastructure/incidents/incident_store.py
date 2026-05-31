from datetime import datetime, timedelta
from threading import Lock

class IncidentStore:

    def __init__(self):
        self._incidents: dict = {}
        self._lock = Lock()

    def find_open_incident(self, service_hint: str) -> dict | None:
        with self._lock:
            cutoff = datetime.now() - timedelta(hours=4)
            for inc in self._incidents.values():
                if (
                    inc["service"] == service_hint
                    and inc["status"] == "open"
                    and datetime.fromisoformat(inc["created_at"]) >= cutoff
                ):
                    return inc
        return None

    def create_or_update(
        self,
        service_hint:    str,
        severity:        str,
        matched_count:   int,
        fa_title:        str,
        fa_reason:       str,
        matched_tickets: list
    ) -> dict:

        with self._lock:
            existing = self.find_open_incident(service_hint)

            if existing:
                existing["severity"]         = severity
                existing["matched_count"]    = matched_count
                existing["fa_reason"]        = fa_reason
                existing["matched_tickets"]  = matched_tickets
                existing["updated_at"]       = datetime.now().isoformat()
                existing["is_new"]           = False
                return existing

            inc_id = f"INC-{len(self._incidents) + 1:04d}"
            incident = {
                "incident_id":     inc_id,
                "service":         service_hint,
                "severity":        severity,
                "status":          "open",
                "matched_count":   matched_count,
                "fa_title":        fa_title,
                "fa_reason":       fa_reason,
                "matched_tickets": matched_tickets,
                "created_at":      datetime.now().isoformat(),
                "updated_at":      datetime.now().isoformat(),
                "is_new":          True
            }
            self._incidents[inc_id] = incident
            return incident

    def list_open(self) -> list:
        with self._lock:
            return [
                inc for inc in self._incidents.values()
                if inc["status"] == "open"
            ]

    def close(self, incident_id: str) -> bool:
        with self._lock:
            if incident_id in self._incidents:
                self._incidents[incident_id]["status"]    = "closed"
                self._incidents[incident_id]["closed_at"] = datetime.now().isoformat()
                return True
        return False


# singleton — یک instance در کل برنامه
incident_store = IncidentStore()
