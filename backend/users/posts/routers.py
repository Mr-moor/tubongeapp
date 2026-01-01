from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import database, models
from backend.auth.jwt_handler import decode_token
from backend.schemas import PostCreate, PostResponse, CommentCreate, ShareCreate, FlagCreate, SubscriptionCreate

router = APIRouter(prefix="/posts", tags=["posts"])

# DB Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mock Auth dependency: pass token in headers for simplicity
def get_current_user(token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        user = db.query(models.User).filter(models.User.id == payload["user_id"]).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# Create Post
@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# View all posts
@router.get("/", response_model=list[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

# Like a post
@router.post("/{post_id}/like")
def like_post(post_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    like = models.Like(user_id=current_user.id, post_id=post_id)
    db.add(like)
    db.commit()
    return {"message": "Post liked"}

# Comment on a post
@router.post("/comment")
def comment_post(comment: CommentCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    db_comment = models.Comment(user_id=current_user.id, post_id=comment.post_id, content=comment.content)
    db.add(db_comment)
    db.commit()
    return {"message": "Comment added"}

# Share a post
@router.post("/share")
def share_post(share: ShareCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == share.post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    db_share = models.Share(user_id=current_user.id, post_id=share.post_id, edited_content=share.edited_content)
    db.add(db_share)
    db.commit()
    return {"message": "Post shared"}

# Flag a post
@router.post("/flag")
def flag_post(flag: FlagCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == flag.post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    db_flag = models.Flag(user_id=current_user.id, post_id=flag.post_id, status=flag.status)
    db.add(db_flag)
    db.commit()
    return {"message": f"Post flagged {flag.status}"}

# Subscribe to a user
@router.post("/subscribe")
def subscribe(subscription: SubscriptionCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_sub = models.Subscription(follower_id=current_user.id, followed_id=subscription.followed_id)
    db.add(db_sub)
    db.commit()
    return {"message": "Subscribed successfully"}

from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
import shutil
from backend.config import UPLOAD_DIR
import uuid

# Upload media for a post
@router.post("/upload/{post_id}")
def upload_media(post_id: int, file: UploadFile = File(...), current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.owner_id == current_user.id).first()
    if not post:
        raise HTTPException(404, "Post not found or you don't own it")

    # Create unique filename
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update post with media info
    post.media_url = file_path
    post.media_type = file.content_type.split("/")[0]  # video, image, audio
    db.commit()
    db.refresh(post)

    return {"message": "Media uploaded successfully", "media_url": post.media_url, "media_type": post.media_type}

@router.post("/live/start")
def start_live(title: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    import secrets
    # Generate a unique streaming URL (mock)
    stream_url = f"http://127.0.0.1:8000/live/{secrets.token_hex(8)}"
    live_session = models.LiveSession(user_id=current_user.id, title=title, stream_url=stream_url)
    db.add(live_session)
    db.commit()
    db.refresh(live_session)
    return {"message": "Live session started", "stream_url": live_session.stream_url, "title": live_session.title}

@router.post("/live/end/{live_id}")
def end_live(live_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(models.LiveSession).filter(models.LiveSession.id == live_id, models.LiveSession.user_id == current_user.id).first()
    if not session:
        raise HTTPException(404, "Live session not found or you are not the owner")
    session.is_active = False
    db.commit()
    return {"message": "Live session ended"}

from backend.dependencies import admin_required

# Admin deletes a post
@router.delete("/admin/delete/{post_id}")
def admin_delete_post(post_id: int, admin: models.User = Depends(admin_required), db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted by admin"}

from fastapi import APIRouter, Depends
from backend.database import get_db
from backend.models import User
from sqlalchemy.orm import Session
import bcrypt

router = APIRouter()

@router.post("/register")
def register_user(data: dict, db: Session = Depends(get_db)):
    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
    user = User(username=data["username"], email=data["email"],
                password=hashed, role="user")
    db.add(user)
    db.commit()
    return {"message": "User created"}

@router.post("/admin/register")
def register_admin(data: dict, db: Session = Depends(get_db)):
    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
    admin = User(username=data["username"], password=hashed, role="admin")
    db.add(admin)
    db.commit()
    return {"message": "Admin created"}

@router.get("/me")
def profile(user=Depends(get_current_user)):
    return user

@router.put("/me")
def update_profile(data: dict, db: Session = Depends(get_db),
                   user=Depends(get_current_user)):
    user.email = data["email"]
    db.commit()
    return {"status": "updated"}

@app.delete("/admin/posts/{id}")
def delete_post(id: int, user=Depends(admin_only)):
    db.query(Post).filter(Post.id == id).delete()
    db.commit()

@app.post("/admin/ban/{user_id}")
def ban_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    user.is_active = False
    db.commit()
