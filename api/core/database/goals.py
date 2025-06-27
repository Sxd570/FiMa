from sqlalchemy import *
from shared.logger import Logger
from core.models.tables.goals import Goals
from core.database.base import get_db_session
from copy import deepcopy
from core.models.io_models.goals_io_models import (
    GoalDetailsDBResponse,
    GoalDetail
)

logger = Logger(__name__)

class GoalsDatabase:
    def __init__(self):
        self.db_session = None
        self.user_id = None

    def get_total_goals_count(self, user_id):
        try:
            self.db_session = get_db_session()

            self.user_id = user_id

            filter_group = [
                Goals.user_id == self.user_id
            ]

            total_goals_count = self.db_session.query(
                func.count(Goals.goal_id)
            ).filter(
                *filter_group
            ).scalar()

            if total_goals_count is None:
                total_goals_count = 0

            return total_goals_count
        except Exception as e:
            logger.error(f"Error in get_goals_overview: {e}")
            raise e
    
    
    def get_goal_details(self, user_id):
        try:
            self.db_session = get_db_session()
            self.user_id = user_id

            db_response = self.db_session.query(
                Goals
            ).filter(
                Goals.user_id == self.user_id
            ).all()
            
            if not db_response:
                return GoalDetailsDBResponse(
                    Goals=[]
                )
            
            response = deepcopy(db_response)

            goal_details = GoalDetailsDBResponse(
                Goals=[
                    GoalDetail(
                        goal_id = goal.goal_id,
                        goal_target_amount = goal.goal_target_amount,
                        goal_current_amount = goal.goal_current_amount,
                    ) for goal in response
                ]
            )

            return goal_details
        except Exception as e:
            logger.error(f"Error in get_goal_details: {e}")
            raise e