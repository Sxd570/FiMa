from abc import ABC, abstractmethod


class BudgetInterface(ABC):
    @abstractmethod
    def get_total_budget(self, user_id: str) -> float:
        """
        Get the total budget for a user.
        
        :param user_id: The ID of the user.
        :return: The total budget amount.
        """
        pass

    @abstractmethod
    def get_total_spent(self, user_id: str) -> float:
        """
        Get the total amount spent by a user.
        
        :param user_id: The ID of the user.
        :return: The total amount spent.
        """
        pass