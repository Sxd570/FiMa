from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Budget(Base):
    __tablename__ = 'budget'
    
    user_id = Column(String(36), nullable=False)
    budget_id = Column(String(36), primary_key=True, nullable=False)
    budget_name = Column(String(255), nullable=False)
    budget_description = Column(String(255), nullable=True)
    budget_target_amount = Column(Integer, nullable=False)
    budget_current_amount = Column(Integer, default=0, nullable=False)

    def __init__(self, user_id, budget_id, budget_name, budget_description, budget_current_amount, budget_target_amount):
        self.user_id = user_id
        self.budget_id = budget_id
        self.budget_name = budget_name
        self.budget_description = budget_description
        self.budget_current_amount = budget_current_amount
        self.budget_target_amount = budget_target_amount