from shared.logger import Logger
from core.database.goals import GoalsDatabase
from core.models.io_models.goals_io_models import (
    GoalsOverviewResponse
)

logger = Logger(__name__)

class GoalUseCase:
    def __init__(self):
        self.goal_database = None

        self.user_id = None
        self.total_goals_count = 0
        self.total_goals_completed = 0
        self.total_amount_saved = 0
        self.total_goal_amount = 0


    def get_goals_overview(self, user_id):
        try:
            self.goal_database = GoalsDatabase()

            self.user_id = user_id

            self.total_goals_count = self.goal_database.get_total_goals_count(self.user_id)
            goal_details_list = self.goal_database.get_goal_details(self.user_id)
            if goal_details_list is None or not goal_details_list.Goals:
                return GoalsOverviewResponse(
                    total_goals_count=0,
                    total_goals_completed=0,
                    total_amount_saved=0.0,
                    total_goal_amount=0.0
                )
            
            self.total_goals_completed = sum(
                1 for goal in goal_details_list.Goals if goal.goal_current_amount >= goal.goal_target_amount
            )

            self.total_amount_saved = sum(
                goal.goal_current_amount for goal in goal_details_list.Goals if goal.goal_current_amount >= goal.goal_target_amount
            )

            self.total_amount = sum(
                goal.goal_target_amount for goal in goal_details_list.Goals
            )

            return GoalsOverviewResponse(
                total_goals_count=self.total_goals_count,
                total_goals_completed=self.total_goals_completed,
                total_amount_saved=float(self.total_amount_saved),
                total_goal_amount=float(self.total_goal_amount)
            )

        except Exception as e:
            logger.error(f"Error in get_goals_overview use case: {e}")
            raise e