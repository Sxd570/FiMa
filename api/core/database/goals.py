from sqlalchemy import *
from shared.logger import Logger
from core.models.tables.goals import Goals
from core.database.base import get_db_session
from copy import deepcopy
from core.models.io_models.goals_io_models import (
    GoalDetailsDBResponse,
    GoalDetail
)
from core.interfaces.goals_interface import GoalsInterface

logger = Logger(__name__)

class GoalsDatabase(GoalsInterface):
    def __init__(self):
        self.db_session = None
        self.user_id = None

    def get_total_goals_count(self, user_id:str):
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

            return total_goals_count
        except Exception as e:
            logger.error(f"Error in get_goals_overview: {e}")
            raise e
        finally:
            if self.db_session:
                self.db_session.close()


    def get_total_goals_completed(self, user_id: str):
        try:
            self.db_session = get_db_session()
            self.user_id = user_id

            filter_group = [
                Goals.user_id == self.user_id,
                Goals.goal_current_amount >= Goals.goal_target_amount
            ]

            total_goals_completed = self.db_session.query(
                func.count(Goals.goal_id)
            ).filter(
                *filter_group
            ).scalar()

            return total_goals_completed
        except Exception as e:
            logger.error(f"Error in get_total_goals_completed: {e}")
            raise e
        finally:
            if self.db_session:
                self.db_session.close()
    

    def get_total_amount_saved(self, user_id: str):
        try:
            self.db_session = get_db_session()
            self.user_id = user_id

            filter_group = [
                Goals.user_id == self.user_id,
            ]

            total_amount_saved = self.db_session.query(
                func.sum(Goals.goal_current_amount)
            ).filter(
                *filter_group,
            ).scalar()

            return total_amount_saved
        except Exception as e:
            logger.error(f"Error in get_total_amount_saved: {e}")
            raise e
        finally:
            if self.db_session:
                self.db_session.close()


    def get_total_goals_amount(self, user_id: str):
        try:
            self.db_session = get_db_session()
            self.user_id = user_id

            filter_group = [
                Goals.user_id == self.user_id,
            ]

            total_goal_amount = self.db_session.query(
                func.sum(Goals.goal_target_amount)
            ).filter(
                *filter_group,
            ).scalar()

            return total_goal_amount
        except Exception as e:
            logger.error(f"Error in get_total_goals_amount: {e}")
            raise e
        finally:
            if self.db_session:
                self.db_session.close()


    def get_goal_details(self, user_id: str):
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
                    goals=[]
                )
            
            response = deepcopy(db_response)

            goal_details = GoalDetailsDBResponse(
                goals=[
                    GoalDetail(
                        goal_id=goal.goal_id,
                        goal_name=goal.goal_name,
                        goal_description=goal.goal_description,
                        goal_target_amount=goal.goal_target_amount,
                        goal_current_amount=goal.goal_current_amount,
                    ) for goal in response
                ]
            )

            return goal_details
        except Exception as e:
            logger.error(f"Error in get_goal_details: {e}")
            raise e
        finally:
            if self.db_session:
                self.db_session.close()


    def create_goal(self, goal: GoalDetail):
        try:
            self.db_session = get_db_session()

            new_goal = Goals(
                user_id=goal.user_id,
                goal_id=goal.goal_id,
                goal_name=goal.goal_name,
                goal_description=goal.goal_description,
                goal_target_amount=goal.goal_target_amount,
                goal_current_amount=goal.goal_current_amount
            )

            self.db_session.add(new_goal)
            self.db_session.commit()
        except Exception as e:
            logger.error(f"Error in create_goal: {e}")
            raise e
        finally:
            if self.db_session:
                self.db_session.close()