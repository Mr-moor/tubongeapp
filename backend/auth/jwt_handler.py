from datetime import datetime, timedelta
from jose import jwt

SECRET = "SUPER_SECRET_JWT_KEY"
ALGO = "HS256"

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(days=3)
    return jwt.encode(payload, SECRET, algorithm=ALGO)

from jose import  JWTError

SECRET_KEY = "SECRET"
ALGORITHM = "HS256"

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
