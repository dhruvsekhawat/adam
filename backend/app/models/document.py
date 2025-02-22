from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base, Vector
from datetime import datetime

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    source_type = Column(String, nullable=False)  # 'email', 'drive', 'calendar'
    source_id = Column(String, nullable=False)    # Original document ID (e.g., email ID)
    chunk_index = Column(Integer, nullable=False) # Position in the original document
    content = Column(Text, nullable=False)        # The actual text chunk
    chunk_metadata = Column(JSON)                 # Additional metadata (subject, sender, etc.)
    embedding = Column(Vector(1536))             # Vector embedding (using 1536 for Vertex AI's dimension)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="document_chunks")
    
    class Config:
        indexes = [
            ("embedding", "vector_l2_ops")  # Index for vector similarity search
        ]

class EmailMetadata(Base):
    __tablename__ = "email_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email_id = Column(String, unique=True, nullable=False)
    thread_id = Column(String)
    subject = Column(String)
    sender = Column(String)
    recipients = Column(JSON)  # List of recipients
    timestamp = Column(DateTime)
    labels = Column(JSON)      # Gmail labels
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="email_metadata") 