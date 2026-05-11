from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Conversations(Base):
    __tablename__ = 'conversation'

    conversation_id = Column(String(36), primary_key=True, nullable=False)
    user_id = Column(String(36), nullable=False)
    title = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)
    total_token_used = Column(Integer, nullable=False)
    last_message_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, conversation_id, user_id, title, status, total_token_used, last_message_at, created_at, updated_at):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.title = title
        self.status = status
        self.total_token_used = total_token_used
        self.last_message_at = last_message_at
        self.created_at = created_at
        self.updated_at = updated_at
