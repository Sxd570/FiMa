from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any


class Conversation(BaseModel):
    conversation_id: str = Field(..., description="Unique identifier for the conversation")
    title: Optional[str] = Field(None, description="Title of the conversation")
    created_at: Optional[str] = Field(None, description="Timestamp when the conversation was created")
    updated_at: Optional[str] = Field(None, description="Timestamp when the conversation was last updated")
    last_message_at: Optional[str] = Field(None, description="Timestamp of the last message in the conversation")
    total_token_used: Optional[int] = Field(0, description="Total tokens used in the conversation")
    status: Optional[str] = Field("active", description="Status of the conversation (e.g., active, archived)")


class ConversationDBResponse(BaseModel):
    conversations: Optional[List[Conversation]] = Field(None, description="List of conversations")