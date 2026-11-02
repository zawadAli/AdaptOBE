"""Curriculum catalog lookups (read-only reference data from app/core/curriculum.py),
plus adding a course's curriculum CLOs (app/core/curriculum_clos.py) to it."""

from collections import defaultdict
from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.curriculum import catalog_for, catalog_source
from app.core.curriculum_clos import CURRICULUM_CLOS, CatalogCLO
from app.models.course import Course
from app.models.user import User
from app.schemas.clo import CLOCreate, CLORead
from app.schemas.curriculum import (
    CatalogCourseRead,
    CatalogOffering,
    CourseCurriculumClos,
    CurriculumCloRead,
    CurriculumRead,
    ImportCurriculumClosRequest,
    ImportCurriculumClosResponse,
)
from app.services import clo_service, course_service, program_service
from app.services.exceptions import ValidationError


def _clos_for_code(program_code: str, course_code: str) -> tuple[CatalogCLO, ...]:
    """Curriculum CLOs for a course code in a programme (BSDS reads BSCS's)."""
    source = catalog_source(program_code)
    if source is None:
        return ()
    key = course_service.code_key(course_code)
    for code, clos in CURRICULUM_CLOS.get(source, {}).items():
        if course_service.code_key(code) == key:
            return clos
    return ()


async def _offerings_by_code(
    db: AsyncSession, program_id: int, user: User
) -> dict[str, list[CatalogOffering]]:
    """Existing courses in the programme, keyed by `code_key` -- the same
    normalisation the duplicate check uses, so 'Already offered' in the picker
    means exactly 'creating this would be rejected'."""
    rows = await db.execute(
        select(Course.code, Course.semester, Course.owner_faculty_id, User.full_name)
        .join(User, User.id == Course.owner_faculty_id)
        .where(Course.program_id == program_id)
        .order_by(Course.semester)
    )
    offerings: dict[str, list[CatalogOffering]] = defaultdict(list)
    for code, semester, owner_id, owner_name in rows:
        offerings[course_service.code_key(code)].append(
            CatalogOffering(semester=semester, owner_name=owner_name, is_mine=owner_id == user.id)
        )
    return offerings


async def get_curriculum(db: AsyncSession, program_id: int, user: User) -> CurriculumRead:
    program = await program_service.get_program_scoped(db, program_id, user)
    offerings = await _offerings_by_code(db, program.id, user)
    return CurriculumRead(
        program_id=program.id,
        program_code=program.code,
        source_program_code=catalog_source(program.code),
        courses=[
            CatalogCourseRead(
                **asdict(course),
                offerings=offerings.get(course_service.code_key(course.code), []),
                clo_count=len(_clos_for_code(program.code, course.code)),
            )
            for course in catalog_for(program.code)
        ],
    )


# ---- Curriculum CLOs for a specific course ------------------------------------

def _same_statement(text: str) -> str:
    return " ".join(text.lower().split())


async def _course_and_catalog_clos(db: AsyncSession, course_id: int, user: User):
    course = await course_service.get_course_for_user(db, course_id, user)
    program = await program_service.get_program(db, course.program_id)
    return course, _clos_for_code(program.code, course.code)


async def get_course_clos(db: AsyncSession, course_id: int, user: User) -> CourseCurriculumClos:
    course, catalog = await _course_and_catalog_clos(db, course_id, user)
    existing = {_same_statement(clo.description) for clo in await clo_service.list_clos(db, course.id)}
    return CourseCurriculumClos(
        course_id=course.id,
        clos=[
            CurriculumCloRead(
                index=i,
                title=clo.title,
                description=clo.description,
                bloom_level=clo.bloom_level,
                already_added=_same_statement(clo.description) in existing,
            )
            for i, clo in enumerate(catalog)
        ],
    )


def _pick_code(preferred_number: int, taken: set[str]) -> str:
    """Keep the document's numbering (CLO-3 stays CLO-3) unless that code is
    already used in the course, then take the next free CLO-n."""
    preferred = f"CLO-{preferred_number}"
    if course_service.code_key(preferred) not in taken:
        return preferred
    n = 1
    while course_service.code_key(f"CLO-{n}") in taken:
        n += 1
    return f"CLO-{n}"


async def import_course_clos(
    db: AsyncSession, course_id: int, data: ImportCurriculumClosRequest, user: User
) -> ImportCurriculumClosResponse:
    """Add curriculum CLOs to a course through the normal CLO creation path
    (so each gets its embedding for the manual CLO->PLO mapping step).

    Deliberately creates no CLO->PLO mappings: mapping stays a faculty
    decision. Re-running is safe -- CLOs the course already has are skipped.
    """
    course, catalog = await _course_and_catalog_clos(db, course_id, user)

    indices = range(len(catalog)) if data.indices is None else sorted(set(data.indices))
    out_of_range = [i for i in indices if not 0 <= i < len(catalog)]
    if out_of_range:
        raise ValidationError(f"Unknown curriculum CLO index: {out_of_range}")

    existing = await clo_service.list_clos(db, course.id)
    statements = {_same_statement(clo.description) for clo in existing}
    codes = {course_service.code_key(clo.code) for clo in existing}

    created: list[CLORead] = []
    skipped = 0
    for i in indices:
        entry = catalog[i]
        if _same_statement(entry.description) in statements:
            skipped += 1
            continue
        code = _pick_code(i + 1, codes)
        clo = await clo_service.create_clo(
            db,
            course.id,
            CLOCreate(
                code=code,
                title=entry.title,
                description=entry.description,
                bloom_level=entry.bloom_level,
            ),
            user,
        )
        codes.add(course_service.code_key(code))
        statements.add(_same_statement(entry.description))
        created.append(CLORead.model_validate(clo))

    return ImportCurriculumClosResponse(created=created, skipped=skipped)
