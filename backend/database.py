from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:DanteBrute254%40@localhost:3306/tubonge"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    is_verified = Column(Boolean, default=False)
    verification_type = Column(String, nullable=True)  # blue, medical, org
    role = Column(String, default="user")  # user, admin, moderator

    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    private_account = Column(Boolean, default=False)
    allow_messages = Column(Boolean, default=True)
    allow_comments = Column(Boolean, default=True)
    allow_tags = Column(Boolean, default=True)
    show_online_status = Column(Boolean, default=True)

    language = Column(String, default="en")

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    type = Column(String)  # post, video, story
    text = Column(Text, nullable=True)
    media_url = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)  # seconds (for video)

    visibility = Column(String, default="public")  # public, followers, private

    created_at = Column(DateTime, default=datetime.utcnow)

class Engagement(Base):
    __tablename__ = "engagement"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    content_id = Column(Integer, ForeignKey("content.id"), primary_key=True)

    liked = Column(Boolean, default=False)
    saved = Column(Boolean, default=False)
    watch_time = Column(Integer, default=0)  # seconds
    shared = Column(Boolean, default=False)

class FeedScore(Base):
    __tablename__ = "feed_scores"

    content_id = Column(Integer, ForeignKey("content.id"), primary_key=True)
    score = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Follow(Base):
    __tablename__ = "follows"

    follower_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    following_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    created_at = Column(DateTime, default=datetime.utcnow)

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    is_private = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

class GroupMember(Base):
    __tablename__ = "group_members"

    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(String, default="member")  # admin, moderator

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class ContentTag(Base):
    __tablename__ = "content_tags"

    content_id = Column(Integer, ForeignKey("content.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    room_id = Column(String)
    sender_id = Column(Integer, ForeignKey("users.id"))

    content = Column(Text)
    encrypted = Column(Boolean, default=True)
    read = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"

    reporter_id = Column(Integer, ForeignKey("users.id"))
    content_id = Column(Integer, ForeignKey("content.id"))

    reason = Column(String)
    status = Column(String, default="pending")

       