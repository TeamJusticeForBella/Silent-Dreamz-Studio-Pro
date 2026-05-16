from contextlib import asynccontextmanager
from fastapi import FastAPI
from .core.clients import close_nats, connect_nats
from .routers import citations, drafts, evidence, exports, health, incidents, packets, search
from .services.nats_jobs import ensure_stream


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_nats()
    await ensure_stream()
    yield
    await close_nats()


app = FastAPI(title="Bella Command Center API", version="0.1.0", root_path="/api", lifespan=lifespan)
app.include_router(health.router)
app.include_router(evidence.router)
app.include_router(incidents.router)
app.include_router(packets.router)
app.include_router(drafts.router)
app.include_router(citations.router)
app.include_router(exports.router)
app.include_router(search.router)
