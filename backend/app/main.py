from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db import create_all_tables
from app.middleware.auth import AuthMiddleware
from app.routes import decisions, reflections, replay, insights, daily
from app.tasks.scheduler import start_scheduler, stop_scheduler

app = FastAPI(
    title="JARVIS – Decision Intelligence System",
    description=(
        "AI-powered 4-layer cognitive architecture:\n"
        "1. Decision Capture (Memory)\n"
        "2. Reflection Engine (Learning)\n"
        "3. Pattern Intelligence (Insight)\n"
        "4. Daily Guidance (Cognitive)"
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth middleware
app.add_middleware(AuthMiddleware)

# Startup / shutdown lifecycle
@app.on_event("startup")
async def startup():
    create_all_tables()
    start_scheduler()


@app.on_event("shutdown")
async def shutdown():
    stop_scheduler()


# Routers
app.include_router(decisions.router)
app.include_router(reflections.router)
app.include_router(replay.router)
app.include_router(insights.router)
app.include_router(daily.router)


@app.get("/", tags=["health"])
def root():
    return {
        "system": "JARVIS",
        "version": "2.0.0",
        "status": "online",
        "layers": {
            "memory": "/decisions",
            "learning": "/reflections",
            "recall": "/replay",
            "insight": "/insights",
            "cognitive": "/daily",
        },
    }


@app.get("/health", tags=["health"])
def health():
    return {"status": "healthy"}
