from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class GetGoalsOverviewResponse(BaseModel):
    total_goals_count: int = Field(..., description="Total number of goals created by the user.")
    total_goals_completed: int = Field(..., description="Number of goals that have been completed.")
    total_amount_saved: float = Field(..., description="Total amount saved across all goals.")
    total_goal_amount: float = Field(..., description="Total target amount across all goals.")


class GoalDetail(BaseModel):
    goal_id: UUID = Field(..., description="Unique identifier of the goal.")
    goal_name: str = Field(..., description="Name of the goal.")
    goal_description: str = Field(..., description="Description of the goal.")
    goal_target_amount: float = Field(..., gt=0, description="Target amount to be saved for the goal.")
    goal_current_amount: float = Field(..., ge=0, description="Current amount saved towards the goal.")
    goal_remaining_amount: float = Field(..., ge=0, description="Amount remaining to reach the target goal.")
    goal_percentage: float = Field(..., ge=0, le=100, description="Percentage of the goal achieved.")
    is_goal_reached: bool = Field(..., description="Indicates if the goal has been reached or completed.")


class GetGoalDetailsResponse(BaseModel):
    goal_details: List[GoalDetail] = Field(..., description="List of goal detail objects for the user.")


class CreateGoalResponse(BaseModel):
    status: str = Field(..., description="Indicates whether the goal was created successfully.")


class DeleteGoalResponse(BaseModel):
    status: str = Field(..., description="Indicates whether the goal was deleted successfully.")
    goal_id: UUID = Field(..., description="The ID of the deleted goal.")


class EditGoalResponse(BaseModel):
    status: str = Field(..., description="Indicates whether the goal was edited successfully.")


class AddAmountToGoalResponse(BaseModel):
    status: str = Field(..., description="Indicates whether the amount was added successfully.")
