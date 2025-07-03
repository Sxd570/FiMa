from sqlalchemy import *
from shared.logger import Logger
from core.models.tables.goal import Goal
from shared.Utility.db_base import get_db_session
from copy import deepcopy
from core.models.io_models.goals_io_models import (
    GoalDetailsDBResponse,
    GoalDetail,
    EditGoalDetail,
    AddGoalDetailDBRequest
)
from core.interfaces.goals_interface import GoalsInterface
from typing import Optional

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
                Goal.user_id == self.user_id
            ]

            total_goals_count = self.db_session.query(
                func.count(Goal.goal_id)
            ).filter(
                *filter_group
            ).scalar()

            if not total_goals_count:
                total_goals_count = 0

            return total_goals_count
        except Exception as e:
            logger.error(f"Error in get_goals_overview: {e}")
            raise e



    def get_total_goals_completed(self, user_id: str):
        try:
            self.db_session = get_db_session()
            self.user_id = user_id

            filter_group = [
                Goal.user_id == self.user_id,
                Goal.goal_current_amount >= Goal.goal_target_amount
            ]

            total_goals_completed = self.db_session.query(
                func.count(Goal.goal_id)
            ).filter(
                *filter_group
            ).scalar()

            if not total_goals_completed:
                total_goals_completed = 0

            return total_goals_completed
        except Exception as e:
            logger.error(f"Error in get_total_goals_completed: {e}")
            raise e

    

    def get_total_amount_saved(self, user_id: str):
        try:
            self.db_session = get_db_session()
            self.user_id = user_id

            filter_group = [
                Goal.user_id == self.user_id,
            ]

            total_amount_saved = self.db_session.query(
                func.sum(Goal.goal_current_amount)
            ).filter(
                *filter_group,
            ).scalar()

            if not total_amount_saved:
                total_amount_saved = 0

            return total_amount_saved
        except Exception as e:
            logger.error(f"Error in get_total_amount_saved: {e}")
            raise e



    def get_total_goals_amount(self, user_id: str):
        try:
            self.db_session = get_db_session()
            self.user_id = user_id

            filter_group = [
                Goal.user_id == self.user_id,
            ]

            total_goal_amount = self.db_session.query(
                func.sum(Goal.goal_target_amount)
            ).filter(
                *filter_group,
            ).scalar()

            if not total_goal_amount:
                total_goal_amount = 0

            return total_goal_amount
        except Exception as e:
            logger.error(f"Error in get_total_goals_amount: {e}")
            raise e



    def get_goal_details(self, user_id: str, limit: Optional[int] = None, offset: Optional[int] = 0):
        try:
            self.db_session = get_db_session()
            self.user_id = user_id

            query = self.db_session.query(
                    Goal
                ).filter(
                    Goal.user_id == self.user_id
                )

            if offset:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)
                
            db_response = query.all()
            
            if not db_response:
                return GoalDetailsDBResponse(
                    Goal=[]
                )
            
            response = deepcopy(db_response)

            goal_details = GoalDetailsDBResponse(
                Goal=[
                    GoalDetail(
                        goal_id=goal.goal_id,
                        goal_name=goal.goal_name,
                        goal_description=goal.goal_description,
                        goal_target_amount=goal.goal_target_amount,
                        goal_current_amount=goal.goal_current_amount,
                        is_goal_reached=goal.is_goal_reached
                    ) for goal in response
                ]
            )

            return goal_details
        except Exception as e:
            logger.error(f"Error in get_goal_details: {e}")
            raise e



    def create_goal(self, goal: AddGoalDetailDBRequest):
        try:
            self.db_session = get_db_session()

            existing_goal = self.db_session.query(
                Goal
            ).filter(
                Goal.goal_id == goal.goal_id
            ).first()
            
            if existing_goal:
                logger.error(f"Goal with goal_id {goal.goal_id} already exists. Goal not created.")
                return {
                    "message": "Goal already exists",
                }

            new_goal = Goal(
                user_id=goal.user_id,
                goal_id=goal.goal_id,
                goal_name=goal.goal_name,
                goal_description=goal.goal_description,
                goal_target_amount=goal.goal_target_amount,
                goal_current_amount=goal.goal_current_amount
            )

            self.db_session.add(new_goal)
            self.db_session.commit()

            return {
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Error in create_goal: {e}")
            raise e



    def edit_goal(self, user_id, goal: EditGoalDetail):
        try:
            self.db_session = get_db_session()

            goal_name = goal.goal_name
            goal_description = goal.goal_description
            goal_target_amount = goal.goal_target_amount
            goal_current_amount = goal.goal_current_amount

            filter_group = [
                Goal.user_id == user_id,
                Goal.goal_id == goal.goal_id
            ]

            existing_goal = self.db_session.query(
                    Goal
                ).filter(
                    *filter_group
                ).first()
            if not existing_goal:
                logger.error(f"Goal with goal_id {goal.goal_id} does not exist. Goal not updated.")
                return {
                    "message": "Goal does not exist",
                }

            if goal_name:
                existing_goal.goal_name = goal_name
            if goal_description:
                existing_goal.goal_description = goal_description
            if goal_target_amount:
                existing_goal.goal_target_amount = goal_target_amount
            if goal_current_amount:
                existing_goal.goal_current_amount = goal_current_amount

            if existing_goal.goal_current_amount >= existing_goal.goal_target_amount:
                existing_goal.is_goal_reached = True
            else:
                existing_goal.is_goal_reached = False

            self.db_session.commit()

            return {
                "status": "success",
                "goal_id": goal.goal_id
            }
        except Exception as e:
            logger.error(f"Error in update_goal: {e}")
            raise e

    def delete_goal(self, user_id: str, goal_id: str):
        try:
            self.db_session = get_db_session()
            filter_group = [
                Goal.user_id == user_id, 
                Goal.goal_id == goal_id
            ]

            goal = self.db_session.query(
                Goal
                ).filter(
                    *filter_group
                ).first()
            if not goal:
                logger.error(f"Goal with goal_id {goal_id} does not exist. Goal not deleted.")
                return {
                    "message": "Goal does not exist"
                }
            
            self.db_session.delete(goal)
            self.db_session.commit()
            return {
                "status": "success",
                "goal_id": goal_id
            }
        except Exception as e:
            logger.error(f"Error in delete_goal: {e}")
            raise e


    
    def add_amount_to_goal(self, user_id: str, goal_id: str, amount_to_add: float):
        try:
            self.db_session = get_db_session()

            filter_group = [
                Goal.user_id == user_id, 
                Goal.goal_id == goal_id
            ]

            goal = self.db_session.query(
                    Goal
                ).filter(
                    *filter_group
                ).first()
            if not goal:
                logger.error(f"Goal with goal_id {goal_id} does not exist. Amount not added.")
                return {
                    "message": "Goal does not exist"
                }

            goal.goal_current_amount += amount_to_add

            if goal.goal_current_amount >= goal.goal_target_amount:
                goal.is_goal_reached = True
            else:
                goal.is_goal_reached = False

            self.db_session.commit()

            return {
                "status": "success",
                "goal_id": goal_id
            }
        except Exception as e:
            logger.error(f"Error in add_amount_to_goal: {e}")
            raise e
