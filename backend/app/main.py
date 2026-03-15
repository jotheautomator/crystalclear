"""CrystalClear — Political transparency network analysis platform."""
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_postgres, close_postgres
from app.core.neo4j import init_neo4j, close_neo4j


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown."""
    # Startup
    await init_postgres()
    await init_neo4j()
    yield
    # Shutdown
    await close_postgres()
    await close_neo4j()


app = FastAPI(
    title="CrystalClear API",
    description="Political transparency network analysis platform",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


# Routers will be registered here as they are implemented:
# from app.api import auth, users, entities, declarations, analysis, complaints
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
# ...
