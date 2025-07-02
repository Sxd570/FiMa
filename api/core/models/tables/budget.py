from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Budget(Base):
    __tablename__ = 'budget'
    
    user_id = Column(String(36), nullable=False)
    category_id = Column(String(36), nullable=False)
    budget_id = Column(String(36), primary_key=True, nullable=False)
    allocated_amount = Column(Integer, nullable=False)
    spent_amount = Column(Integer, nullable=False)
    allocated_month = Column(String(7), nullable=False)
    is_limit_reached = Column(Boolean, nullable=False)
    is_over_limit = Column(Boolean, nullable=False)

    def __init__(self, user_id, category_id, budget_id, allocated_amount, spent_amount, allocated_month, is_limit_reached, is_over_limit):
        self.user_id = user_id
        self.category_id = category_id
        self.budget_id = budget_id
        self.allocated_amount = allocated_amount
        self.spent_amount = spent_amount
        self.allocated_month = allocated_month  
        self.is_limit_reached = is_limit_reached
        self.is_over_limit = is_over_limit