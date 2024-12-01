import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from uuid import UUID
from typing import Set

# Конфигурация токенов
SECRET_KEY = "your_secret_key"  # Замените на ваш секретный ключ
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Для схемы OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Чёрный список токенов
BLACKLISTED_TOKENS: Set[str] = set()

# Модель токена
class Token(BaseModel):
    access_token: str
    token_type: str

# Модель данных токена
class TokenData(BaseModel):
    user_id: UUID
    role: str
    exp: datetime

# Функция создания токена
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Функция проверки токена
def decode_access_token(token: str):
    if token in BLACKLISTED_TOKENS:
        raise HTTPException(status_code=401, detail="Token is blacklisted")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Функция добавления токена в черный список
def blacklist_token(token: str):
    BLACKLISTED_TOKENS.add(token)
