from typing import Dict, List, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import base64
import logging

logger = logging.getLogger(__name__)

class GmailService:
    def __init__(self, credentials: Dict[str, str]):
        """Initialize Gmail service with OAuth2 credentials."""
        self.creds = Credentials(
            token=credentials.get('access_token'),
            refresh_token=credentials.get('refresh_token'),
            client_id=None,  # Not needed for token-only usage
            client_secret=None,  # Not needed for token-only usage
            token_uri="https://oauth2.googleapis.com/token",
        )
        self.service = build('gmail', 'v1', credentials=self.creds)
    
    async def fetch_recent_emails(self, max_results: int = 100) -> List[Dict]:
        """Fetch recent emails from Gmail."""
        try:
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results,
                labelIds=['INBOX']
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                
                # Extract email data
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '')
                sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), '')
                recipients = next((h['value'] for h in headers if h['name'].lower() == 'to'), '').split(',')
                
                # Get email body
                parts = [msg['payload']]
                content = []
                
                while parts:
                    part = parts.pop()
                    if part.get('parts'):
                        parts.extend(part['parts'])
                    if part.get('mimeType') == 'text/plain':
                        data = part.get('body', {}).get('data', '')
                        if data:
                            content.append(base64.urlsafe_b64decode(data).decode())
                
                email_data = {
                    'id': msg['id'],
                    'threadId': msg['threadId'],
                    'subject': subject,
                    'sender': sender,
                    'recipients': recipients,
                    'content': '\n'.join(content),
                    'timestamp': int(msg['internalDate']),
                    'labels': msg['labelIds']
                }
                
                emails.append(email_data)
            
            return emails
            
        except Exception as e:
            logger.error(f"Error fetching emails: {str(e)}")
            raise 