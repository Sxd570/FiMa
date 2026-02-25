from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class GetGoalsOverviewResponse(BaseModel):
    total_goals_count: Optional[int] = Field(None, description="Total number of goals created by the user.")
    total_goals_completed: Optional[int] = Field(None, description="Number of goals that have been completed.")
    total_amount_saved: Optional[float] = Field(None, description="Total amount saved across all goals.")
    total_goal_amount: Optional[float] = Field(None, description="Total target amount across all goals.")


class GoalDetail(BaseModel):
    goal_id: Optional[UUID] = Field(None, description="Unique identifier of the goal.")
    goal_name: Optional[str] = Field(None, description="Name of the goal.")
    goal_description: Optional[str] = Field(None, description="Description of the goal.")
    goal_target_amount: Optional[float] = Field(None, description="Target amount to be saved for the goal.")
    goal_current_amount: Optional[float] = Field(None, description="Current amount saved towards the goal.")
    goal_remaining_amount: Optional[float] = Field(None, description="Amount remaining to reach the target goal.")
    goal_percentage: Optional[float] = Field(None, description="Percentage of the goal achieved.")
    is_goal_reached: Optional[bool] = Field(None, description="Indicates if the goal has been reached or completed.")


class GetGoalDetailsResponse(BaseModel):
    goal_details: Optional[List[GoalDetail]] = Field(None, description="List of goal detail objects for the user.")


class CreateGoalResponse(BaseModel):
    status: Optional[str] = Field(None, description="Indicates whether the goal was created successfully.")


class DeleteGoalResponse(BaseModel):
    status: Optional[str] = Field(None, description="Indicates whether the goal was deleted successfully.")
    goal_id: Optional[UUID] = Field(None, description="The ID of the deleted goal.")


class EditGoalResponse(BaseModel):
    status: Optional[str] = Field(None, description="Indicates whether the goal was edited successfully.")


class AddAmountToGoalResponse(BaseModel):
    status: Optional[str] = Field(None, description="Indicates whether the amount was added successfully.")
