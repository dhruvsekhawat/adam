from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from authlib.integrations.starlette_client import OAuth
from app.db.database import get_db
from app.models.user import User
from config.config import get_settings
import jwt
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

settings = get_settings()
security = HTTPBearer()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Configure OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@router.get("/me")
async def get_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active
    }

@router.get("/login/google")
async def google_login(request: Request):
    """Redirect to Google OAuth2 login"""
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Google OAuth2 callback"""
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not fetch user info from Google"
            )
        
        # Check if user exists
        user = db.query(User).filter(User.email == user_info['email']).first()
        
        if not user:
            # Create new user
            user = User(
                email=user_info['email'],
                full_name=user_info.get('name'),
                google_id=user_info['sub'],
                is_active=True
            )
            db.add(user)
        
        # Update tokens
        user.access_token = token['access_token']
        user.token_expires = datetime.fromtimestamp(token['expires_at'])
        db.commit()
        
        # Create JWT token
        access_token = create_access_token(
            data={"sub": user.email}
        )
        
        # Redirect to frontend with token
        frontend_url = settings.BACKEND_CORS_ORIGINS[0]
        redirect_url = f"{frontend_url}/auth/callback?token={access_token}"
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 