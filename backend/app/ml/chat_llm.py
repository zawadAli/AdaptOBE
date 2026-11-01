"""Groq chat-completion calls for the AdaptOBE assistant (chatbot).

Same lazy-`AsyncGroq` pattern and model as `clo_generator.py` /
`question_extractor.py`, but conversational and with tool calling. Importing
this module never needs an API key; any failure becomes `LLMGenerationError`.
"""

from dataclasses import dataclass, field

from app.core.config import settings
from app.services.exceptions import LLMGenerationError

#: Same model the rest of the codebase already uses on this Groq account.
MODEL_NAME = "openai/gpt-oss-120b"
MAX_COMPLETION_TOKENS = 900
TEMPERATURE = 0.2

_client = None


def get_client():
    """Return the shared AsyncGroq client, constructing it on first use."""
    global _client
    if _client is None:
        if not settings.groq_api_key:
            raise LLMGenerationError(
                "GROQ_API_KEY is not configured -- set it in backend/.env to use the assistant."
            )
        from groq import AsyncGroq

        _client = AsyncGroq(api_key=settings.groq_api_key)
    return _client


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: str  # raw JSON string, exactly as the model produced it


@dataclass
class AssistantTurn:
    content: str | None
    tool_calls: list[ToolCall] = field(default_factory=list)

    def as_message(self) -> dict:
        """The assistant message to echo back to the API in the next round."""
        message: dict = {"role": "assistant", "content": self.content or ""}
        if self.tool_calls:
            message["tool_calls"] = [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {"name": call.name, "arguments": call.arguments},
                }
                for call in self.tool_calls
            ]
        return message


async def acomplete(messages: list[dict], tools: list[dict] | None) -> AssistantTurn:
    """One chat-completion round. Raises LLMGenerationError on any failure."""
    client = get_client()

    kwargs = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": TEMPERATURE,
        "max_completion_tokens": MAX_COMPLETION_TOKENS,
    }
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    try:
        response = await client.chat.completions.create(**kwargs)
    except Exception as exc:  # noqa: BLE001 - any SDK/network failure becomes one typed error
        raise LLMGenerationError(f"Assistant request failed: {exc}") from exc

    if not response.choices:
        raise LLMGenerationError("The AI returned an empty response")

    message = response.choices[0].message
    calls = [
        ToolCall(id=call.id, name=call.function.name, arguments=call.function.arguments or "{}")
        for call in (getattr(message, "tool_calls", None) or [])
    ]
    return AssistantTurn(content=message.content, tool_calls=calls)
