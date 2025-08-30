from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    
    user_id = Column(String(36), nullable=False)
    transaction_type = Column(String(36), nullable=False)
    category_id = Column(String(36), primary_key=True)
    category_name = Column(String(255), nullable=False)
    category_description = Column(String(255), nullable=True)

    def __init__(self, user_id, transaction_type, category_id, category_name, category_description):
        self.user_id = user_id
        self.transaction_type = transaction_type
        self.category_id = category_id
        self.category_name = category_name
        self.category_description = category_description