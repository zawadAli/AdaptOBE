"""Semester-wise curriculum (scheme of studies) for the UBIT programmes.

Transcribed from the department's curriculum documents (BSCS, BSSE, BSAI;
"Proposed curriculum ... as per the recommendations of NCEAC, HEC and Board of
Studies of University of Karachi"). Faculty pick from this catalog when creating
a course so code / name / credit hours / semester are consistent; manual entry
stays available for anything off-catalog (a "Topic of Current Interest", a
retake offering, ...).

This is reference data only -- it is never written to the database. A course
row is still created per faculty member when they actually teach it.

Conventions:
* Planned courses carry the single semester the scheme places them in.
* Domain-elective *slots* in the scheme ("CS-xxx Domain Elective-1") are not
  courses, so they are not listed. Instead every course in the elective pool is
  listed with the semesters its slots occur in. `ELECTIVE_SLOTS` records how many
  slots each semester has, so tests can check every semester's credit total
  against the documents.
* BSAI's Thesis I/II is an alternative to Final Year Project I/II, marked with
  `alternative_to`.
* BS Data Science has no curriculum document yet; per department direction it
  uses the BSCS catalog for now (`CURRICULUM_SOURCE`).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CatalogCourse:
    code: str
    name: str
    credit_hours: int
    breakdown: str  # theory+lab split as printed, e.g. "3+1"
    semesters: tuple[int, ...]
    category: str = "core"  # "core" | "elective"
    group: str | None = None  # elective pool, e.g. "Domain Elective 1-2"
    alternative_to: str | None = None


def _plan(semester: int, *rows: tuple[str, str, int, str]) -> tuple[CatalogCourse, ...]:
    return tuple(CatalogCourse(code, name, credits, split, (semester,)) for code, name, credits, split in rows)


def _electives(group: str, semesters: tuple[int, ...], *rows: tuple[str, str, int, str]) -> tuple[CatalogCourse, ...]:
    return tuple(
        CatalogCourse(code, name, credits, split, semesters, category="elective", group=group)
        for code, name, credits, split in rows
    )


BSCS = (
    *_plan(
        1,
        ("CS-351", "Programming Fundamentals", 4, "3+1"),
        ("CS-353", "Introduction to Information & Communication Technologies", 3, "3+0"),
        ("CS-355", "Calculus and Analytical Geometry", 3, "3+0"),
        ("CS-357", "Applied Physics", 3, "2+1"),
        ("CS-359", "Functional English", 3, "3+0"),
        ("CS-361", "Islamic Studies or Ethics", 2, "2+0"),
        ("CS-363", "Pakistan Studies", 2, "2+0"),
    ),
    *_plan(
        2,
        ("CS-352", "Object Oriented Concepts & Programming", 4, "3+1"),
        # The scheme prints "4 (2+1)"; the computing-core table gives DLD as 4 (3+1).
        ("CS-354", "Digital Logic Design", 4, "3+1"),
        ("CS-356", "Linear Algebra", 3, "3+0"),
        ("CS-358", "Discrete Structures", 3, "3+0"),
        ("CS-362", "Ideology and Constitution of Pakistan", 2, "2+0"),
        ("CS-364", "Fehm e Quran", 2, "2+0"),
    ),
    *_plan(
        3,
        ("CS-451", "Data Structures and Applications", 4, "3+1"),
        ("CS-453", "Software Engineering Fundamentals", 3, "3+0"),
        ("CS-455", "Computer Organization & Assembly Language", 3, "2+1"),
        ("CS-457", "Multivariable Calculus", 3, "3+0"),
        ("CS-459", "Probability & Statistics", 3, "3+0"),
        ("CS-461", "Urdu", 2, "2+0"),
    ),
    *_plan(
        4,
        ("CS-452", "Database Management Systems", 4, "3+1"),
        ("CS-454", "Expository Writing", 3, "3+0"),
        ("CS-456", "Theory of Automata", 3, "3+0"),
        ("CS-458", "Software Project Management", 3, "3+0"),
        ("CS-460", "Data Communication and Networking", 3, "2+1"),
        ("CS-462", "Professional Practices", 3, "3+0"),
    ),
    *_plan(
        5,
        ("CS-551", "Artificial Intelligence", 3, "2+1"),
        ("CS-553", "Operating Systems", 4, "3+1"),
        ("CS-555", "HCI and Computer Graphics", 3, "2+1"),
        ("CS-557", "Information Security", 3, "2+1"),
        ("CS-559", "Civics and Community Engagement", 2, "2+0"),
        ("CS-561", "Cloud Computing", 3, "2+1"),
    ),
    *_plan(
        6,
        ("CS-552", "Advance Database Management Systems", 3, "2+1"),
        ("CS-554", "Compiler Construction", 3, "2+1"),
        ("CS-556", "Design and Analysis of Algorithms", 3, "3+0"),
        ("CS-558", "Financial Accounting", 3, "3+0"),
    ),
    *_plan(
        7,
        ("CS-651", "Parallel & Distributed Computing", 3, "2+1"),
        ("CS-653", "Entrepreneurship", 3, "3+0"),
        ("CS-655", "Final Year Project - I", 3, "0+3"),
        ("CS-657", "Internship", 3, "3+0"),
    ),
    *_plan(
        8,
        ("CS-654", "Professional Certification", 3, "0+3"),
        ("CS-656", "Final Year Project - II", 3, "0+3"),
    ),
    *_electives(
        "Domain Elective 1-2", (6,),
        ("CS-572", "Advanced Programming", 3, "2+1"),
        ("CS-574", "Mobile Applications Development", 3, "2+1"),
        ("CS-575", "Web Technologies", 3, "2+1"),
        ("CS-576", "Multimedia Systems", 3, "2+1"),
        ("CS-577", "Simulation and Digital Twins", 3, "2+1"),
        ("CS-578", "Object Oriented Analysis and Design", 3, "3+0"),
    ),
    *_electives(
        "Domain Elective 3-5", (7, 8),
        ("CS-671", "Software Testing & Quality Assurance", 3, "3+0"),
        ("CS-672", "Advanced Computer Graphics", 3, "3+0"),
        ("CS-673", "Cyber Security", 3, "3+0"),
        ("CS-674", "Data Science", 3, "2+1"),
        ("CS-675", "Data Warehousing and Data Mining", 3, "2+1"),
        ("CS-677", "Web Engineering", 3, "2+1"),
        ("CS-678", "Natural Language Processing", 3, "3+0"),
        ("CS-679", "Neural Networks and Fuzzy Logic", 3, "3+0"),
    ),
)

BSSE = (
    *_plan(
        1,
        ("SE-351", "Programming Fundamentals", 4, "3+1"),
        ("SE-353", "Introduction to Information & Communication Technologies", 3, "2+1"),
        ("SE-355", "Calculus and Analytical Geometry", 3, "3+0"),
        ("SE-357", "Discrete Structures", 3, "3+0"),
        ("SE-359", "Functional English", 3, "3+0"),
        ("SE-361", "Ideology and Constitution of Pakistan", 2, "2+0"),
        ("SE-363", "Islamic Studies or Ethics", 2, "2+0"),
    ),
    *_plan(
        2,
        ("SE-352", "Object Oriented Concepts & Programming", 4, "3+1"),
        ("SE-354", "Software Engineering Fundamentals", 3, "3+0"),
        ("SE-356", "Multivariable Calculus", 3, "3+0"),
        ("SE-358", "Applied Physics", 3, "2+1"),
        ("SE-360", "Probability & Statistics", 3, "3+0"),
        ("SE-362", "Urdu", 2, "2+0"),
        ("SE-366", "Fehm e Quran", 2, "2+0"),
    ),
    *_plan(
        3,
        ("SE-451", "Data Structures and Applications", 4, "3+1"),
        ("SE-453", "Software Requirement Engineering", 3, "3+0"),
        ("SE-455", "Digital Logic Design", 4, "3+1"),
        ("SE-457", "Linear Algebra", 3, "3+0"),
        ("SE-459", "Expository Writing", 3, "3+0"),
        ("SE-450", "Pakistan Studies", 2, "2+0"),
    ),
    *_plan(
        4,
        ("SE-452", "Database Management Systems", 4, "3+1"),
        ("SE-454", "Software Design and Architecture", 3, "3+0"),
        ("SE-456", "Computer Organization & Assembly Language", 3, "2+1"),
        ("SE-458", "Operating Systems", 4, "3+1"),
        ("SE-460", "Artificial Intelligence", 3, "2+1"),
        ("SE-462", "Civics and Community Engagement", 2, "2+0"),
    ),
    *_plan(
        5,
        ("SE-551", "Software Construction and Development", 3, "2+1"),
        ("SE-553", "Software Project Management", 3, "3+0"),
        ("SE-555", "Data Communication and Networking", 3, "2+1"),
        ("SE-557", "Theory of Automata", 3, "2+1"),
        ("SE-559", "Professional Practices", 3, "3+0"),
    ),
    *_plan(
        6,
        ("SE-552", "Design and Analysis of Algorithms", 3, "3+0"),
        ("SE-554", "Software Quality Engineering, Testing and Assurance", 3, "3+0"),
        ("SE-556", "Information Security", 3, "2+1"),
        ("SE-558", "Cloud Computing", 3, "2+1"),
    ),
    *_plan(
        7,
        ("SE-651", "Financial Accounting", 3, "3+0"),
        ("SE-653", "Internship", 3, "3+0"),
        # Printed as "2SE-655" -- a stray footnote marker in the document.
        ("SE-655", "Final Year Project - I", 3, "0+3"),
    ),
    *_plan(
        8,
        ("SE-666", "Professional Certification", 3, "3+0"),
        ("SE-652", "Parallel & Distributed Computing", 3, "2+1"),
        ("SE-654", "Entrepreneurship", 3, "3+0"),
        ("SE-656", "Final Year Project - II", 3, "0+3"),
    ),
    *_electives(
        "Domain Elective 1-2", (5, 6),
        ("SE-571", "HCI and Computer Graphics", 3, "3+0"),
        ("SE-572", "Advanced Database Management Systems", 3, "2+1"),
        ("SE-573", "Object Oriented Analysis and Design", 3, "3+0"),
        ("SE-574", "Web Technologies", 3, "2+1"),
        ("SE-575", "Mobile Applications Development", 3, "2+1"),
        ("SE-576", "Computer Architecture", 3, "3+0"),
        ("SE-577", "Modelling and Simulation", 3, "2+1"),
    ),
    *_electives(
        "Domain Elective 3-4", (7,),
        ("SE-671", "Software Re-engineering", 3, "3+0"),
        ("SE-672", "Software Reverse Engineering and Ethical Hacking", 3, "3+0"),
        ("SE-673", "Remote Sensing and Geographic Information System", 3, "3+0"),
        ("SE-674", "Data Science", 3, "2+1"),
        ("SE-675", "Data Warehousing and Data Mining", 3, "2+1"),
        ("SE-677", "Web Engineering", 3, "2+1"),
        ("SE-678", "Natural Language Processing", 3, "3+0"),
        ("SE-679", "Neural Networks and Fuzzy Logic", 3, "3+0"),
    ),
)

BSAI = (
    *_plan(
        1,
        ("AI-351", "Programming Fundamentals", 4, "3+1"),
        ("AI-353", "Applications of Information & Communication Technologies", 3, "3+0"),
        ("AI-355", "Calculus and Analytical Geometry", 3, "3+0"),
        ("AI-357", "Applied Physics", 3, "2+1"),
        ("AI-359", "Functional English", 3, "3+0"),
        ("AI-361", "Islamic Studies or Ethics", 2, "2+0"),
    ),
    *_plan(
        2,
        ("AI-352", "Object Oriented Concepts & Programming", 4, "3+1"),
        ("AI-354", "Digital Logic Design", 3, "2+1"),
        ("AI-356", "Linear Algebra", 3, "3+0"),
        ("AI-358", "Discrete Structures", 3, "3+0"),
        ("AI-360", "Expository Writing", 3, "3+0"),
        ("AI-362", "Ideology and Constitution of Pakistan", 2, "2+0"),
        ("AI-364", "Pakistan Studies", 2, "2+0"),
    ),
    *_plan(
        3,
        ("AI-451", "Data Structures and Applications", 4, "3+1"),
        ("AI-453", "Software Engineering Fundamentals", 3, "3+0"),
        ("AI-455", "Computer Organization & Assembly Language", 3, "2+1"),
        ("AI-457", "Multivariable Calculus", 3, "3+0"),
        ("AI-459", "Probability & Statistics", 3, "3+0"),
        ("AI-461", "Urdu", 2, "2+0"),
    ),
    *_plan(
        4,
        ("AI-452", "Database Management Systems", 4, "3+1"),
        ("AI-454", "Artificial Intelligence", 3, "2+1"),
        ("AI-444", "Fehm e Quran", 2, "2+0"),
        ("AI-456", "Data Communication and Networking", 3, "2+1"),
    ),
    *_plan(
        5,
        ("AI-551", "Programming for AI", 3, "2+1"),
        ("AI-553", "Operating Systems", 3, "2+1"),
        ("AI-555", "Machine Learning", 3, "2+1"),
        ("AI-561", "Financial Accounting", 3, "3+0"),
        ("AI-557", "Information Security", 3, "2+1"),
        ("AI-559", "Civics and Community Engagement", 2, "2+0"),
    ),
    *_plan(
        6,
        ("AI-552", "Artificial Neural Networks & Deep Learning", 3, "2+1"),
        ("AI-554", "Professional Practices", 3, "2+1"),
        ("AI-556", "Design and Analysis of Algorithms", 3, "3+0"),
        ("AI-558", "Technical and Business Writing", 3, "3+0"),
    ),
    *_plan(
        7,
        ("AI-610", "Professional Certification", 3, "0+3"),
        ("AI-651", "Computer Vision", 3, "2+1"),
        ("AI-653", "Internship", 3, "0+3"),
        ("AI-655", "Final Year (Capstone) Project - I", 3, "0+3"),
    ),
    CatalogCourse("AI-657", "Thesis - I", 3, "3+0", (7,), alternative_to="AI-655"),
    *_plan(
        8,
        ("AI-652", "Parallel & Distributed Computing", 3, "2+1"),
        ("AI-660", "Entrepreneurship", 3, "3+0"),
        ("AI-654", "Knowledge Representation and Reasoning", 3, "3+0"),
        ("AI-656", "Final Year (Capstone) Project - II", 3, "0+3"),
    ),
    CatalogCourse("AI-658", "Thesis - II", 3, "3+0", (8,), alternative_to="AI-656"),
    *_electives(
        "Domain Elective 1", (4,),
        ("AI-471", "Theory of Automata", 3, "3+0"),
        ("AI-472", "Numerical Analysis and Computing", 3, "3+0"),
        ("AI-473", "Simulation and Modeling", 3, "3+0"),
    ),
    *_electives(
        "Domain Elective 2-3", (6,),
        ("AI-571", "Operations Research", 3, "3+0"),
        ("AI-572", "Agent Based Simulation and Modeling", 3, "3+0"),
        ("AI-573", "Fuzzy Systems", 3, "3+0"),
        ("AI-574", "Reinforcement Learning", 3, "3+0"),
        ("AI-575", "Social Network Analysis", 3, "3+0"),
        ("AI-576", "Mobile Applications Development", 3, "2+1"),
        ("AI-577", "HCI & Computer Graphics", 3, "2+1"),
        ("AI-578", "Internet of Things", 3, "2+1"),
    ),
    *_electives(
        "Domain Elective 4-5", (7, 8),
        ("AI-671", "Natural Language Processing", 3, "3+0"),
        ("AI-672", "Speech Processing", 3, "3+0"),
        ("AI-673", "Swarm Intelligence", 3, "3+0"),
        ("AI-674", "Data Warehousing and Data Mining", 3, "2+1"),
        ("AI-675", "Cyber Security", 3, "2+1"),
        ("AI-676", "Web Engineering", 3, "2+1"),
        ("AI-677", "Bioinformatics", 3, "3+0"),
        ("AI-678", "Complex Networks", 3, "3+0"),
        ("AI-680", "Topic of Current Interest", 3, "3+0"),
    ),
)

CURRICULA: dict[str, tuple[CatalogCourse, ...]] = {"BSCS": BSCS, "BSSE": BSSE, "BSAI": BSAI}

#: Programmes without their own document borrow another's catalog.
CURRICULUM_SOURCE: dict[str, str] = {"BSDS": "BSCS"}

#: Number of 3-credit domain-elective slots per semester, from each scheme.
ELECTIVE_SLOTS: dict[str, dict[int, int]] = {
    "BSCS": {6: 2, 7: 1, 8: 2},
    "BSSE": {5: 1, 6: 1, 7: 2},
    "BSAI": {4: 1, 6: 2, 7: 1, 8: 1},
}

#: "Total Credits for Semester" lines from each document.
SEMESTER_CREDIT_TOTALS: dict[str, dict[int, int]] = {
    "BSCS": {1: 20, 2: 18, 3: 18, 4: 19, 5: 18, 6: 18, 7: 15, 8: 12},
    "BSSE": {1: 20, 2: 20, 3: 19, 4: 19, 5: 18, 6: 15, 7: 15, 8: 12},
    "BSAI": {1: 18, 2: 20, 3: 18, 4: 15, 5: 17, 6: 18, 7: 15, 8: 15},
}


def catalog_source(program_code: str) -> str | None:
    """The programme whose catalog `program_code` uses, or None if it has none."""
    code = CURRICULUM_SOURCE.get(program_code, program_code)
    return code if code in CURRICULA else None


def catalog_for(program_code: str) -> tuple[CatalogCourse, ...]:
    source = catalog_source(program_code)
    return CURRICULA[source] if source else ()
