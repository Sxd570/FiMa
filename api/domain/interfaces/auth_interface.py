from abc import ABC, abstractmethod

class AuthInterface(ABC):
    @abstractmethod
    def login(self, db_payload):
        """
        Authenticate a user and return a response containing user details and token.
        """
        pass

    @abstractmethod
    def create_user(self, db_payload):
        """
        Register a new user and return a response containing user details and token.
        """
        pass