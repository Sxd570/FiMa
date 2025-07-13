from abc import ABC, abstractmethod

class AuthInterface(ABC):
    @abstractmethod
    def login(self, payload) -> dict:
        """
        Authenticate a user and return a response containing user details and token.
        """
        pass

    @abstractmethod
    def signup(self, payload) -> dict:
        """
        Register a new user and return a response containing user details and token.
        """
        pass