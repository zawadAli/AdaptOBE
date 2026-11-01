"""Curriculum catalog: fidelity to the source documents, and the read-only API."""

import pytest

from app.core import curriculum
from app.models.user import User, UserRole
from app.schemas.department import DepartmentCreate
from app.schemas.program import ProgramCreate
from app.services import department_service, program_service
from tests.conftest import auth_header

PREFIX = {"BSCS": "CS-", "BSSE": "SE-", "BSAI": "AI-"}


# ---- Fidelity to the curriculum documents -----------------------------------

@pytest.mark.parametrize("program", sorted(curriculum.CURRICULA))
def test_semester_credit_totals_match_documents(program):
    """Planned courses + 3 credits per elective slot == the document's printed
    'Total Credits for Semester' line, for every semester. Catches any
    mistyped credit, missing course or misplaced semester."""
    courses = curriculum.CURRICULA[program]
    for semester, expected in curriculum.SEMESTER_CREDIT_TOTALS[program].items():
        planned = sum(
            c.credit_hours
            for c in courses
            if c.category == "core" and c.alternative_to is None and c.semesters == (semester,)
        )
        slots = curriculum.ELECTIVE_SLOTS[program].get(semester, 0)
        assert planned + 3 * slots == expected, f"{program} semester {semester}"


@pytest.mark.parametrize("program", sorted(curriculum.CURRICULA))
def test_codes_unique_and_prefixed(program):
    codes = [c.code for c in curriculum.CURRICULA[program]]
    assert len(codes) == len(set(codes))
    assert all(code.startswith(PREFIX[program]) for code in codes)
    assert not any("xxx" in code for code in codes)  # elective slots aren't courses


@pytest.mark.parametrize("program", sorted(curriculum.CURRICULA))
def test_semesters_and_categories_valid(program):
    for course in curriculum.CURRICULA[program]:
        assert course.semesters and all(1 <= s <= 8 for s in course.semesters)
        assert course.category in {"core", "elective"}
        assert (course.group is not None) == (course.category == "elective")
        theory, lab = (int(part) for part in course.breakdown.split("+"))
        assert course.credit_hours in (theory + lab, theory + lab + 1)  # DLD-style 4 (3+1)


def test_elective_slots_have_courses_to_fill_them():
    for program, slots in curriculum.ELECTIVE_SLOTS.items():
        for semester in slots:
            assert any(
                c.category == "elective" and semester in c.semesters
                for c in curriculum.CURRICULA[program]
            ), f"{program} semester {semester} has slots but no electives"


def test_thesis_is_alternative_to_fyp():
    bsai = {c.code: c for c in curriculum.BSAI}
    assert bsai["AI-657"].alternative_to == "AI-655"
    assert bsai["AI-658"].alternative_to == "AI-656"


def test_bsds_uses_bscs_catalog_and_unknown_has_none():
    assert curriculum.catalog_source("BSDS") == "BSCS"
    assert curriculum.catalog_for("BSDS") is curriculum.BSCS
    assert curriculum.catalog_source("BSXX-TEST") is None
    assert curriculum.catalog_for("BSXX-TEST") == ()


# ---- API ---------------------------------------------------------------------

async def _program(db_session, department, code):
    """The real seeded programme if this DB has it, else a temporary one."""
    existing = await program_service.get_program_by_code(db_session, code)
    if existing:
        return existing
    return await program_service.create_program(
        db_session,
        ProgramCreate(dept_id=department.id, code=code, name=f"{code} test", total_semesters=8),
        current_user=User(role=UserRole.faculty),
    )


async def test_faculty_gets_bsds_catalog_from_bscs(client, db_session, department, faculty):
    bsds = await _program(db_session, department, "BSDS")
    resp = await client.get(f"/api/v1/curriculum/{bsds.id}", headers=auth_header(faculty))
    assert resp.status_code == 200
    body = resp.json()
    assert body["program_code"] == "BSDS"
    assert body["source_program_code"] == "BSCS"
    assert len(body["courses"]) == len(curriculum.BSCS)
    first = body["courses"][0]
    assert first == {
        "code": "CS-351", "name": "Programming Fundamentals", "credit_hours": 4,
        "breakdown": "3+1", "semesters": [1], "category": "core", "group": None,
        "alternative_to": None,
    }


async def test_programme_without_catalog_returns_empty(client, program, faculty):
    resp = await client.get(f"/api/v1/curriculum/{program.id}", headers=auth_header(faculty))
    assert resp.status_code == 200
    assert resp.json()["courses"] == []
    assert resp.json()["source_program_code"] is None


async def test_catalog_entry_creates_a_course(client, db_session, department, program, faculty):
    """A catalog entry is shaped exactly like the existing course-create body.

    Posted to the isolated test programme rather than the real BSAI one, so a
    real 'AI-555' offering in the dev DB can never make this test 409."""
    bsai = await _program(db_session, department, "BSAI")
    catalog = (await client.get(f"/api/v1/curriculum/{bsai.id}", headers=auth_header(faculty))).json()
    entry = next(c for c in catalog["courses"] if c["code"] == "AI-555")
    resp = await client.post(
        "/api/v1/courses",
        json={
            "program_id": program.id, "code": entry["code"], "name": entry["name"],
            "credit_hours": entry["credit_hours"], "semester": entry["semesters"][0],
        },
        headers=auth_header(faculty),
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Machine Learning"


async def test_students_cannot_read_catalog(client, program, make_student):
    student = await make_student("cat")
    resp = await client.get(f"/api/v1/curriculum/{program.id}", headers=auth_header(student))
    assert resp.status_code == 403


async def test_sub_admin_scoped_to_own_department(client, db_session, sub_admin):
    other_dept = await department_service.create_department(
        db_session, DepartmentCreate(name="Other Dept", code="OTHER-TEST")
    )
    foreign = await program_service.create_program(
        db_session,
        ProgramCreate(dept_id=other_dept.id, code="BSXX-TEST", name="Foreign", total_semesters=8),
        current_user=User(role=UserRole.faculty),
    )
    resp = await client.get(f"/api/v1/curriculum/{foreign.id}", headers=auth_header(sub_admin))
    assert resp.status_code == 403


async def test_unknown_programme_is_404(client, faculty):
    resp = await client.get("/api/v1/curriculum/999999999", headers=auth_header(faculty))
    assert resp.status_code == 404
