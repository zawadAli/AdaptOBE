"""Curriculum catalog lookups (read-only reference data from app/core/curriculum.py)."""

from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.curriculum import catalog_for, catalog_source
from app.models.user import User
from app.schemas.curriculum import CatalogCourseRead, CurriculumRead
from app.services import program_service


async def get_curriculum(db: AsyncSession, program_id: int, user: User) -> CurriculumRead:
    program = await program_service.get_program_scoped(db, program_id, user)
    return CurriculumRead(
        program_id=program.id,
        program_code=program.code,
        source_program_code=catalog_source(program.code),
        courses=[CatalogCourseRead(**asdict(course)) for course in catalog_for(program.code)],
    )
