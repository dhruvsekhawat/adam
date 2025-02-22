from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from config.config import get_settings
import sqlalchemy as sa
from sqlalchemy.types import UserDefinedType

settings = get_settings()

# PostgreSQL connection URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Configure engine with connection pooling
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True
)

# Enable pgvector extension
def init_vector_db():
    conn = engine.connect()
    conn.execute(sa.text('CREATE EXTENSION IF NOT EXISTS vector;'))
    conn.commit()
    conn.close()

try:
    init_vector_db()
except Exception as e:
    print(f"Warning: Could not initialize vector extension: {e}")

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Custom Vector type for SQLAlchemy
class Vector(UserDefinedType):
    def __init__(self, dim):
        self.dim = dim

    def get_col_spec(self):
        return f"vector({self.dim})"

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process

# Register the vector type
sa.Vector = Vector 