from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv
from typing import List

# Determine the environment
ENV = os.getenv("ENV", "development")
env_path = os.path.join(os.path.dirname(__file__), f".env.{ENV}")
load_dotenv(env_path)

class Settings(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_TITLE: str = "Adam AI Backend"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Database
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "adam_ai")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-development")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI")
    
    # Google Cloud & Vertex AI
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT")
    GOOGLE_CLOUD_LOCATION: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # Email Processing
    MAX_EMAILS_PER_BATCH: int = 100
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    
    # Vector Search
    VECTOR_SIMILARITY_METRIC: str = "cosine"
    DEFAULT_SEARCH_K: int = 5
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Vertex AI Models
    VERTEX_EMBEDDING_MODEL: str = "textembedding-gecko@latest"
    VERTEX_LLM_MODEL: str = "gemini-pro"
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings() 