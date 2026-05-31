from pydantic import BaseModel


class SimilarTicketRequest(BaseModel):
    
    query:      str
    top_k:      int        = 5
    department: str | None = None
    tenant:     str | None = None
    exclude_id: int | None = None  
