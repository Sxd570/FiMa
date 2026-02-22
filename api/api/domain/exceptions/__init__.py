from fastapi import HTTPException
from starlette import status

class BudgetNotFoundException(HTTPException):
    def __init__(self, detail: str = "Budget not found."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class GoalNotFoundException(HTTPException):
    def __init__(self, detail: str = "Goal not found."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class TransactionNotFoundException(HTTPException):
    def __init__(self, detail: str = "Transaction not found."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class InvalidTimePeriodException(HTTPException):
    def __init__(self, detail: str = "Invalid time period specified."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = "User not found."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class InvalidCredentialsException(HTTPException):
    def __init__(self, detail: str = "Invalid credentials."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )

class UserAlreadyExistsException(HTTPException):
    def __init__(self, detail: str = "User already exists."):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )
