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
    is_limit_reached = Column(Boolean, nullable=False)

    def __init__(self, user_id, category_id, budget_id, allocated_amount, spent_amount, is_limit_reached):
        self.user_id = user_id
        self.category_id = category_id
        self.budget_id = budget_id
        self.allocated_amount = allocated_amount
        self.spent_amount = spent_amount
        self.is_limit_reached = is_limit_reached