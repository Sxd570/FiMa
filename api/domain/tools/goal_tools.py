from shared.Utility.api_request import APIRequest
from strands import tool
from shared.logger import Logger

logger = Logger(__name__)


class GoalTools:

    @tool
    def get_goals_overview(self, user_id: str):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in get goals overview tool, {str(e)}")
            raise e
        

    @tool
    def get_goal_details(self, user_id: str):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in get goal details tool, {str(e)}")
            raise e
    
    @tool
    def create_goal(self, user_id: str, goal_name: str, goal_description: str, goal_target_amount: float):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in create goal tool, {str(e)}")
            raise e
        
    @tool
    def delete_goal(self, user_id: str, goal_id: str):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in delete goal tool, {str(e)}")
            raise e
        
    @tool
    def edit_goal(self, user_id: str, goal_id: str, goal_name: str, goal_description: str, goal_target_amount: float, goal_current_amount: float):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in edit goal tool, {str(e)}")
            raise e
    
    @tool
    def add_amount_to_goal(self, user_id: str, goal_id: str, amount_to_add: float):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in add amount to goal tool, {str(e)}")
            raise e