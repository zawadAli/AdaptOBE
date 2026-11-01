from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User, UserRole
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import chat_service
from app.services.exceptions import LLMGenerationError, RateLimitError

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

# Every signed-in role may use the assistant; what each role can *see* through
# it is enforced inside chat_tools, not here.
AnyUser = Depends(
    require_roles(UserRole.super_admin, UserRole.sub_admin, UserRole.faculty, UserRole.student)
)


@router.post("", response_model=ChatResponse)
async def send_message(
    data: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = AnyUser,
):
    try:
        return await chat_service.chat(db, current_user, data)
    except RateLimitError as exc:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(exc)) from exc
    except LLMGenerationError as exc:
        # The real cause (API/network detail) is logged server-side, not echoed.
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI assistant is unavailable right now. Please try again later.",
        ) from exc
