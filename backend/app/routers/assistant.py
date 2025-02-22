from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user
from app.services.gmail import GmailService
from app.services.email_processor import EmailProcessor
from app.services.rag import RAGService
from app.services.vertex import VertexAIService
from typing import Dict, List, Optional
from pydantic import BaseModel

router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"]
)

class QueryRequest(BaseModel):
    query: str
    time_window_days: Optional[int] = None
    source_type: Optional[str] = None

class ProcessEmailsRequest(BaseModel):
    max_emails: Optional[int] = 100

@router.post("/process-emails")
async def process_emails(
    request: ProcessEmailsRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process user's emails in the background."""
    try:
        # Initialize services
        vertex_service = VertexAIService()
        gmail_service = GmailService({
            'access_token': current_user.access_token,
            'refresh_token': current_user.refresh_token
        })
        email_processor = EmailProcessor(db, vertex_service)
        
        # Add email processing to background tasks
        background_tasks.add_task(
            email_processor.process_emails,
            current_user.id,
            gmail_service,
            request.max_emails
        )
        
        return {
            "message": "Email processing started",
            "status": "processing"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error starting email processing: {str(e)}"
        )

@router.post("/query")
async def query_assistant(
    request: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Query the assistant using RAG."""
    try:
        # Initialize services
        vertex_service = VertexAIService()
        rag_service = RAGService(db, vertex_service)
        
        # Process query
        response = await rag_service.query(
            user_id=current_user.id,
            query=request.query,
            time_window_days=request.time_window_days,
            source_type=request.source_type
        )
        
        return {
            "response": response
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@router.get("/analyze-style")
async def analyze_writing_style(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze the user's writing style."""
    try:
        # Initialize services
        vertex_service = VertexAIService()
        rag_service = RAGService(db, vertex_service)
        
        # Analyze style
        style_analysis = await rag_service.analyze_user_style(current_user.id)
        
        return style_analysis
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing writing style: {str(e)}"
        ) 