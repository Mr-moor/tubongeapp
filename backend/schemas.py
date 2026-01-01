from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PostCreate(BaseModel):
    title: Optional[str]
    content: str
    media_type: Optional[str]
    media_url: Optional[str]

class PostResponse(BaseModel):
    id: int
    owner_id: int
    title: Optional[str]
    content: str
    media_type: Optional[str]
    media_url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    post_id: int
    content: str

class ShareCreate(BaseModel):
    post_id: int
    edited_content: Optional[str]

class FlagCreate(BaseModel):
    post_id: int
    status: str  # "red" or "green"

class SubscriptionCreate(BaseModel):
    followed_id: int

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    username: str
    phone: str
    password: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    username: str
    phone: str

    class Config:
        orm_mode = True
