from abc import ABC, abstractmethod


class TransactionInterface(ABC):
    @abstractmethod
    def get_transactions(self, db_request):
        """
        Fetch transactions based on the provided request.
        
        :param db_request: An instance of GetTransactionDBRequest containing user ID and filters.
        :return: A list of transactions matching the request criteria.
        """
        pass

    @abstractmethod
    def create_transaction(self, db_request):
        """
        Create a new transaction based on the provided request.
        
        :param db_request: An instance of CreateTransactionDBRequest containing transaction details.
        :return: The created transaction details.
        """
        pass