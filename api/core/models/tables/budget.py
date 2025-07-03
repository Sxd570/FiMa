from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Budget(Base):
    __tablename__ = 'budget'
    
    user_id = Column(String(36), nullable=False)
    category_id = Column(String(36), nullable=False)
    budget_id = Column(String(36), primary_key=True, nullable=False)
    budget_allocated_amount = Column(Integer, nullable=False)
    budget_spent_amount = Column(Integer, nullable=False)
    budget_allocated_month = Column(String(7), nullable=False)
    is_budget_limit_reached = Column(Boolean, nullable=False)
    is_budget_over_limit = Column(Boolean, nullable=False)

    def __init__(self, user_id, category_id, budget_id, budget_allocated_amount, budget_spent_amount, budget_allocated_month, is_budget_limit_reached, is_budget_over_limit):
        self.user_id = user_id
        self.category_id = category_id
        self.budget_id = budget_id
        self.budget_allocated_amount = budget_allocated_amount
        self.budget_spent_amount = budget_spent_amount
        self.budget_allocated_month = budget_allocated_month  
        self.is_budget_limit_reached = is_budget_limit_reached
        self.is_budget_over_limit = is_budget_over_limit