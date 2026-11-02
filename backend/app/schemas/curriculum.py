from pydantic import BaseModel

from app.schemas.clo import CLORead


class CatalogOffering(BaseModel):
    """An existing course row for this catalog entry, by anyone in the programme."""

    semester: int
    owner_name: str
    is_mine: bool


class CatalogCourseRead(BaseModel):
    code: str
    name: str
    credit_hours: int
    breakdown: str
    semesters: list[int]
    category: str  # "core" | "elective"
    group: str | None
    alternative_to: str | None
    # Semesters where this course already exists in the programme -- creating it
    # again there would be a duplicate, whoever owns the existing one.
    offerings: list[CatalogOffering]
    # How many CLOs the curriculum document lists for this course (0 = none).
    clo_count: int


class CurriculumRead(BaseModel):
    program_id: int
    program_code: str
    # The programme whose catalog this is, when it differs (BSDS -> BSCS); None
    # when no catalog exists, in which case `courses` is empty.
    source_program_code: str | None
    courses: list[CatalogCourseRead]


class CurriculumCloRead(BaseModel):
    """One CLO from the curriculum document, as offered for a specific course."""

    index: int  # position in the document's list; used to import a subset
    title: str
    description: str
    bloom_level: str
    already_added: bool  # the course already has a CLO with this statement


class CourseCurriculumClos(BaseModel):
    course_id: int
    clos: list[CurriculumCloRead]


class ImportCurriculumClosRequest(BaseModel):
    # Which CLOs (by `index`) to add; omit to add every one not yet added.
    indices: list[int] | None = None


class ImportCurriculumClosResponse(BaseModel):
    created: list[CLORead]
    skipped: int  # requested CLOs the course already had
