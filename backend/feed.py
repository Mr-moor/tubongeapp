from sqlalchemy.orm import Session
from backend.models.content import Content
from backend.models.engagement import Engagement
from backend.models.user import User

def calculate_score(content, engagement):
    return (
        engagement.watch_time * 3 +
        engagement.liked * 2 +
        engagement.shared * 3 +
        engagement.saved * 4
    )

def build_for_you_feed(db: Session, user_id: int, limit=20):
    contents = db.query(Content).filter(
        Content.visibility == "public"
    ).all()

    feed = []

    for c in contents:
        e = db.query(Engagement).filter_by(
            user_id=user_id,
            content_id=c.id
        ).first()

        score = calculate_score(c, e) if e else 0
        feed.append((c, score))

    feed.sort(key=lambda x: x[1], reverse=True)
    return [c for c, _ in feed[:limit]]
