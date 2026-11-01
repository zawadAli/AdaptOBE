"""The chatbot's tool boundary: role gating, scoping and data minimisation.

Each test plays the part of a manipulated model that asks for something it
shouldn't get, and checks the server-side boundary refuses it regardless.
"""

import json

from app.models.user import UserRole
from app.schemas.course import CourseCreate
from app.services import chat_tools, course_service

REFUSED = {"error": "That information isn't available to you."}


async def _graded_student(course, make_clo, make_student, enroll, make_assessment, make_question,
                          enter_scores, suffix="tool", marks=4.0):
    clo = await make_clo("CLO-1", "Loops", "Write loops.")
    student = await make_student(suffix)
    await enroll(student)
    assessment = await make_assessment(total_marks=10.0)
    question = await make_question(assessment.id, 1, 10.0, clo.id)
    await enter_scores(assessment.id, [(question.id, student.id, marks)])
    return student


async def test_student_gets_own_progress(
    db_session, course, make_clo, make_student, enroll, make_assessment, make_question, enter_scores,
):
    student = await _graded_student(
        course, make_clo, make_student, enroll, make_assessment, make_question, enter_scores
    )
    result = await chat_tools.execute(db_session, student, "get_my_progress", {})
    assert result["courses"][0]["course_code"] == course.code
    clo = result["courses"][0]["clos"][0]
    assert clo["attainment"] == 40.0
    assert clo["is_weak"] is True


async def test_forged_student_id_argument_is_ignored(
    db_session, course, make_clo, make_student, enroll, make_assessment, make_question, enter_scores,
):
    """No tool takes a user id, so 'show me student X' can't be expressed."""
    victim = await _graded_student(
        course, make_clo, make_student, enroll, make_assessment, make_question, enter_scores,
        suffix="victim",
    )
    attacker = await make_student("attacker")  # enrolled nowhere

    result = await chat_tools.execute(
        db_session, attacker, "get_my_progress", {"student_id": victim.id, "user_id": victim.id}
    )
    assert result["courses"] == []  # attacker's own (empty) data, never the victim's


async def test_student_cannot_call_faculty_tools(db_session, course, make_student, enroll):
    student = await make_student("nosy")
    await enroll(student)
    for tool in ("get_course_risk", "get_course_attainment", "list_course_assessments", "list_my_courses"):
        result = await chat_tools.execute(db_session, student, tool, {"course_code": course.code})
        assert result == REFUSED


async def test_faculty_cannot_call_student_tools(db_session, faculty):
    result = await chat_tools.execute(db_session, faculty, "get_my_progress", {})
    assert result == REFUSED


async def test_admins_have_no_data_tools(db_session, sub_admin, super_admin):
    for admin in (sub_admin, super_admin):
        assert chat_tools.tools_for_role(admin.role) == []
        result = await chat_tools.execute(db_session, admin, "list_my_courses", {})
        assert result == REFUSED


async def test_unknown_tool_is_refused(db_session, faculty):
    for name in ("run_sql", "delete_course", "update_scores", "", "__import__"):
        assert await chat_tools.execute(db_session, faculty, name, {}) == REFUSED


async def test_no_registered_tool_can_write():
    """Guard against someone later registering a mutating tool by name."""
    forbidden = ("create", "update", "delete", "set", "enroll", "save", "write", "grade")
    for name in chat_tools.TOOLS:
        assert not any(word in name for word in forbidden), name


async def test_faculty_cannot_read_another_instructors_course(db_session, make_user, program, faculty):
    other = await make_user("other.fac@adaptobe.edu", role=UserRole.faculty, employee_id="FAC-OTHER")
    foreign = await course_service.create_course(
        db_session,
        CourseCreate(program_id=program.id, code="CS-999", name="Not Yours", credit_hours=3, semester=2),
        other,
    )
    result = await chat_tools.execute(
        db_session, faculty, "get_course_attainment", {"course_code": foreign.code}
    )
    assert "error" in result
    # Reads exactly like a code that doesn't exist -- and doesn't list it.
    assert "CS-999" not in result["error"].split("Your courses:")[-1]


async def test_student_cannot_read_scores_of_unenrolled_course(db_session, course, make_student):
    student = await make_student("outsider")
    result = await chat_tools.execute(
        db_session, student, "get_my_scores", {"course_code": course.code}
    )
    assert "error" in result
    assert "No course" in result["error"]


async def test_injected_course_code_is_rejected(db_session, faculty, course):
    for payload in ("CS-101'; DROP TABLE users;--", "CS-101 OR 1=1", None, 7):
        result = await chat_tools.execute(
            db_session, faculty, "get_course_attainment", {"course_code": payload}
        )
        assert result == {"error": "Please give a valid course code, e.g. 'SE-301'."}


async def test_course_code_matching_is_forgiving(db_session, faculty, course):
    result = await chat_tools.execute(
        db_session, faculty, "list_course_assessments", {"course_code": "cs 101"}
    )
    assert result["course_code"] == course.code
    assert result["weightage_remaining"] == 100.0


async def test_faculty_risk_tool_exposes_seat_numbers_not_emails(
    db_session, client, course, faculty, make_clo, make_student, enroll, make_assessment,
    make_question, enter_scores,
):
    from tests.conftest import auth_header

    clo = await make_clo("CLO-1", "Loops", "Write loops.")
    weak = await make_student("risky")
    await enroll(weak)
    for i in range(5):
        a = await make_assessment(title=f"Quiz {i}", total_marks=10.0, weightage_percent=1.0)
        q = await make_question(a.id, 1, 10.0, clo.id)
        await enter_scores(a.id, [(q.id, weak.id, 1.0)])
    await client.post(f"/api/v1/ml/predict-risk/{course.id}", headers=auth_header(faculty))

    result = await chat_tools.execute(db_session, faculty, "get_course_risk", {"course_code": course.code})
    assert result["predictions_available"] is True
    assert result["at_risk_students"][0]["seat_no"] == weak.seat_no
    dumped = json.dumps(result)
    assert weak.email not in dumped and "@" not in dumped


async def test_risk_tool_before_any_prediction(db_session, faculty, course):
    result = await chat_tools.execute(db_session, faculty, "get_course_risk", {"course_code": course.code})
    assert result["predictions_available"] is False
    assert "Run Prediction" in result["note"]


async def test_non_dict_arguments_do_not_crash(db_session, faculty):
    result = await chat_tools.execute(db_session, faculty, "list_my_courses", ["not", "a", "dict"])
    assert "courses" in result
