"""Curriculum CLOs: data integrity, preview, import into a course, and access rules.

Test courses use semester 2 for catalog codes that the curriculum places in a
later semester, so they can never collide with real courses in the dev DB.
"""

from sqlalchemy import func, select

from app.core.curriculum import CURRICULA
from app.core.curriculum_clos import CURRICULUM_CLOS
from app.models.mapping import CloPloMapping
from app.models.user import User, UserRole
from app.schemas.clo import BLOOM_LEVELS
from app.schemas.course import CourseCreate
from app.schemas.program import ProgramCreate
from app.services import course_service, program_service
from tests.conftest import auth_header

OS_CLOS = CURRICULUM_CLOS["BSCS"]["CS-553"]


# ---- Data integrity ------------------------------------------------------------

def test_every_entry_belongs_to_a_catalog_course():
    for program, courses in CURRICULUM_CLOS.items():
        catalog_codes = {c.code for c in CURRICULA[program]}
        assert set(courses) <= catalog_codes, program


def test_clo_fields_are_valid():
    for program, courses in CURRICULUM_CLOS.items():
        for code, clos in courses.items():
            assert clos, f"{program} {code} has an empty CLO list"
            statements = [c.description for c in clos]
            assert len(statements) == len(set(statements)), f"{program} {code} repeats a CLO"
            for clo in clos:
                assert clo.bloom_level in BLOOM_LEVELS
                assert 0 < len(clo.title) <= 255
                assert len(clo.description) >= 8
                assert not clo.description.lower().startswith("as per guidelines")


# ---- Helpers -------------------------------------------------------------------

async def _bscs(db_session, department):
    existing = await program_service.get_program_by_code(db_session, "BSCS")
    if existing:
        return existing
    return await program_service.create_program(
        db_session,
        ProgramCreate(dept_id=department.id, code="BSCS", name="BSCS test", total_semesters=8),
        current_user=User(role=UserRole.faculty),
    )


async def _os_course(db_session, department, faculty, code="CS-553"):
    bscs = await _bscs(db_session, department)
    return await course_service.create_course(
        db_session,
        CourseCreate(program_id=bscs.id, code=code, name="Operating Systems", credit_hours=4, semester=2),
        faculty,
    )


# ---- Preview & import ------------------------------------------------------------

async def test_preview_lists_curriculum_clos(client, db_session, department, faculty):
    course = await _os_course(db_session, department, faculty)
    resp = await client.get(f"/api/v1/courses/{course.id}/curriculum-clos", headers=auth_header(faculty))
    assert resp.status_code == 200
    clos = resp.json()["clos"]
    assert [c["index"] for c in clos] == list(range(len(OS_CLOS)))
    assert [c["description"] for c in clos] == [c.description for c in OS_CLOS]
    assert not any(c["already_added"] for c in clos)


