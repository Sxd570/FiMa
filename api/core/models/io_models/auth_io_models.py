from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any

class LoginRequest(BaseModel):
    user_email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")


class LoginPayload(BaseModel):
    user_email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")


class SignupRequest(BaseModel):
    user_email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")
    username: str = Field(..., description="Username of the user")


class SignupPayload(BaseModel):
    user_email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")
    username: str = Field(..., description="Username of the user")


class SignupDBRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    user_email: str = Field(..., description="Email of the user")
    username: str = Field(..., description="Username of the user")
