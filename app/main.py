from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.routes.tickets    import router as ticket_router
from app.api.routes.incidents  import router as incident_router
from app.api.routes.knowledge  import router as knowledge_router
from app.api.routes.evaluation import router as evaluation_router
from app.core.startup          import load_ticket_embeddings


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_ticket_embeddings()
    yield


app = FastAPI(
    title="AI Helpdesk Infrastructure",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ticket_router,    prefix="/tickets",    tags=["Tickets"])
app.include_router(incident_router,  prefix="/incidents",  tags=["Incidents"])
app.include_router(knowledge_router, prefix="/knowledge",  tags=["Knowledge"])
app.include_router(evaluation_router,prefix="/evaluation", tags=["Evaluation"])


@app.get("/health")
async def health():
    return {"status": "ok"}
