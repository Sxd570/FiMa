from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any
from datetime import datetime


class Conversation(BaseModel):
    conversation_id: str = Field(..., description="Unique identifier for the conversation")
    title: Optional[str] = Field(None, description="Title of the conversation")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the conversation was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the conversation was last updated")
    last_message_at: Optional[datetime] = Field(None, description="Timestamp of the last message in the conversation")
    total_token_used: Optional[int] = Field(0, description="Total tokens used in the conversation")
    status: Optional[str] = Field("active", description="Status of the conversation (e.g., active, archived)")


class ListConversationDBResponse(BaseModel):
    conversations: Optional[List[Conversation]] = Field(None, description="List of conversations")


class ListConversationDBPayload(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")


class ListConversationsPayload(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")


class ListConversationsDBRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")


class ListConversationResponse(BaseModel):
    conversations: Optional[List[Conversation]] = Field(None, description="List of conversations")


class GetConversationPayload(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    conversation_id: str = Field(..., description="Unique identifier for the conversation")


class GetConversationDBRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    conversation_id: str = Field(..., description="Unique identifier for the conversation")


class MessageMetadata(BaseModel):
    token_used: Optional[int] = Field(None, description="Number of tokens used for this message")
    model: Optional[str] = Field(None, description="Model used to generate the message")
    temperature: Optional[float] = Field(None, description="Sampling temperature used for the message generation")

class Message(BaseModel):
    message_id: str = Field(..., description="Unique identifier for the message")
    conversation_id: str = Field(..., description="Unique identifier for the conversation")
    sender: str = Field(..., description="Sender of the message (e.g., user, agent)")
    content_type: str = Field(..., description="Type of content (e.g., html, react)")
    content: Any = Field(..., description="Content of the message")
    created_at: datetime = Field(..., description="Timestamp when the message was created")
    metadata: Optional[MessageMetadata] = Field(None, description="Additional metadata for the message")



class GetConversationDBResponse(BaseModel):
    message_details: Optional[List[Message]] = Field(None, description="List of messages in the conversation")

class GetConversationResponse(BaseModel):
    message_details: Optional[List[Message]] = Field(None, description="List of messages in the conversation")