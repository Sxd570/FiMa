from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TransactionTypes(Base):
    __tablename__ = 'transaction_types'
    
    user_id = Column(String(36), nullable=False)
    type_id = Column(String(36), primary_key=True)
    type_name = Column(String(255), nullable=False)
    type_description = Column(String(255), nullable=True)

    def __init__(self, user_id, type_id, type_name, type_description):
        self.user_id = user_id
        self.type_id = type_id
        self.type_name = type_name
        self.type_description = type_description