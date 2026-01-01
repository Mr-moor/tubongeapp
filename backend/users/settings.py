class UserSettings(Base):
    user_id = Column(Integer, ForeignKey("users.id"))
    private_account = Column(Boolean, default=False)
    allow_messages = Column(Boolean, default=True)
    allow_tags = Column(Boolean, default=True)
