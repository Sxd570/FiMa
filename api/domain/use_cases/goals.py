from shared.logger import Logger
from shared.Utility.generate_id import generate_goal_id
from domain.database.goals import GoalsDatabase
from domain.models.io_models.goals_io_models import (
    GoalDetail,
    AddGoalDetailDBRequest,
    AddGoalDetailDBRequest,
    CreateGoalDetailPayload,
    GoalsDetailsResponse,
    GoalsOverviewResponse,
    UpdateGoalDetailPayload,
    EditGoalDetailDBRequest,
    DeleteGoalDetailDBRequest,
    DeleteGoalDetailPayload,
    AddAmountToGoalDetailPayload,
    AddAmountToGoalDetailDBRequest,
    GetGoalsDashboardPayload,
    GetGoalsDashboardDBRequest,
    GetGoalsDBRequest,
    UpdateGoalDetailPayload,
    EditGoalDetailDBRequest,
    DeleteGoalDetailDBRequest,
    DeleteGoalDetailPayload,
    AddAmountToGoalDetailPayload,
    AddAmountToGoalDetailDBRequest,
    GetGoalsDashboardPayload,
    GetGoalsDashboardDBRequest,
    GetGoalsDBRequest,
)

logger = Logger(__name__)

class GoalsUseCase:
    def __init__(self):
        self.goal_database = GoalsDatabase()

        self.user_id = None
        self.goal_id = None

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
                total_goal_amount=float(self.total_goal_amount),
            )
        except Exception as e:
            logger.error(f"Error in get_goals_overview use case: {e}")
            raise e


    def get_goal_details(self, user_id: str):
        try:
            self.user_id = user_id
            db_request = GetGoalsDBRequest(user_id=self.user_id)
            goal_details = self.goal_database.get_goal_details(db_request=db_request)
            return GoalsDetailsResponse(
                goal_details=[
                    GoalDetail(
                        goal_id=goal.goal_id,
                        goal_name=goal.goal_name,
                        goal_description=goal.goal_description,
                        goal_target_amount=float(goal.goal_target_amount),
                        goal_current_amount=float(goal.goal_current_amount),
                        goal_remaining_amount=float(goal.goal_target_amount - goal.goal_current_amount),
                        goal_percentage=float(
                            goal.goal_current_amount / goal.goal_target_amount * 100
                            if goal.goal_target_amount > 0 else 0
                        ),
                        is_goal_reached=goal.is_goal_reached,
                    )
                    for goal in goal_details.goal_details
                ]
            )
        except Exception as e:
            logger.error(f"Error in get_goal_details use case: {e}")
            raise e


    def create_goal(self, payload: CreateGoalDetailPayload):
        try:
            self.user_id = payload.user_id
            self.goal_name = payload.goal_name
            self.goal_description = payload.goal_description
            self.goal_target_amount = payload.goal_target_amount
            self.goal_current_amount = 0

            self.goal_id = generate_goal_id(
                goal_name=self.goal_name, 
                user_id=self.user_id
            )

            db_request = AddGoalDetailDBRequest(
                goal_id=self.goal_id,
                user_id=self.user_id,
                goal_name=self.goal_name,
                goal_description=self.goal_description,
                goal_target_amount=float(self.goal_target_amount),
                goal_current_amount=float(self.goal_current_amount),
            )

            status = self.goal_database.create_goal(
                db_request=db_request
            )

            return status
        except Exception as e:
            logger.error(f"Error in create_goal use case: {e}")
            raise e

    def edit_goal(self, payload: UpdateGoalDetailPayload):
        try:
            self.user_id = payload.user_id
            self.goal_id = payload.goal_id
            self.goal_name = getattr(payload, 'goal_name', None)
            self.goal_description = getattr(payload, 'goal_description', None)
            self.goal_target_amount = getattr(payload, 'goal_target_amount', None)
            self.goal_current_amount = getattr(payload, 'goal_current_amount', None)
            db_request = EditGoalDetailDBRequest(
                user_id=self.user_id,
                goal_id=self.goal_id,
                goal_name=self.goal_name,
                goal_description=self.goal_description,
                goal_target_amount=float(self.goal_target_amount) if self.goal_target_amount is not None else None,
                goal_current_amount=float(self.goal_current_amount) if self.goal_current_amount is not None else None,
            )
            status = self.goal_database.edit_goal(db_request=db_request)
            return status
        except Exception as e:
            logger.error(f"Error in edit_goal use case: {e}")
            raise e

    def delete_goal(self, payload: DeleteGoalDetailPayload):
        try:
            self.user_id = payload.user_id
            self.goal_id = payload.goal_id
            db_request = DeleteGoalDetailDBRequest(
                user_id=self.user_id, goal_id=self.goal_id
            )
            status = self.goal_database.delete_goal(db_request=db_request)
            return status
        except Exception as e:
            logger.error(f"Error in delete_goal use case: {e}")
            raise e

    def add_amount_to_goal(self, payload: AddAmountToGoalDetailPayload):
        try:
            self.user_id = payload.user_id
            self.goal_id = payload.goal_id
            self.amount_to_add = payload.amount_to_add
            db_request = AddAmountToGoalDetailDBRequest(
                user_id=self.user_id,
                goal_id=self.goal_id,
                amount_to_add=self.amount_to_add,
            )
            status = self.goal_database.add_amount_to_goal(db_request=db_request)
            return status
        except Exception as e:
            logger.error(f"Error in add_amount_to_goal use case: {e}")
            raise e

    def get_goals_dashboard(self, payload: GetGoalsDashboardPayload):
        try:
            self.user_id = payload.user_id
            self.limit = payload.limit
            self.offset = payload.offset

            db_request = GetGoalsDashboardDBRequest(
                user_id=self.user_id, 
                limit=self.limit, 
                offset=self.offset
            )

            goals_response = self.goal_database.get_goal_details(
                db_request=db_request
            )

            return GoalsDetailsResponse(
                goal_details=[
                    GoalDetail(
                        goal_id=goal.goal_id,
                        goal_name=goal.goal_name,
                        goal_description=goal.goal_description,
                        goal_target_amount=float(goal.goal_target_amount),
                        goal_current_amount=float(goal.goal_current_amount),
                        goal_remaining_amount=float(goal.goal_target_amount - goal.goal_current_amount),
                        goal_percentage=float(goal.goal_current_amount / goal.goal_target_amount * 100 if goal.goal_target_amount > 0 else 0),
                        is_goal_reached=goal.is_goal_reached
                    ) for goal in goals_response.goal_details
                ]
            )
        except Exception as e:
            logger.error(f"Error in get_goals_dashboard use case: {e}")
            raise e