from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    user_id = Column(String(36), primary_key=True, nullable=False)
    user_name = Column(String(50), unique=True, nullable=False)
    user_email = Column(String(100), unique=True, nullable=False)
    user_password = Column(String(255), nullable=False)

    def __init__(self, user_id, user_name, user_email, user_password):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password