from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models import User
from auth_utils import hash_password, verify_password, create_token, decode_token
from typing import Optional

# Ensure tables
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/api/auth", tags=["auth"])

class RegisterReq(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)
    age: Optional[int] = Field(None, ge=1, le=120)

class LoginReq(BaseModel):
    username: str
    password: str

class TokenResp(BaseModel):
    access_token: str
    token_type: str = "bearer"


def get_current_user(token: Optional[str]) -> Optional[dict]:
    if not token:
        return None
    return decode_token(token)

@router.post('/register', response_model=TokenResp)
def register(data: RegisterReq, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=data.username, password_hash=hash_password(data.password), age=data.age)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token(user.id, user.username, user.age)
    return TokenResp(access_token=token)

@router.post('/login', response_model=TokenResp)
def login(data: LoginReq, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_token(user.id, user.username, user.age)
    return TokenResp(access_token=token)

@router.get('/me')
def me(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail='Not authenticated')
    token = authorization.split()[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid token')
    return {
        'username': payload['username'],
        'age': payload.get('age'),
        'user_id': payload['sub']
    }

@router.post('/logout')
def logout(authorization: Optional[str] = Header(default=None)):
    """Logout endpoint - primarily for frontend to call during logout process."""
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail='Not authenticated')
    token = authorization.split()[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    # For now, we just confirm the token is valid
    # In a production system, you might add the token to a blacklist
    return {
        'message': 'Successfully logged out',
        'username': payload['username']
    }
