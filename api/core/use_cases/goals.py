from shared.logger import Logger
from shared.Utility import generate_goal_id
from core.database.goals import GoalsDatabase
from core.models.io_models.goals_io_models import (
    GoalDetail,
    GoalDetailPayload,
    GoalsDetailsResponse,
    GoalsOverviewResponse
)

logger = Logger(__name__)

class GoalsUseCase:
    def __init__(self):
        self.goal_database = GoalsDatabase()

        self.user_id = None
        self.goal_id = None

        self.goal_name = None
        self.goal_description = None
        self.goal_target_amount = None
        self.goal_current_amount = None

        self.total_goals_count = 0
        self.total_goals_completed = 0
        self.total_amount_saved = 0
        self.total_goal_amount = 0


    def get_goals_overview(self, user_id: str):
        try:
            self.user_id = user_id

            self.total_goals_count = self.goal_database.get_total_goals_count(self.user_id)
            self.total_goals_completed = self.goal_database.get_total_goals_completed(self.user_id)
            self.total_amount_saved = self.goal_database.get_total_amount_saved(self.user_id)
            self.total_goal_amount = self.goal_database.get_total_goals_amount(self.user_id)

            return GoalsOverviewResponse(
                total_goals_count=self.total_goals_count,
                total_goals_completed=self.total_goals_completed,
                total_amount_saved=float(self.total_amount_saved),
                total_goal_amount=float(self.total_goal_amount)
            )

        except Exception as e:
            logger.error(f"Error in get_goals_overview use case: {e}")
            raise e
        
    
    def get_goal_details(self, user_id: str):
        try:
            self.user_id = user_id

            goal_details = self.goal_database.get_goal_details(self.user_id)
            
            return GoalsDetailsResponse(
                goals = [
                    GoalDetail(
                        goal_id=goal.goal_id,
                        goal_name=goal.goal_name,
                        goal_description=goal.goal_description,
                        goal_target_amount=float(goal.goal_target_amount),
                        goal_current_amount=float(goal.goal_current_amount),
                        goal_remaining_amount=float(goal.goal_target_amount - goal.goal_current_amount),
                        goal_percentage=float(goal.goal_current_amount / goal.goal_target_amount * 100 if goal.goal_target_amount > 0 else 0)
                    ) for goal in goal_details.goals
                ]
            )
        except Exception as e:
            logger.error(f"Error in get_goal_details use case: {e}")
            raise e
        
    
    def create_goal(self, user_id: str, params: GoalDetailPayload):
        try:
            self.user_id = user_id
            self.goal_name = params.goal_name
            self.goal_description = params.goal_description
            self.goal_target_amount = params.goal_target_amount
            self.goal_current_amount = 0

            self.goal_id = generate_goal_id(
                goal_name=self.goal_name, 
                user_id=self.user_id
            )

            query_input = GoalDetail(
                goal_id=self.goal_id,
                user_id=self.user_id,
                goal_name=self.goal_name,
                goal_description=self.goal_description,
                goal_target_amount=float(self.goal_target_amount),
                goal_current_amount=float(self.goal_current_amount),
            )

            self.goal_database.create_goal(query_input)

            return {
                "status": "success",
                "goal_id": self.goal_id
            }

        except Exception as e:
            logger.error(f"Error in create_goal use case: {e}")
            raise e