"""Read-only, role-scoped tools the chatbot may call (chatbot Phase 2).

This module is the security boundary of the assistant. The LLM never touches
the database, never writes SQL, and never decides whose data it sees:

* **Allowlist.** Only the functions registered in `TOOLS` exist. A model asking
  for anything else gets an error result, not an exception.
* **Read-only.** Every tool only reads, through the same services the REST API
  uses. Nothing here can create, update or delete.
* **Identity from the JWT.** Handlers receive the authenticated `user` from the
  router. No tool accepts a user/student id argument, so "show me student 42"
  cannot be expressed -- a student only ever gets their own data.
* **Role re-checked at execution.** `execute` refuses a tool the caller's role
  isn't allowed, even if a manipulated model emits the call anyway.
* **Scoped lookups.** A course code is resolved only among the caller's own
  courses (taught, for faculty; enrolled, for students). A code belonging to
  someone else reads exactly like a code that doesn't exist, so nothing leaks.
* **Minimal data.** Results carry codes, titles and percentages; student
  identity is limited to seat numbers, never emails.
"""

import logging
from collections import Counter
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course
from app.models.enrollment import CourseEnrollment
from app.models.user import User, UserRole
from app.services import (
    assessment_service,
    attainment_service,
    course_service,
    risk_service,
    student_service,
)
from app.services.chat_guard import clean_course_code, course_code_key
from app.services.exceptions import NotFoundError, PermissionDeniedError

logger = logging.getLogger(__name__)

Handler = Callable[[AsyncSession, User, dict], Awaitable[dict]]


class ToolError(Exception):
    """A user-facing tool failure, reported back to the model as data."""


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    roles: frozenset
    takes_course_code: bool
    handler: Handler

    def schema(self) -> dict:
        properties = {}
        required = []
        if self.takes_course_code:
            properties["course_code"] = {
                "type": "string",
                "description": "The course code exactly as the user wrote it, e.g. 'SE-301'.",
            }
            required.append("course_code")
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {"type": "object", "properties": properties, "required": required},
            },
        }


def _pct(value: float) -> float:
    return round(float(value), 1)


# ---- Course resolution (always scoped to the caller) -------------------------

async def _own_courses(db: AsyncSession, user: User) -> list[Course]:
    if user.role == UserRole.faculty:
        return await course_service.list_courses(db, owner_faculty_id=user.id)
    if user.role == UserRole.student:
        result = await db.execute(
            select(Course)
            .join(CourseEnrollment, CourseEnrollment.course_id == Course.id)
            .where(CourseEnrollment.student_id == user.id)
            .order_by(Course.id)
        )
        return list(result.scalars().all())
    return []


async def _resolve_course(db: AsyncSession, user: User, args: dict) -> Course:
    code = clean_course_code(args.get("course_code"))
    if code is None:
        raise ToolError("Please give a valid course code, e.g. 'SE-301'.")

    key = course_code_key(code)
    courses = await _own_courses(db, user)
    matches = [course for course in courses if course_code_key(course.code) == key]
    if not matches:
        available = ", ".join(sorted({course.code for course in courses})) or "none"
        raise ToolError(f"No course '{code}' among your courses. Your courses: {available}.")
    if len(matches) > 1:
        options = "; ".join(f"{c.code} {c.name} (semester {c.semester})" for c in matches)
        raise ToolError(f"Several of your courses use code '{code}': {options}.")
    return matches[0]


# ---- Student tools -----------------------------------------------------------

async def _get_my_progress(db: AsyncSession, user: User, args: dict) -> dict:
    progress = await student_service.get_progress(db, user)
    return {
        "overall_average": _pct(progress.overall_average),
        "courses": [
            {
                "course_code": course.code,
                "course_name": course.name,
                "threshold": _pct(course.threshold),
                "overall_average": _pct(course.overall_average),
                "clos": [
                    {
                        "code": clo.code,
                        "title": clo.title,
                        "attainment": _pct(clo.attainment_percentage),
                        "is_weak": clo.is_weak,
                    }
                    for clo in course.clo_progress
                ],
            }
            for course in progress.courses
        ],
    }


async def _get_my_scores(db: AsyncSession, user: User, args: dict) -> dict:
    course = await _resolve_course(db, user, args)
    history = await student_service.get_course_scores(db, user, course.id)
    return {
        "course_code": course.code,
        "assessments": [
            {
                "title": item.title,
                "type": item.type,
                "obtained": item.obtained,
                "total_marks": item.total_marks,
                "percentage": _pct(item.percentage),
            }
            for item in history.items
        ],
    }


# ---- Faculty tools -----------------------------------------------------------

async def _list_my_courses(db: AsyncSession, user: User, args: dict) -> dict:
    courses = await _own_courses(db, user)
    return {
        "courses": [
            {"course_code": c.code, "course_name": c.name, "semester": c.semester}
            for c in courses
        ]
    }


