from abc import ABC, abstractmethod


class GoalsInterface(ABC):
    @abstractmethod
    def get_total_goals_count(self, user_id):
        """
        Get the total number of goals for a user.
        
        :param user_id: The ID of the user.
        :return: The total number of goals.
        """
        pass

    @abstractmethod
    def get_total_goals_completed(self, user_id):
        """
        Get the total number of completed goals for a user.
        
        :param user_id: The ID of the user.
        :return: The total number of completed goals.
        """
        pass

    @abstractmethod
    def get_total_amount_saved(self, user_id):
        """
        Get the total amount saved by a user across all goals.
        
        :param user_id: The ID of the user.
        :return: The total amount saved.
        """
        pass

    @abstractmethod
    def get_total_goals_amount(self, user_id):
        """
        Get the total amount of all goals for a user.
        
        :param user_id: The ID of the user.
        :return: The total amount of all goals.
        """
        pass

    @abstractmethod
    def get_goal_details(self, user_id, limit=None, offset=None):
        """
        Get the details of a specific goal for a user.

        :param user_id: The ID of the user.
        :return: The details of the goal.
        """
        pass

    @abstractmethod
    def create_goal(self, goal):
        """
        Create a new goal for a user.

        :param user_id: The ID of the user.
        :param goal_data: The data for the new goal.
        :return: The ID of the created goal.
        """
        pass

    @abstractmethod
    def edit_goal(self, user_id, goal):
        """
        Edit an existing goal for a user.

        :param user_id: The ID of the user.
        :param goal: The updated data for the goal.
        :return: A success message or the updated goal details.
        """
        pass

    @abstractmethod
    def delete_goal(self, user_id, goal_id):
        """
        Delete a goal for a user.

        :param user_id: The ID of the user.
        :param goal_id: The ID of the goal to be deleted.
        :return: A success message or an error message if the goal does not exist.
        """
        pass

    @abstractmethod
    def add_amount_to_goal(self, user_id, goal_id, amount_to_add):
        """
        Add an amount to a specific goal for a user.

        :param user_id: The ID of the user.
        :param goal_id: The ID of the goal to which the amount will be added.
        :param amount: The amount to be added to the goal.
        :return: A success message or an error message if the goal does not exist.
        """
        pass