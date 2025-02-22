from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.document import DocumentChunk
from app.services.vertex import VertexAIService
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, db: Session, vertex_service: VertexAIService):
        self.db = db
        self.vertex_service = vertex_service
        self.default_k = 5  # Number of relevant chunks to retrieve
    
    async def query(
        self,
        user_id: int,
        query: str,
        k: int = None,
        time_window_days: Optional[int] = None,
        source_type: Optional[str] = None
    ) -> str:
        """
        Process a query using RAG:
        1. Generate query embedding
        2. Retrieve relevant chunks
        3. Generate response using context
        """
        try:
            k = k or self.default_k
            
            # Generate query embedding
            query_embedding = (await self.vertex_service.generate_embeddings([query]))[0]
            
            # Retrieve relevant chunks
            relevant_chunks = await self._retrieve_relevant_chunks(
                user_id,
                query_embedding,
                k,
                time_window_days,
                source_type
            )
            
            # Extract context from chunks
            context = [chunk.content for chunk in relevant_chunks]
            
            # Generate response
            response = await self.vertex_service.generate_response(
                prompt=query,
                context=context
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error in RAG query: {str(e)}")
            raise
    
    async def _retrieve_relevant_chunks(
        self,
        user_id: int,
        query_embedding: np.ndarray,
        k: int,
        time_window_days: Optional[int] = None,
        source_type: Optional[str] = None
    ) -> List[DocumentChunk]:
        """Retrieve the most relevant document chunks using vector similarity."""
        try:
            # Construct the base query
            base_query = """
            SELECT id, content, metadata, source_type, source_id,
                   embedding <-> :query_embedding AS distance
            FROM document_chunks
            WHERE user_id = :user_id
            """
            
            # Add optional filters
            if time_window_days:
                cutoff_date = datetime.utcnow() - timedelta(days=time_window_days)
                base_query += " AND created_at >= :cutoff_date"
            
            if source_type:
                base_query += " AND source_type = :source_type"
            
            # Add ordering and limit
            base_query += """
            ORDER BY distance
            LIMIT :k
            """
            
            # Execute the query
            params = {
                "user_id": user_id,
                "query_embedding": query_embedding.tolist(),
                "k": k,
                "cutoff_date": cutoff_date if time_window_days else None,
                "source_type": source_type
            }
            
            result = self.db.execute(text(base_query), params)
            chunk_ids = [row.id for row in result]
            
            # Fetch the actual DocumentChunk objects
            chunks = self.db.query(DocumentChunk).filter(
                DocumentChunk.id.in_(chunk_ids)
            ).all()
            
            # Sort chunks to maintain the order from the similarity search
            id_to_chunk = {chunk.id: chunk for chunk in chunks}
            sorted_chunks = [id_to_chunk[id_] for id_ in chunk_ids]
            
            return sorted_chunks
            
        except Exception as e:
            logger.error(f"Error retrieving relevant chunks: {str(e)}")
            raise
    
    async def analyze_user_style(self, user_id: int) -> Dict:
        """Analyze the user's writing style from their emails."""
        try:
            # Fetch recent email chunks
            chunks = self.db.query(DocumentChunk).filter(
                DocumentChunk.user_id == user_id,
                DocumentChunk.source_type == 'email'
            ).order_by(
                DocumentChunk.created_at.desc()
            ).limit(50).all()
            
            if not chunks:
                return {"error": "No email data available for analysis"}
            
            # Extract content from chunks
            texts = [chunk.content for chunk in chunks]
            
            # Analyze writing style
            style_analysis = await self.vertex_service.analyze_writing_style(texts)
            
            return style_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing user style: {str(e)}")
            raise 