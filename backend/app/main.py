from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from config.config import get_settings
import uvicorn

settings = get_settings()

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
            "environment": settings.ENV
        }
    )

@app.get(f"{settings.API_PREFIX}/status")
async def api_status():
    """API status endpoint"""
    return {
        "status": "operational",
        "version": settings.VERSION,
        "environment": settings.ENV
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 