async def _get_course_attainment(db: AsyncSession, user: User, args: dict) -> dict:
    course = await _resolve_course(db, user, args)
    report = await attainment_service.build_course_report(db, course.id)
    return {
        "course_code": course.code,
        "threshold": _pct(report.threshold),
        "students_with_attainment": report.student_count,
        "clos": [
            {
                "code": clo.code,
                "title": clo.title,
                "class_average": _pct(clo.class_average),
                "achieved": clo.is_achieved,
            }
            for clo in report.clo_attainment
        ],
        "plos": [
            {"code": plo.code, "title": plo.title, "class_average": _pct(plo.class_average)}
            for plo in report.plo_attainment
        ],
    }


async def _list_course_assessments(db: AsyncSession, user: User, args: dict) -> dict:
    course = await _resolve_course(db, user, args)
    assessments = await assessment_service.list_assessments(db, course.id)
    used = sum(a.weightage_percent for a in assessments)
    return {
        "course_code": course.code,
        "total_weightage_used": _pct(used),
        "weightage_remaining": _pct(max(0.0, 100.0 - used)),
        "assessments": [
            {
                "title": a.title,
                "type": a.type.value,
                "total_marks": a.total_marks,
                "weightage_percent": a.weightage_percent,
            }
            for a in assessments
        ],
    }


async def _get_course_risk(db: AsyncSession, user: User, args: dict) -> dict:
    course = await _resolve_course(db, user, args)
    report = await risk_service.get_stored_predictions(db, course.id, user)

    seat_by_id = {}
    student_ids = [p.student_id for p in report.predictions]
    if student_ids:
        rows = await db.execute(select(User.id, User.seat_no).where(User.id.in_(student_ids)))
        seat_by_id = {row.id: row.seat_no for row in rows}

    at_risk = []
    for prediction in report.predictions:
        if prediction.risk_level.value == "low":
            continue
        drivers = [
            c.feature
            for c in prediction.shap_explanation.feature_contributions
            if c.impact == "increased_risk"
        ][:2]
        at_risk.append({
            "seat_no": seat_by_id.get(prediction.student_id) or "unknown",
            "risk_level": prediction.risk_level.value,
            "predicted_score": _pct(prediction.predicted_score),
            "main_risk_factors": drivers,
        })
    at_risk.sort(key=lambda s: (s["risk_level"] != "high", s["predicted_score"]))

    return {
        "course_code": course.code,
        "predictions_available": bool(report.predictions),
        "note": None if report.predictions else (
            "No prediction has been run yet. Use 'Run Prediction' on the Dashboard."
        ),
        "risk_counts": dict(Counter(p.risk_level.value for p in report.predictions)),
        "at_risk_students": at_risk,
        "learning_gaps": [
            {"clo": gap.code, "title": gap.title, "class_average": _pct(gap.class_average)}
            for gap in report.learning_gaps
        ],
    }


# ---- Registry ----------------------------------------------------------------

_STUDENT = frozenset({UserRole.student})
_FACULTY = frozenset({UserRole.faculty})

TOOLS: dict[str, Tool] = {
    tool.name: tool
    for tool in (
        Tool(
            "get_my_progress",
            "Get the signed-in student's own CLO attainment for every enrolled course, "
            "including which CLOs are weak.",
            _STUDENT, False, _get_my_progress,
        ),
        Tool(
            "get_my_scores",
            "Get the signed-in student's own marks on each assessment of one course.",
            _STUDENT, True, _get_my_scores,
        ),
        Tool(
            "list_my_courses",
            "List the courses the signed-in faculty member teaches.",
            _FACULTY, False, _list_my_courses,
        ),
        Tool(
            "get_course_attainment",
            "Get class-average CLO and PLO attainment for one of the faculty member's courses.",
            _FACULTY, True, _get_course_attainment,
        ),
        Tool(
            "list_course_assessments",
            "List the assessments of one of the faculty member's courses, with marks and "
            "weightage used/remaining.",
            _FACULTY, True, _list_course_assessments,
        ),
        Tool(
            "get_course_risk",
            "Get the latest stored risk predictions (by seat number) and learning gaps for "
            "one of the faculty member's courses.",
            _FACULTY, True, _get_course_risk,
        ),
    )
}


def tools_for_role(role: UserRole) -> list[Tool]:
    return [tool for tool in TOOLS.values() if role in tool.roles]


async def execute(db: AsyncSession, user: User, name: str, args) -> dict:
    """Run one tool call on behalf of `user`. Never raises; errors become data."""
    tool = TOOLS.get(name)
    if tool is None or user.role not in tool.roles:
        logger.warning("Chat tool refused: user=%s role=%s tool=%r", user.id, user.role, name)
        return {"error": "That information isn't available to you."}

    if not isinstance(args, dict):
        args = {}

    logger.info("Chat tool call: user=%s tool=%s", user.id, name)
    try:
        return await tool.handler(db, user, args)
    except ToolError as exc:
        return {"error": str(exc)}
    except (NotFoundError, PermissionDeniedError):
        return {"error": "That information isn't available to you."}
