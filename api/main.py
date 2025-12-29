"""FastAPI application for bot detection."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from api.routes import router
from api.monitoring import router as monitoring_router

# Create FastAPI app
app = FastAPI(
    title="ConsensusWatch API",
    description="Detect synthetic consensus and coordinated narrative steering in Reddit threads",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routes
app.include_router(router, prefix="/api/v1")
app.include_router(monitoring_router, prefix="/api/v1", tags=["monitoring"])


@app.on_event("startup")
async def startup_event() -> None:
    """Run on application startup."""
    print("ConsensusWatch API starting...")
    print("Docs available at: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Run on application shutdown."""
    print("ConsensusWatch API shutting down...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
