from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import settings
from models import create_tables
from routes import decisions, reflections, replay, insights, daily

app = FastAPI(
    title="JARVIS – Decision Intelligence System",
    description="AI-powered 4-layer cognitive architecture for personal decision intelligence.",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()


# Register routers
app.include_router(decisions.router)
app.include_router(reflections.router)
app.include_router(replay.router)
app.include_router(insights.router)
app.include_router(daily.router)


@app.get("/", tags=["health"])
def root():
    return {
        "system": "JARVIS",
        "status": "online",
        "layers": [
            "Decision Capture",
            "Reflection Engine",
            "Pattern Intelligence",
            "Daily Guidance",
        ],
    }


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}
