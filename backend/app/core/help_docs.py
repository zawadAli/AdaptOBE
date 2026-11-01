"""Help-centre articles for the AdaptOBE assistant (chatbot Phase 1).

Static, reviewed text -- the only "knowledge" the help mode answers from. Each
article lists the roles allowed to see it, so a student is never shown faculty
or admin procedures (and vice versa). Keep wording in sync with the UI labels.
"""

from dataclasses import dataclass

ALL = frozenset({"super_admin", "sub_admin", "faculty", "student"})
FACULTY = frozenset({"faculty"})
SUB_ADMIN = frozenset({"sub_admin"})
SUPER_ADMIN = frozenset({"super_admin"})
STUDENT = frozenset({"student"})


@dataclass(frozen=True)
class HelpArticle:
    id: str
    title: str
    roles: frozenset
    body: str


HELP_ARTICLES: tuple[HelpArticle, ...] = (
    # ---- Everyone -----------------------------------------------------------
    HelpArticle(
        "obe-basics", "What OBE, CLOs and PLOs mean", ALL,
        "AdaptOBE follows Outcome-Based Education. A Course Learning Outcome (CLO) "
        "is what a student should be able to do after one course, e.g. 'Apply "
        "process synchronization techniques'. A Programme Learning Outcome (PLO) is "
        "a broader outcome for the whole degree; UBIT uses 10 standard PLOs (PLO-1 "
        "Academic Education to PLO-10 Lifelong Learning). Each CLO is mapped to one "
        "or more PLOs with a strength of 1 (weak), 2 (moderate) or 3 (strong).",
    ),
    HelpArticle(
        "attainment-formula", "How CLO and PLO attainment are calculated", ALL,
        "CLO attainment for a student = marks obtained on questions tagged to that "
        "CLO divided by the total marks of those questions, times 100. A student "
        "with no score on a question counts as 0 for it. PLO attainment is the "
        "strength-weighted average of the CLO attainments mapped to that PLO. A CLO "
        "is 'achieved' when the class average reaches the course threshold, 50% by "
        "default. Attainment recalculates automatically whenever scores, questions "
        "or CLO tags change.",
    ),
    HelpArticle(
        "bloom-levels", "Bloom's taxonomy levels", ALL,
        "Every CLO is tagged with one of the six cognitive Bloom levels: Remember, "
        "Understand, Apply, Analyze, Evaluate, Create. Lower levels test recall, "
        "higher levels test judgement and creation.",
    ),
    HelpArticle(
        "login-password", "Signing in and passwords", ALL,
        "Sign in at the login page with your university email and password. "
        "Accounts are created by an administrator; there is no self sign-up. If you "
        "forgot your password, ask your department's Sub-Admin -- they can view or "
        "reset it from your account's Edit page. Sessions expire after a period of "
        "inactivity and you will be asked to sign in again.",
    ),
    # ---- Super Admin --------------------------------------------------------
    HelpArticle(
        "superadmin-departments", "Managing departments", SUPER_ADMIN,
        "As Super Admin, open Admin Panel > Departments and click '+ Add Department'. "
        "Departments can be edited or deleted from the same list. Super Admins manage "
        "only departments and Sub-Admins, not programmes, courses or students.",
    ),
    HelpArticle(
        "superadmin-subadmins", "Creating and managing Sub-Admins", SUPER_ADMIN,
        "Open Admin Panel > Sub-Admins and click '+ Add Sub-Admin'. A Sub-Admin needs "
        "a department and an Employee ID. Use Deactivate to block an account and "
        "Reactivate to restore it. The search box filters by Employee ID.",
    ),
    # ---- Sub-Admin ----------------------------------------------------------
    HelpArticle(
        "subadmin-programmes-plos", "Programmes and PLOs", SUB_ADMIN,
        "Open Admin Panel > Programmes to add or edit degree programmes ('+ Add "
        "Programme'), and Admin Panel > PLOs to add or edit PLOs ('+ Add PLO'). Each "
        "PLO has a Bloom domain: Cognitive, Psychomotor or Affective. You can only "
        "manage your own department's data.",
    ),
    HelpArticle(
        "subadmin-students", "Adding students (one at a time or from a file)", SUB_ADMIN,
        "Open Admin Panel > Students. '+ Add Student' creates one account: enter "
        "full name, father's name, email, enrollment number and seat number; a "
        "password is generated automatically and shown once (you can view it later "
        "from Edit). 'Add Students via File' accepts an Excel or PDF roster: you get "
        "a preview of complete and incomplete rows before anything is saved, and "
        "incomplete rows are skipped. The search box filters by Seat No or "
        "Enrollment No.",
    ),
    HelpArticle(
        "subadmin-faculty", "Adding faculty accounts", SUB_ADMIN,
        "Open Admin Panel > Faculty and click '+ Add Faculty'. A Faculty ID is "
        "required. Use Deactivate / Reactivate to block or restore an account, and "
        "Edit to view a generated password.",
    ),
    # ---- Faculty ------------------------------------------------------------
    HelpArticle(
        "faculty-course", "Creating a course", FACULTY,
        "Go to Courses and click '+ New Course'. Choose the programme, code, name, "
        "credit hours and semester. The same code may repeat in a different "
        "programme or semester, but not the exact same combination. Open a course "
        "to reach its tabs: CLOs & Mappings, Enrollments, Assessments and Attendance.",
    ),
    HelpArticle(
        "faculty-clos", "Adding CLOs (manually or with AI)", FACULTY,
        "In a course, open the 'CLOs & Mappings' tab. '+ Add CLO' lets you type the "
        "code, title, description and Bloom level. 'Create CLO with AI' drafts the "
        "wording for you from a topic and the PLOs it should support; review it "
        "before saving. CLOs can be edited, deleted and reordered by dragging the "
        "grip handle.",
    ),
    HelpArticle(
        "faculty-mapping", "Mapping CLOs to PLOs", FACULTY,
        "On the 'CLOs & Mappings' tab, click 'Map to PLOs' on a CLO. The system "
        "suggests the most similar PLOs using AI text similarity and labels each "
        "Strong, Moderate or Weak (the ⓘ icon shows the exact score). Pick a "
        "strength from 1 to 3 and confirm. Nothing is mapped without your "
        "confirmation.",
    ),
    HelpArticle(
        "faculty-enroll", "Enrolling students", FACULTY,
        "Open the Enrollments tab. '+ Enroll Students' lists students of this "
        "course's programme and current batch. 'Add Students via File' matches an "
        "uploaded roster to existing accounts and enrolls the eligible ones (it "
        "never creates accounts). '+ Add Backlog Student' searches the whole "
        "department for a student from an earlier batch who is repeating the course.",
    ),
    HelpArticle(
        "faculty-assessments", "Creating assessments and questions", FACULTY,
        "Open the Assessments tab and click '+ Add Assessment'. Types are Quiz, "
        "Assignment, Lab, Project, Midterm and Final; total weightage across a course "
        "cannot exceed 100%. Open an assessment and use '+ Add Question' to add a "
        "Question, MCQ, Fill in the Blanks or True/False item, each tagged to a CLO "
        "('Suggest with AI' recommends a CLO). Question marks cannot exceed the "
        "assessment total and question numbers must be unique. Lab and Project "
        "assessments use their own component screen instead.",
    ),
    HelpArticle(
        "faculty-paper-import", "Uploading an assessment paper", FACULTY,
        "On an assessment's page, 'Upload Assessment Paper' accepts the real paper as "
        "PDF or Word. AI extracts the questions and header details; you verify the "
        "course/assessment/instructor match, review or edit each question, then add "
        "the ones you approve. Imported questions show an 'Extracted' badge.",
    ),
    HelpArticle(
        "faculty-scores", "Entering and importing scores", FACULTY,
        "On an assessment's page, enter marks in the score grid and click 'Save "
        "Scores', or use 'Upload Scores' to import an Excel/PDF score sheet with a "
        "preview before saving. Marks cannot exceed a question's marks. Saving "
        "scores recalculates attainment and updates the dashboard live.",
    ),
    HelpArticle(
        "faculty-attendance", "Recording attendance", FACULTY,
        "Open the course's Attendance tab. Type each student's attendance % and click "
        "'Save Attendance', or click 'Upload Attendance' to import a sheet with a "
        "preview first. Attendance is one of the inputs to risk prediction. You can "
        "search by name or seat number and filter students below or above a %.",
    ),
    HelpArticle(
        "faculty-dashboard", "Using the faculty dashboard and reports", FACULTY,
        "Dashboard shows, per course, enrolled students, the threshold, CLOs achieved "
        "and a CLO x PLO heatmap that refreshes live when scores change. "
        "'Recalculate' rebuilds attainment; 'Export Excel' and 'Export PDF' download "
        "the attainment report. On an assessment's page, 'Export' downloads the "
        "paper as PDF or Word.",
    ),
    HelpArticle(
        "faculty-risk", "Student risk prediction", FACULTY,
        "On the Dashboard, the Student Risk Prediction card's 'Run Prediction' "
        "classifies each student as low, medium or high risk using an XGBoost model "
        "over five features: attendance, quiz average, assignment average, midterm "
        "score and current CLO attainment. A student needs at least 5 scored "
        "assessments to be predicted. The ⓘ in the 'Why' column explains which "
        "features drove the prediction (SHAP). 'Learning gaps' lists CLOs whose class "
        "average is below the threshold.",
    ),
    # ---- Student ------------------------------------------------------------
    HelpArticle(
        "student-progress", "Reading your progress page", STUDENT,
        "My Progress shows your overall attainment, the number of courses you are "
        "enrolled in and how many of your CLOs are weak. A CLO is marked Weak when "
        "your own attainment on it is below the course threshold (usually 50%). "
        "Each course card shows a bar per CLO.",
    ),
    HelpArticle(
        "student-scores", "Seeing your score history", STUDENT,
        "On a course card in My Progress, click 'Score History' to see each "
        "assessment with your marks and percentage.",
    ),
    HelpArticle(
        "student-quiz", "Practice quizzes", STUDENT,
        "Click 'Practice Quiz' on a course card. You get MCQ, True/False and "
        "Fill-in-the-blank questions chosen mostly from the CLOs you are weakest in. "
        "Submit to see your score and which CLOs to keep practising. Practice "
        "quizzes are never added to your official marks; click 'Try Another' for a "
        "new set.",
    ),
    HelpArticle(
        "student-improve", "How to improve a weak CLO", STUDENT,
        "Read the CLO's title on your progress page to see what it covers, practise "
        "it with the Practice Quiz (which focuses on weak CLOs), review the related "
        "assessments in Score History, and ask your instructor about the topics you "
        "missed. Your attainment updates when new scores are entered.",
    ),
)


def articles_for_role(role: str) -> list[HelpArticle]:
    return [article for article in HELP_ARTICLES if role in article.roles]
