from pydantic import BaseModel


class CatalogCourseRead(BaseModel):
    code: str
    name: str
    credit_hours: int
    breakdown: str
    semesters: list[int]
    category: str  # "core" | "elective"
    group: str | None
    alternative_to: str | None


class CurriculumRead(BaseModel):
    program_id: int
    program_code: str
    # The programme whose catalog this is, when it differs (BSDS -> BSCS); None
    # when no catalog exists, in which case `courses` is empty.
    source_program_code: str | None
    courses: list[CatalogCourseRead]
