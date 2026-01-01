from sqlalchemy.orm import Session
from backend import models

def get_user_by_email_or_username(db: Session, identifier: str):
    return db.query(models.User).filter((models.User.email==identifier)|(models.User.username==identifier)).first()

def create_user(db: Session, username: str, email: str, password_hash: str, role: str='user'):
    u = models.User(username=username, email=email, password_hash=password_hash, role=role)
    db.add(u); db.commit(); db.refresh(u)
    return u

def create_post(db: Session, author_id: int, media_type: str, content_text: str=None, media_url: str=None):
    p = models.Post(author_id=author_id, media_type=media_type, content_text=content_text, media_url=media_url)
    db.add(p); db.commit(); db.refresh(p)
    return p