async def test_import_adds_clos_with_document_numbering_and_no_mappings(
    client, db_session, department, faculty
):
    course = await _os_course(db_session, department, faculty)
    resp = await client.post(
        f"/api/v1/courses/{course.id}/curriculum-clos/import", json={}, headers=auth_header(faculty)
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["skipped"] == 0
    created = body["created"]
    assert [c["code"] for c in created] == [f"CLO-{i}" for i in range(1, len(OS_CLOS) + 1)]
    assert [c["bloom_level"] for c in created] == [c.bloom_level for c in OS_CLOS]
    assert [c["title"] for c in created] == [c.title for c in OS_CLOS]

    # They show up in the course's CLO list like any manually added CLO.
    listed = await client.get(f"/api/v1/courses/{course.id}/clos", headers=auth_header(faculty))
    assert {c["id"] for c in listed.json()} == {c["id"] for c in created}

    # Mapping to PLOs is left to the faculty -- none are created.
    mappings = await db_session.scalar(
        select(func.count()).select_from(CloPloMapping).where(
            CloPloMapping.clo_id.in_([c["id"] for c in created])
        )
    )
    assert mappings == 0


async def test_import_is_idempotent(client, db_session, department, faculty):
    course = await _os_course(db_session, department, faculty)
    url = f"/api/v1/courses/{course.id}/curriculum-clos"
    await client.post(f"{url}/import", json={}, headers=auth_header(faculty))

    again = (await client.post(f"{url}/import", json={}, headers=auth_header(faculty))).json()
    assert again["created"] == []
    assert again["skipped"] == len(OS_CLOS)

    preview = (await client.get(url, headers=auth_header(faculty))).json()
    assert all(c["already_added"] for c in preview["clos"])


async def test_import_selected_subset_keeps_its_number(client, db_session, department, faculty):
    course = await _os_course(db_session, department, faculty)
    resp = await client.post(
        f"/api/v1/courses/{course.id}/curriculum-clos/import",
        json={"indices": [1]},
        headers=auth_header(faculty),
    )
    created = resp.json()["created"]
    assert len(created) == 1
    assert created[0]["code"] == "CLO-2"
    assert created[0]["description"] == OS_CLOS[1].description


async def test_import_avoids_codes_already_used_by_manual_clos(client, db_session, department, faculty):
    course = await _os_course(db_session, department, faculty)
    manual = await client.post(
        f"/api/v1/courses/{course.id}/clos",
        json={"code": "CLO-1", "title": "My own CLO", "description": "Something the instructor wrote.",
              "bloom_level": "Apply"},
        headers=auth_header(faculty),
    )
    assert manual.status_code == 201  # manual CLO entry still works alongside

    created = (await client.post(
        f"/api/v1/courses/{course.id}/curriculum-clos/import", json={}, headers=auth_header(faculty)
    )).json()["created"]
    listed = (await client.get(f"/api/v1/courses/{course.id}/clos", headers=auth_header(faculty))).json()
    codes = [c["code"] for c in listed]
    assert len(codes) == len(set(codes)) == len(OS_CLOS) + 1
    assert "CLO-1" not in [c["code"] for c in created]  # the manual CLO-1 is untouched


async def test_respelled_course_code_still_finds_clos(client, db_session, department, faculty):
    course = await _os_course(db_session, department, faculty, code="cs 553")
    clos = (await client.get(f"/api/v1/courses/{course.id}/curriculum-clos", headers=auth_header(faculty))).json()
    assert len(clos["clos"]) == len(OS_CLOS)


async def test_unknown_index_is_rejected(client, db_session, department, faculty):
    course = await _os_course(db_session, department, faculty)
    resp = await client.post(
        f"/api/v1/courses/{course.id}/curriculum-clos/import",
        json={"indices": [99]},
        headers=auth_header(faculty),
    )
    assert resp.status_code == 422


async def test_course_without_curriculum_clos(client, course, faculty):
    """The conftest course sits in a non-catalog test programme."""
    preview = await client.get(f"/api/v1/courses/{course.id}/curriculum-clos", headers=auth_header(faculty))
    assert preview.json()["clos"] == []
    imported = await client.post(
        f"/api/v1/courses/{course.id}/curriculum-clos/import", json={}, headers=auth_header(faculty)
    )
    assert imported.json() == {"created": [], "skipped": 0}


async def test_other_faculty_and_students_cannot_use_it(client, db_session, department, faculty, make_user, make_student):
    course = await _os_course(db_session, department, faculty)
    other = await make_user("clo.other@adaptobe.edu", role=UserRole.faculty, employee_id="FAC-CLO-OTHER")
    student = await make_student("cloimp")
    for actor in (other, student):
        get = await client.get(f"/api/v1/courses/{course.id}/curriculum-clos", headers=auth_header(actor))
        post = await client.post(
            f"/api/v1/courses/{course.id}/curriculum-clos/import", json={}, headers=auth_header(actor)
        )
        assert get.status_code == 403
        assert post.status_code == 403


async def test_picker_reports_clo_counts(client, db_session, department, faculty):
    bscs = await _bscs(db_session, department)
    catalog = (await client.get(f"/api/v1/curriculum/{bscs.id}", headers=auth_header(faculty))).json()
    by_code = {c["code"]: c for c in catalog["courses"]}
    assert by_code["CS-553"]["clo_count"] == len(OS_CLOS)
    assert by_code["CS-363"]["clo_count"] == 0  # Pakistan Studies: empty in the document
