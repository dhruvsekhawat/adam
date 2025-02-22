from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from config.config import get_settings
import uvicorn
from app.routers import auth, assistant
from app.models.user import Base
from app.db.database import engine
from google.cloud import aiplatform
import os

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize Vertex AI
try:
    aiplatform.init(
        project=settings.GOOGLE_CLOUD_PROJECT,
        location=settings.GOOGLE_CLOUD_LOCATION
    )
except Exception as e:
    print(f"Warning: Could not initialize Vertex AI: {e}")

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_TITLE,
    description="AI-driven executive assistant API",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

# Include routers
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(assistant.router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    """Root endpoint that redirects to docs"""
    return {
        "message": "Welcome to Adam AI API",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "health_check": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and Docker healthcheck"""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "adam-ai-backend",
            "version": settings.VERSION,
            "environment": settings.ENV,
            "vertex_ai_status": "initialized" if aiplatform._has_been_initialized else "not_initialized"
        }
    )

@app.get(f"{settings.API_PREFIX}/status")
async def api_status():
    """API status endpoint"""
    return {
        "status": "operational",
        "version": settings.VERSION,
        "environment": settings.ENV,
        "features": {
            "auth": True,
            "email_processing": True,
            "rag": True,
            "style_analysis": True
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 