from shared.Utility.api_request import APIRequest
from strands import tool
from shared.logger import Logger
from constants import APIConstants, GoalConstants

logger = Logger(__name__)


class GoalTools:

    @tool
    def get_goals_overview(self, user_id: str):
        """
        This tool fetched the overview of goals for a user.

        Args:
            user_id (str): The ID of the user whose goals overview is to be fetched.

        Returns:
            dict: A dictionary containing the goals overview data.
                - total_goals_count: Total number of goals.
                - total_goals_completed: Number of completed goals.
                - total_amount_saved: Total amount saved across all goals.
                - total_goal_amount: Total target amount across all goals.
        
        Raises:
            Exception: If there is an error during the API request.

        Example:
            {
                "total_goals_count": 5,
                "total_goals_completed": 2,
                "total_amount_saved": 1500.0,
                "total_goal_amount": 5000.0
            }
        """
        def _get_goals_overview(user_id: str):
            try:
                api_request = APIRequest(
                    http_method=APIConstants.KEY_GET_METHOD.value,
                    endpoint=f"/goals/overview/{user_id}",
                )
                response = api_request.execute()
                return response
            except Exception as e:
                logger.error(f"Error in get goals overview tool, {str(e)}")
                raise e
            
        return _get_goals_overview(user_id)
    

    @tool
    def get_goal_details(self, user_id: str):
        """
        This tool fetched the details of a specific goal for a user.

        Args:
            user_id (str): The ID of the user whose goal details are to be fetched.

        Returns:
            dict: A dictionary containing the goal details data.
                - goal_details (list): A list of goal objects, each containing:
                    - goal_id: Unique identifier for the goal.
                    - goal_name: Name of the goal.
                    - goal_description: Description of the goal.
                    - goal_target_amount: Target amount for the goal.
                    - goal_current_amount: Current amount saved towards the goal.
                    - goal_remaining_amount: Remaining amount to reach the goal.
                    - goal_percentage: Percentage of the goal that has been achieved.
                    - is_goal_completed: Boolean indicating if the goal is completed.
        Raises:
            Exception: If there is an error during the API request.

        Example:
            {
                "goal_details": [
                    {
                        "goal_id": "d5ec4560-b4c5-5c88-aa3d-19825e0546e3",
                        "goal_name": "test goal 1",
                        "goal_description": "test description",
                        "goal_target_amount": 10000.0,
                        "goal_current_amount": 0.0,
                        "goal_remaining_amount": 10000.0,
                        "goal_percentage": 0.0,
                        "is_goal_reached": false
                    },
                    {
                        "goal_id": "f4ec4560-b4c5-5c88-aa3d-19825e0546e3",
                        "goal_name": "test goal 2",
                        "goal_description": "test description 2",
                        "goal_target_amount": 5000.0,
                        "goal_current_amount": 1500.0,
                        "goal_remaining_amount": 3500.0,
                        "goal_percentage": 30.0,
                        "is_goal_reached": false
                    }
                ]
            }
        """
        def _get_goal_details(user_id: str):
            try:
                api_request = APIRequest(
                    http_method=APIConstants.KEY_GET_METHOD.value,
                    endpoint=f"/goals/details/{user_id}",
                )
                response = api_request.execute()
                return response
            except Exception as e:
                logger.error(f"Error in get goal details tool, {str(e)}")
                raise e
            
        return _get_goal_details(user_id)
    
    
    @tool
    def create_goal(self, user_id: str, goal_name: str, goal_description: str, goal_target_amount: float):
        """
        This tool creates a new goal for a user.

        Args:
            user_id (str): The ID of the user for whom the goal is to be created
            goal_name (str): The name of the goal.
            goal_description (str): A brief description of the goal.
            goal_target_amount (float): The target amount to be saved for the goal.

        Returns:
            dict: A dictionary containing the status of the goal creation.
                - status: A message indicating whether the goal was created successfully.
        
        Raises:
            Exception: If there is an error during the API request.

        Example:
            {
                "status": "success"
            }
        """
        def _create_goal(user_id: str, goal_name: str, goal_description: str, goal_target_amount: float):
            try:
                api_request = APIRequest(
                    http_method=APIConstants.KEY_POST_METHOD.value,
                    endpoint=f"/goals/{user_id}",
                    payload={
                        GoalConstants.KEY_GOAL_NAME.value: goal_name,
                        GoalConstants.KEY_GOAL_DESCRIPTION.value: goal_description,
                        GoalConstants.KEY_GOAL_TARGET_AMOUNT.value: goal_target_amount
                    }
                )
                response = api_request.execute()
                return response
            except Exception as e:
                logger.error(f"Error in create goal tool, {str(e)}")
                raise e
            
        return _create_goal(user_id, goal_name, goal_description, goal_target_amount)

        
    @tool
    def delete_goal(self, user_id: str, goal_id: str):
        """
        This tool deletes a specific goal for a user.
        
        Args:
            user_id (str): The ID of the user whose goal is to be deleted.
            goal_id (str): The ID of the goal to be deleted.

        Returns:
            dict: A dictionary containing the status and goal_id of the deleted goal.
                - status: A message indicating whether the goal was deleted successfully.
                - goal_id: The ID of the deleted goal.

        Raises:
            Exception: If there is an error during the API request.

        Example:
            {
                "status": "success",
                "goal_id": "d5ec4560-b4c5-5c88-aa3d-19825e0546e3"
            }
        """
        def _delete_goal(user_id: str, goal_id: str):
            try:
                api_request = APIRequest(
                    http_method=APIConstants.KEY_DELETE_METHOD.value,
                    endpoint=f"/goals/{user_id}",
                    payload={
                        GoalConstants.KEY_GOAL_ID.value: goal_id
                    }
                )
                response = api_request.execute()
                return response
            except Exception as e:
                logger.error(f"Error in delete goal tool, {str(e)}")
                raise e
            
        return _delete_goal(user_id, goal_id)
        
    @tool
    def edit_goal(self, user_id: str, goal_id: str, goal_name: str = None, goal_description: str = None, goal_target_amount: float = None, goal_current_amount: float = None):
        """
        This tool edits the details of a specific goal for a user.

        Args:
            user_id (str): The ID of the user whose goal is to be edited.
            goal_id (str): The ID of the goal to be edited.
            goal_name (str, optional): The new name of the goal.
            goal_description (str, optional): The new description of the goal.
            goal_target_amount (float, optional): The new target amount for the goal.
            goal_current_amount (float, optional): The new current amount saved towards the goal.

        Returns:
            dict: A dictionary containing the status of the goal edit.
                - status: A message indicating whether the goal was edited successfully.

        Raises:
            Exception: If there is an error during the API request.

        Example:
            {
                "status": "success"
            }
        """
        def _edit_goal(user_id: str, goal_id: str, goal_name: str = None, goal_description: str = None, goal_target_amount: float = None, goal_current_amount: float = None):
            try:
                payload = {
                    GoalConstants.KEY_GOAL_ID.value: goal_id
                }

                if goal_name is not None:
                    payload[GoalConstants.KEY_GOAL_NAME.value] = goal_name
                if goal_description is not None:
                    payload[GoalConstants.KEY_GOAL_DESCRIPTION.value] = goal_description
                if goal_target_amount is not None:
                    payload[GoalConstants.KEY_GOAL_TARGET_AMOUNT.value] = goal_target_amount
                if goal_current_amount is not None:
                    payload[GoalConstants.KEY_GOAL_CURRENT_AMOUNT.value] = goal_current_amount

                api_request = APIRequest(
                    http_method=APIConstants.KEY_PUT_METHOD.value,
                    endpoint=f"/goals/{user_id}",
                    payload=payload
                )
                response = api_request.execute()
                return response
            except Exception as e:
                logger.error(f"Error in edit goal tool, {str(e)}")
                raise e

        return _edit_goal(user_id, goal_id, goal_name, goal_description, goal_target_amount, goal_current_amount)


    @tool
    def add_amount_to_goal(self, user_id: str, goal_id: str, amount_to_add: float):
        """
        This tool adds a specified amount to the current amount of a specific goal for a user.

        Args:
            user_id (str): The ID of the user whose goal is to be updated.
            goal_id (str): The ID of the goal to which the amount is to be added
            amount_to_add (float): The amount to be added to the current amount of the goal.

        Returns:
            dict: A dictionary containing the status of the amount addition.
                - status: A message indicating whether the amount was added successfully.

        Raises:
            Exception: If there is an error during the API request.

        Example:
            {
                "status": "success"
            }
        """
        def _add_amount_to_goal(user_id: str, goal_id: str, amount_to_add: float):
            try:
                api_request = APIRequest(
                    http_method=APIConstants.KEY_PATCH_METHOD.value,
                    endpoint=f"/goals/{user_id}",
                    payload={
                        GoalConstants.KEY_GOAL_ID.value: goal_id,
                        GoalConstants.KEY_GOAL_CURRENT_AMOUNT.value: amount_to_add
                    }
                )
                response = api_request.execute()
                return response
            except Exception as e:
                logger.error(f"Error in add amount to goal tool, {str(e)}")
                raise e
            
        return _add_amount_to_goal(user_id, goal_id, amount_to_add)