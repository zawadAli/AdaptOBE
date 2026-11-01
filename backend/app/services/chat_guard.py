"""Pure security rules for the chatbot -- no DB, no LLM, no FastAPI.

The chatbot's real defence against prompt injection is architectural (tools are
read-only, allowlisted, role-gated and take the caller's identity from the JWT,
never from the model -- see `chat_tools.py`). The rules here are the extra
belts-and-braces around that: bounded input, a per-user rate limit, strict
validation of the only argument the model may supply, and clear delimiting of
any text that came from the database or the help corpus so the model is told to
treat it as data rather than as instructions.
"""

import re
import threading
import time
from collections import defaultdict, deque

from app.services.exceptions import RateLimitError

MAX_MESSAGE_CHARS = 1000
MAX_HISTORY_TURNS = 10
MAX_TOOL_ROUNDS = 3
MAX_REPLY_CHARS = 4000
#: History echoes the assistant's own earlier replies back, so a turn may be as
#: long as a reply -- any shorter and a normal conversation would be rejected.
MAX_HISTORY_TURN_CHARS = MAX_REPLY_CHARS

#: Per-user quota. In-memory and per-process: correct for this single-process
#: FYP deployment; a multi-worker production setup would move it to Redis.
RATE_LIMIT_MESSAGES = 20
RATE_LIMIT_WINDOW_SECONDS = 300

# Course codes in this app look like "SE-301", "CS_101", "DEMO-501".
_COURSE_CODE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_\- ]{0,49}$")


class RateLimiter:
    """Sliding-window limiter keyed by user id."""

    def __init__(self, limit: int = RATE_LIMIT_MESSAGES, window: float = RATE_LIMIT_WINDOW_SECONDS):
        self.limit = limit
        self.window = window
        self._hits: dict[int, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, user_id: int, now: float | None = None) -> None:
        """Record one request, or raise RateLimitError if over quota."""
        now = time.monotonic() if now is None else now
        with self._lock:
            hits = self._hits[user_id]
            while hits and now - hits[0] >= self.window:
                hits.popleft()
            if len(hits) >= self.limit:
                retry_in = int(self.window - (now - hits[0])) + 1
                raise RateLimitError(
                    f"Too many chat messages. Please wait about {retry_in} seconds and try again."
                )
            hits.append(now)

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()


rate_limiter = RateLimiter()


def clean_course_code(raw) -> str | None:
    """Normalise the one model-supplied argument; None if it isn't a plausible code.

    Rejecting anything odd here means a jailbroken model can't smuggle SQL,
    paths, or other payloads through a tool argument -- the value is only ever
    compared for equality against the caller's own course codes anyway.
    """
    if not isinstance(raw, str):
        return None
    value = raw.strip()
    if not _COURSE_CODE_RE.match(value):
        return None
    return value


def course_code_key(code: str) -> str:
    """Comparison key so 'se301', 'SE-301' and 'SE 301' all match."""
    return re.sub(r"[^a-z0-9]", "", code.lower())


def wrap_untrusted(label: str, text: str) -> str:
    """Fence text that came from the DB / help corpus / a tool.

    The system prompt tells the model that anything inside these markers is
    reference data and that instructions found inside it must be ignored.
    Any marker-lookalikes inside the text are neutralised so the data can't
    "close" the fence early and append its own instructions.
    """
    safe = text.replace("<<<", "‹‹‹").replace(">>>", "›››")
    return f"<<<{label}\n{safe}\n>>>"


def clip_reply(text: str) -> str:
    text = (text or "").strip()
    if len(text) > MAX_REPLY_CHARS:
        return text[:MAX_REPLY_CHARS].rstrip() + "…"
    return text
