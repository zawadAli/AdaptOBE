from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User, UserRole
from app.schemas.curriculum import CurriculumRead
from app.services import curriculum_service
from app.services.exceptions import NotFoundError, PermissionDeniedError

router = APIRouter(prefix="/api/v1/curriculum", tags=["curriculum"])

# Same audience as course creation: faculty, and sub-admins for their department.
FacultyOrSubAdmin = Depends(require_roles(UserRole.faculty, UserRole.sub_admin))


@router.get("/{program_id}", response_model=CurriculumRead)
async def get_curriculum(
    program_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = FacultyOrSubAdmin,
):
    try:
        return await curriculum_service.get_curriculum(db, program_id, current_user)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except PermissionDeniedError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
