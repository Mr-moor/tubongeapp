from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Message

router = APIRouter()

@router.post("/")
def send_message(data: dict, db: Session = Depends(get_db)):
    msg = Message(**data)
    db.add(msg)
    db.commit()
    return {"status": "sent"}

@router.get("/{user_id}")
def get_messages(user_id: int, db: Session = Depends(get_db)):
    return db.query(Message).filter(
        (Message.sender_id == user_id) |
        (Message.receiver_id == user_id)
    ).all()

@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    return {
        "users": db.query(User).count(),
        "posts": db.query(Post).count(),
        "messages": db.query(Message).count()
    }

from fastapi import UploadFile, File

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"url": path}

@app.post("/mpesa/pay")
def mpesa_pay(data: dict):
    # STK Push placeholder
    return {"status": "Payment request sent"}

import stripe
stripe.api_key = "sk_test_..."

@app.post("/stripe/pay")
def stripe_pay(data: dict):
    intent = stripe.PaymentIntent.create(
        amount=data["amount"],
        currency="usd"
    )
    return {"client_secret": intent.client_secret}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Message

router = APIRouter(prefix="/messages")

@router.get("/{user_id}")
def get_messages(user_id: int, db: Session = Depends(get_db)):
    return db.query(Message).filter(
        (Message.sender_id == user_id) |
        (Message.receiver_id == user_id)
    ).all()

@router.get("/search/{room_id}")
def search(room_id: str, q: str, page: int = 1, db: Session = Depends(get_db)):
    return (
        db.query(Message)
        .filter(Message.room_id == room_id, Message.content.contains(q))
        .offset((page - 1) * 20)
        .limit(20)
        .all()
    )

@router.delete("/recall/{message_id}")
def recall_message(message_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    msg = db.query(Message).get(message_id)
    if msg.sender_id != user.id:
        raise HTTPException(status_code=403, detail="Cannot delete others’ messages")
    db.delete(msg)
    db.commit()
    return {"status": "deleted"}

@router.post("/upload/{room_id}")
async def upload_file(room_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    msg = Message(room_id=room_id, sender_id=current_user.id, content=path)
    db.add(msg)
    db.commit()
    await manager.send_room(room_id, {"type": "media", "url": path})
    return {"url": path}

@router.post("/verify/request")
def request_verification(user=Depends(get_current_user)):
    user.verification_status = "pending"
    db.commit()
    return {"status": "pending"}

@router.get("/feed")
def get_feed(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return build_for_you_feed(db, user.id)
