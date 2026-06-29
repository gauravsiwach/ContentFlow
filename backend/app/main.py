import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db
from app.shared.storage import ensure_storage_dirs
from app.shared.exceptions import ContentFlowError

# Configure logging
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=settings.LOG_LEVEL,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting ContentFlow backend...")
    init_db()
    ensure_storage_dirs()
    logger.info("Database and storage initialized successfully")
    yield
    # Shutdown
    logger.info("Shutting down ContentFlow backend...")


# Create FastAPI app
app = FastAPI(
    title="ContentFlow API",
    description="AI-powered content creation platform",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(ContentFlowError)
async def contentflow_error_handler(request: Request, exc: ContentFlowError):
    """Handle ContentFlow custom exceptions."""
    logger.error(f"ContentFlow error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "type": type(exc).__name__},
    )


# Health check endpoint
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "database": "connected",
        "storage": "ready",
    }


# Register routers
from app.modules.project.router import router as project_router
from app.modules.script.router import router as script_router
from app.modules.scene.router import router as scene_router
app.include_router(project_router, prefix="/api/v1", tags=["projects"])
app.include_router(script_router, prefix="/api/v1/projects", tags=["scripts"])
app.include_router(scene_router, prefix="/api/v1/projects", tags=["scenes"])
