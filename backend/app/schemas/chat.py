from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.services.chat_guard import MAX_HISTORY_TURN_CHARS, MAX_HISTORY_TURNS, MAX_MESSAGE_CHARS


class ChatTurn(BaseModel):
    # Only plain user/assistant text is accepted from the client. "system" and
    # "tool" turns are rejected so a caller can't forge instructions or fake
    # tool results into the conversation.
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=MAX_HISTORY_TURN_CHARS)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=MAX_MESSAGE_CHARS)
    history: list[ChatTurn] = Field(default_factory=list, max_length=MAX_HISTORY_TURNS)

    @field_validator("message")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("message must not be blank")
        return value


class ChatResponse(BaseModel):
    reply: str
    sources: list[str]  # titles of the help articles the answer drew on
    tools_used: list[str]  # names of the read-only data tools that ran
    degraded: bool = False  # True when the AI was unavailable and help text was returned instead
