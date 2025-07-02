from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Goal(Base):
    __tablename__ = 'goals'
    
    user_id = Column(String(36), nullable=False)
    goal_id = Column(String(36), primary_key=True, nullable=False)
    goal_name = Column(String(255), nullable=False)
    goal_description = Column(String(255), nullable=True)
    goal_target_amount = Column(Integer, nullable=False)
    goal_current_amount = Column(Integer, default=0, nullable=False)

    def __init__(self, user_id, goal_id, goal_name, goal_description, goal_current_amount, goal_target_amount):
        self.user_id = user_id
        self.goal_id = goal_id
        self.goal_name = goal_name
        self.goal_description = goal_description
        self.goal_current_amount = goal_current_amount
        self.goal_target_amount = goal_target_amount

