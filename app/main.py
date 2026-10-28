"""
Main Application Entrypoint — Next-Generation Digital Banking Platform.
FastAPI Microservices Core, FAPI Token Gateway & Static UI Mount.
"""

from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.db.init_db import init_database
from app.api.auth import router as auth_router
from app.api.accounts import router as accounts_router
from app.api.transfers import router as transfers_router
from app.api.cards import router as cards_router
from app.api.sme import router as sme_router
from app.api.approvals import router as approvals_router
from app.api.fraud import router as fraud_router
from app.api.audit import router as audit_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Database on Startup
    init_database()
    yield

app = FastAPI(
    title="Next-Generation Digital Banking Platform",
    description="Cloud-Native Microservices Core, Double-Entry Ledger & Multi-Rail Payment Orchestration",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS Middleware for modern client integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check Probe
@app.get("/health", tags=["System"])
def health_check():
    """Readiness and liveness probe for container orchestrator."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


# Mount REST API Routers under /api/v1
app.include_router(auth_router, prefix="/api/v1")
app.include_router(accounts_router, prefix="/api/v1")
app.include_router(transfers_router, prefix="/api/v1")
app.include_router(cards_router, prefix="/api/v1")
app.include_router(sme_router, prefix="/api/v1")
app.include_router(approvals_router, prefix="/api/v1")
app.include_router(fraud_router, prefix="/api/v1")
app.include_router(audit_router, prefix="/api/v1")


# RFC-7807 Error Handling
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "type": "https://api.apexbank.com/errors/internal-server-error",
            "title": "Internal Server Error",
            "status": 500,
            "detail": str(exc),
            "instance": str(request.url)
        }
    )

# Static UI Serving Strategy: Mount public directory at root
base_dir = Path(__file__).resolve().parent.parent
public_dir = base_dir / "public"
pages_dir = public_dir / "pages"

if pages_dir.exists():
    app.mount("/pages", StaticFiles(directory=str(pages_dir), html=True), name="pages")

if public_dir.exists():
    app.mount("/", StaticFiles(directory=str(public_dir), html=True), name="public")
