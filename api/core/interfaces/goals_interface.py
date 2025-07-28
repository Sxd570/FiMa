from abc import ABC, abstractmethod

from core.models.io_models.goals_io_models import (
    GoalDetailsDBResponse,
    EditGoalDetailDBRequest,
    AddGoalDetailDBRequest,
    DeleteGoalDetailDBRequest,
    AddAmountToGoalDetailDBRequest,
    GetGoalsDBRequest
)

class GoalsInterface(ABC):
    @abstractmethod
    def get_total_goals_count(self, user_id):
        """
        Get the total number of goals for a user.
        """
        pass

    @abstractmethod
    def get_total_goals_completed(self, user_id):
        """
        Get the total number of completed goals for a user.
        """
        pass

    @abstractmethod
    def get_total_amount_saved(self, user_id):
        """
        Get the total amount saved by a user across all goals.
        """
        pass

    @abstractmethod
    def get_total_goals_amount(self, user_id):
        """
        Get the total amount of all goals for a user.
        """
        pass

    @abstractmethod
    def get_goal_details(self, db_request: GetGoalsDBRequest) -> GoalDetailsDBResponse:
        """
        Get the details of all goals for a user, with optional pagination.
        """
        pass

    @abstractmethod
    def create_goal(self, goal: AddGoalDetailDBRequest) -> dict:
        """
        Create a new goal for a user.
        """
        pass

    @abstractmethod
    def edit_goal(self, db_request: EditGoalDetailDBRequest) -> dict:
        """
        Edit an existing goal for a user.
        """
        pass

    @abstractmethod
    def delete_goal(self, db_request: DeleteGoalDetailDBRequest) -> dict:
        """
        Delete a goal for a user.
        """
        pass

    @abstractmethod
    def add_amount_to_goal(self, db_request: AddAmountToGoalDetailDBRequest) -> dict:
        """
        Add an amount to a specific goal for a user.
        """
        pass