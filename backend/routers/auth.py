from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from backend import crud, schemas
from backend.database import get_db
from backend.auth import hash_password, verify_password, create_token

router = APIRouter()

@router.post('/token')
def token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = crud.get_user_by_email_or_username(db, form_data.username)
    if not user or not verify_password(user.password_hash, form_data.password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_token({'id': user.id, 'username': user.username, 'role': user.role})
    return {'access_token': token, 'token_type': 'bearer'}

@router.post('/register')
def register(u: schemas.UserCreate, db=Depends(get_db)):
    existing = crud.get_user_by_email_or_username(db, u.email)
    if existing:
        raise HTTPException(status_code=400, detail='User exists')
    hashed = hash_password(u.password)
    user = crud.create_user(db, u.username, u.email, hashed)
    return {'id': user.id}
