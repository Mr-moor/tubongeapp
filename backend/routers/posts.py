from fastapi import APIRouter, Depends, Form
from backend.database import get_db
from backend.auth import get_current_user, require_admin
from backend import crud, models

router = APIRouter()

@router.post('/')
def create_post(media_type: str = Form(...), content_text: str = Form(None), media_url: str = Form(None), current_user = Depends(get_current_user), db=Depends(get_db)):
    p = crud.create_post(db, current_user.id, media_type, content_text, media_url)
    return {'id': p.id}

@router.get('/feed')
def feed(page: int = 1, per_page: int = 20, db=Depends(get_db)):
    q = db.query(models.Post).filter(models.Post.is_hidden==False).order_by(models.Post.created_at.desc()).offset((page-1)*per_page).limit(per_page).all()
    return q

@router.post('/{post_id}/flag')
def flag(post_id: int, flag: str = Form(...), reason: str = Form(None), current_user = Depends(get_current_user), db=Depends(get_db)):
    existing = db.query(models.Flag).filter(models.Flag.post_id==post_id, models.Flag.user_id==current_user.id).first()
    if existing:
        existing.flag = flag; existing.reason = reason; db.commit()
    else:
        f = models.Flag(post_id=post_id, user_id=current_user.id, flag=flag, reason=reason); db.add(f); db.commit()
    red_count = db.query(models.Flag).filter(models.Flag.post_id==post_id, models.Flag.flag=='red').count()
    if red_count >= 3:
        p = db.query(models.Post).get(post_id); p.is_hidden = True; db.commit()
    return {'msg':'flag recorded'}

@router.post("/")
def create_post(data: dict, db: Session = Depends(get_db)):
    post = Post(content=data["content"])
    db.add(post)
    db.commit()
    return post

@router.post("/{post_id}/like")
def like_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    post.likes += 1
    db.commit()
    return post
