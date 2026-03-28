from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    time = Column(DateTime, default=datetime.utcnow)
    message = Column(String, nullable=False)