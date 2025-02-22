from sqlalchemy import Column, Integer, String, DateTime, Boolean, text
from sqlalchemy.dialects.postgresql import JSON
from app.db.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    google_id = Column(String, unique=True, index=True)
    access_token = Column(String)
    refresh_token = Column(String)
    token_expires = Column(DateTime)
    created_at = Column(
        DateTime(timezone=True),
        server_default=text('CURRENT_TIMESTAMP'),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP'),
        nullable=False
    )
    
    # Relationships
    integrations = relationship("Integration", back_populates="user", cascade="all, delete-orphan")
    document_chunks = relationship("DocumentChunk", back_populates="user", cascade="all, delete-orphan")
    email_metadata = relationship("EmailMetadata", back_populates="user", cascade="all, delete-orphan")
    
    # User preferences and settings
    preferences = Column(JSON, default=dict)  # Store user preferences (e.g., communication style) 