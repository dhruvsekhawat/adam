from typing import List, Dict, Optional
from datetime import datetime
import re
from sqlalchemy.orm import Session
from app.models.document import DocumentChunk, EmailMetadata
from app.services.vertex import VertexAIService
from app.services.gmail import GmailService
import json
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class EmailProcessor:
    def __init__(self, db: Session, vertex_service: VertexAIService):
        self.db = db
        self.vertex_service = vertex_service
        self.chunk_size = 500
        self.chunk_overlap = 50
    
    async def process_emails(
        self,
        user_id: int,
        gmail_service: GmailService,
        max_emails: int = 100
    ) -> List[Dict]:
        """Process recent emails for a user."""
        try:
            # Fetch recent emails
            emails = await gmail_service.fetch_recent_emails(max_results=max_emails)
            processed_emails = []
            
            for email in emails:
                try:
                    # Store email metadata
                    metadata = await self._store_email_metadata(user_id, email)
                    
                    # Process email content
                    if not metadata.is_processed:
                        chunks = await self._process_email_content(user_id, email)
                        processed_emails.extend(chunks)
                        
                        # Mark email as processed
                        metadata.is_processed = True
                        self.db.commit()
                
                except Exception as e:
                    logger.error(f"Error processing email {email.get('id')}: {str(e)}")
                    continue
            
            return processed_emails
        
        except Exception as e:
            logger.error(f"Error in process_emails: {str(e)}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _store_email_metadata(self, user_id: int, email: Dict) -> EmailMetadata:
        """Store email metadata in the database."""
        try:
            metadata = EmailMetadata(
                user_id=user_id,
                email_id=email['id'],
                thread_id=email.get('threadId'),
                subject=email.get('subject'),
                sender=email.get('sender'),
                recipients=email.get('recipients', []),
                timestamp=datetime.fromtimestamp(int(email['timestamp']) / 1000),
                labels=email.get('labels', [])
            )
            
            self.db.add(metadata)
            self.db.commit()
            self.db.refresh(metadata)
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error storing email metadata: {str(e)}")
            raise
    
    async def _process_email_content(self, user_id: int, email: Dict) -> List[Dict]:
        """Process email content into chunks and store with embeddings."""
        try:
            # Clean and chunk the content
            content = email.get('content', '')
            chunks = self._chunk_text(content)
            
            # Generate embeddings for all chunks
            embeddings = await self.vertex_service.generate_embeddings(chunks)
            
            stored_chunks = []
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_doc = DocumentChunk(
                    user_id=user_id,
                    source_type='email',
                    source_id=email['id'],
                    chunk_index=idx,
                    content=chunk,
                    chunk_metadata={
                        'subject': email.get('subject'),
                        'sender': email.get('sender'),
                        'timestamp': email.get('timestamp'),
                        'thread_id': email.get('threadId')
                    },
                    embedding=embedding.tolist()
                )
                
                self.db.add(chunk_doc)
                stored_chunks.append(chunk_doc)
            
            self.db.commit()
            return stored_chunks
            
        except Exception as e:
            logger.error(f"Error processing email content: {str(e)}")
            raise
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap."""
        # Clean text
        text = self._clean_text(text)
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            if current_length + sentence_length > self.chunk_size:
                # Store current chunk
                chunks.append(' '.join(current_chunk))
                
                # Start new chunk with overlap
                overlap_tokens = current_chunk[-self.chunk_overlap:] if self.chunk_overlap > 0 else []
                current_chunk = overlap_tokens + [sentence]
                current_length = sum(len(t) for t in current_chunk)
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Clean email text content."""
        # Remove email signatures
        text = re.sub(r'--\s*\n.*', '', text, flags=re.DOTALL)
        
        # Remove quoted text
        text = re.sub(r'On.*wrote:.*', '', text, flags=re.DOTALL)
        text = re.sub(r'>\s*>.*', '', text, flags=re.DOTALL)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip() 