from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, database
from backend.auth.jwt_handler import decode_token

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        user = db.query(models.User).filter(models.User.id == payload["user_id"]).first()
        if not user:
            raise HTTPException(401, "Invalid token")
        return user
    except:
        raise HTTPException(401, "Invalid token")

def admin_required(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin privilege required")
    return current_user
