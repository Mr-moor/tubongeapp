# backend/admin/routers.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.users.models import User  # same User model
from backend.users.utils import hash_password
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])

# Admin registration schema
class AdminCreate(BaseModel):
    full_name: str
    email: str
    username: str
    phone: str
    password: str
    secret_code: str  # only allow registration if correct

SECRET_ADMIN_CODE = "tubonge_admin_2025"

@router.post("/register", status_code=201)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    # Check secret code
    if admin.secret_code != SECRET_ADMIN_CODE:
        raise HTTPException(status_code=401, detail="Invalid secret code")

    # Check if email or username exists
    existing = db.query(User).filter((User.email == admin.email) | (User.username == admin.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email or username already exists")
    
    new_admin = User(
        full_name=admin.full_name,
        email=admin.email,
        username=admin.username,
        phone=admin.phone,
        password_hash=hash_password(admin.password)
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"message": "Admin registered successfully", "username": new_admin.username}
