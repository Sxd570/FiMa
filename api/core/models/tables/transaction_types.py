from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TransactionType(Base):
    __tablename__ = 'transaction_type'
    
    user_id = Column(String(36), nullable=False)
    transaction_type_id = Column(String(36), primary_key=True, nullable=False)
    transaction_type_name = Column(String(255), nullable=False)
    transaction_type_description = Column(String(255), nullable=True)

    def __init__(self, user_id, transaction_type_id, transaction_type_name, transaction_type_description):
        self.user_id = user_id
        self.transaction_type_id = transaction_type_id
        self.transaction_type_name = transaction_type_name
        self.transaction_type_description = transaction_type_description