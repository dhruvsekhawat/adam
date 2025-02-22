from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from typing import List, Dict, Optional
import numpy as np
from config.config import get_settings
import json
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class VertexAIService:
    def __init__(self):
        aiplatform.init(
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.GOOGLE_CLOUD_LOCATION
        )
        self.embedding_model = "textembedding-gecko@latest"
        self.llm_model = "gemini-pro"
        
    async def generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for a list of texts using Vertex AI."""
        try:
            model = aiplatform.TextEmbeddingModel.from_pretrained(self.embedding_model)
            embeddings = model.get_embeddings(texts)
            return [np.array(embedding.values) for embedding in embeddings]
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    async def generate_response(
        self,
        prompt: str,
        context: Optional[List[str]] = None,
        temperature: float = 0.7
    ) -> str:
        """Generate a response using Vertex AI's Gemini model."""
        try:
            model = aiplatform.GenerativeModel.from_pretrained(self.llm_model)
            
            # Construct the prompt with context if provided
            if context:
                context_str = "\n".join(context)
                full_prompt = f"""Context:
                {context_str}
                
                Based on the above context, please respond to:
                {prompt}
                """
            else:
                full_prompt = prompt
            
            response = model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": temperature,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 1024,
                }
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
    async def analyze_writing_style(self, texts: List[str]) -> Dict:
        """Analyze writing style using Vertex AI."""
        try:
            model = aiplatform.GenerativeModel.from_pretrained(self.llm_model)
            
            analysis_prompt = f"""Analyze the writing style in the following texts and extract key characteristics:
            
            Texts:
            {json.dumps(texts)}
            
            Please analyze:
            1. Tone (formal, casual, professional, etc.)
            2. Common phrases or expressions
            3. Typical greeting and sign-off styles
            4. Vocabulary preferences
            5. Sentence structure patterns
            
            Return the analysis in JSON format."""
            
            response = model.generate_content(analysis_prompt)
            
            # Parse the JSON response
            try:
                style_analysis = json.loads(response.text)
            except json.JSONDecodeError:
                logger.warning("Could not parse style analysis as JSON")
                style_analysis = {"raw_analysis": response.text}
            
            return style_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing writing style: {str(e)}")
            raise 