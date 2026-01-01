class Group(Base):
    name = Column(String)
    description = Column(Text)
    is_private = Column(Boolean, default=False)
