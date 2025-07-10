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