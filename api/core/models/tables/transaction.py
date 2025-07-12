from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transaction'
    
    user_id = Column(String(36), nullable=False)
    transaction_id = Column(String(36), primary_key=True, nullable=False)
    category_id = Column(String(36), nullable=False)
    transaction_type = Column(String(36), nullable=False)
    transaction_info = Column(String(255), nullable=False)
    transaction_amount = Column(Integer, nullable=False)
    transaction_date = Column(String(50), nullable=False)

    def __init__(self, user_id, transaction_id, category_id, transaction_type, transaction_info, transaction_amount, transaction_date):
        self.user_id = user_id
        self.transaction_id = transaction_id
        self.category_id = category_id
        self.transaction_type = transaction_type
        self.transaction_info = transaction_info
        self.transaction_amount = transaction_amount
        self.transaction_date = transaction_date