from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from backend.database import get_db
from backend.models import User
from sqlalchemy.orm import Session
import bcrypt, jwt

router = APIRouter()
SECRET = "tubonge-secret"

@router.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not bcrypt.checkpw(form.password.encode(), user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"id": user.id, "role": user.role}, SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
