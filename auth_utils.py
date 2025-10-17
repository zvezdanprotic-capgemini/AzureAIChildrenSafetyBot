import os
import datetime as dt
import jwt
try:
    from passlib.context import CryptContext
except ImportError as e:
    raise ImportError("passlib is required. Ensure 'pip install passlib bcrypt' succeeded.") from e
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = os.getenv('JWT_SECRET', 'dev-secret-change')
JWT_ALG = 'HS256'
JWT_EXPIRE_MINUTES = int(os.getenv('JWT_EXPIRE_MINUTES', '60'))


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_token(user_id: int, username: str, age: int | None) -> str:
    now = dt.datetime.utcnow()
    payload = {
        'sub': str(user_id),
        'username': username,
        'age': age,
        'iat': now,
        'exp': now + dt.timedelta(minutes=JWT_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except jwt.PyJWTError:
        return None
