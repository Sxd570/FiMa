from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transactions(Base):
    __tablename__ = 'transactions'
    
    user_id = Column(String(36), nullable=False)
    transaction_id = Column(String(36), primary_key=True, nullable=False)
    transaction_type_id = Column(String(36), nullable=False)
    category_id = Column(String(36), nullable=False)
    transaction_name = Column(String(255), nullable=False)
    transaction_description = Column(String(255), nullable=True)
    transaction_amount = Column(Integer, nullable=False)
    transaction_date = Column(String(50), nullable=False)

    def __init__(self, user_id, transaction_id, category_id, transaction_name, transaction_description,transaction_amount, transaction_date):
        self.user_id = user_id
        self.transaction_id = transaction_id
        self.category_id = category_id
        self.transaction_name = transaction_name
        self.transaction_description = transaction_description
        self.transaction_amount = transaction_amount
        self.transaction_date = transaction_date