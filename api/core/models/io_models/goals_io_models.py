from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any

class GoalDetail(BaseModel):
    goal_id: Optional[str] = Field(None, description="Unique identifier for the goal")
    goal_name: Optional[str] = Field(None, description="Name of the goal")
    goal_description: Optional[str] = Field(None, description="Description of the goal")
    goal_target_amount: Optional[float] = Field(None, description="Target amount for the goal")
    goal_current_amount: Optional[float] = Field(None, description="Current amount towards the goal")
    goal_remaining_amount: Optional[float] = Field(None, description="Remaining amount to reach the goal")
    goal_percentage: Optional[float] = Field(None, description="Percentage of the goal achieved")

class AddGoalDetail(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    goal_id: str = Field(..., description="Unique identifier for the goal")
    goal_name: str = Field(..., description="Name of the goal")
    goal_description: str = Field(..., description="Description of the goal")
    goal_target_amount: float = Field(..., description="Target amount for the goal")
    goal_current_amount: float = Field(..., description="Current amount towards the goal", ge=0.0)


class EditGoalDetail(BaseModel):
    goal_id: str = Field(..., description="Unique identifier for the goal")
    goal_name: Optional[str] = Field(None, description="Name of the goal")
    goal_description: Optional[str] = Field(None, description="Description of the goal")
    goal_target_amount: Optional[float] = Field(None, description="Target amount for the goal")
    goal_current_amount: Optional[float] = Field(None, description="Current amount towards the goal", ge=0.0)


class UpdateGoalDetail(BaseModel):
    goal_id: str = Field(..., description="Unique identifier for the goal")
    goal_name: Optional[str] = Field(None, description="Name of the goal")
    goal_description: Optional[str] = Field(None, description="Description of the goal")
    goal_target_amount: Optional[float] = Field(None, description="Target amount for the goal")
    goal_current_amount: Optional[float] = Field(None, description="Current amount towards the goal", ge=0.0)


class DeleteGoalDetailPayload(BaseModel):
    goal_id: str = Field(..., description="Unique identifier for the goal to be deleted")

class AddAmountToGoalDetailPayload(BaseModel):
    goal_id: str = Field(..., description="Unique identifier for the goal")
    amount_to_add: int = Field(..., description="Amount to be added to the goal", ge=0.0)


class CreateGoalDetailPayload(BaseModel):
    goal_name: str = Field(..., description="Name of the goal")
    goal_description: Optional[str] = Field(None, description="Description of the goal")
    goal_target_amount: float = Field(..., description="Target amount for the goal")


class UpdateGoalDetailPayload(BaseModel):
    goal_id: str = Field(..., description="Unique identifier for the goal")
    goal_name: Optional[str] = Field(None, description="Name of the goal")
    goal_description: Optional[str] = Field(None, description="Description of the goal")
    goal_target_amount: Optional[float] = Field(None, description="Target amount for the goal")
    goal_current_amount: Optional[float] = Field(None, description="Current amount towards the goal", ge=0.0)


class GoalDetailsDBResponse(BaseModel):
    goals: Optional[List[GoalDetail]] = None


class GoalsOverviewResponse(BaseModel):
    total_goals_count: int = Field(0, description="Total number of goals")
    total_goals_completed: int = Field(0, description="Total number of completed goals")
    total_amount_saved: float = Field(0.0, description="Total amount saved towards goals")
    total_goal_amount: float = Field(0.0, description="Total amount towards all goals")


class GoalsDetailsResponse(BaseModel):
    goals: Optional[List[GoalDetail]] = None