"""
Contains classes and functions regarding Lectio Assignments.
"""
from urllib.parse import urlparse, parse_qs

from dateutil import parser as dt_parser

from .config import DEFAULT_TZ, DECIMAL_SEPARATOR
from .types import AssignmentWaitingFor, AssignmentStatuses, LectioType
from .utilities import percent2float
from .exceptions import ScrapingError


class Assignment(LectioType):
    """
    Represents an Assignment assigned to a Lectio student.
    """
    WAITING_FOR_LOOKUP = {
        "Elev": AssignmentWaitingFor.STUDENT,
        "Lærer": AssignmentWaitingFor.TEACHER
    }

    STATUS_LOOKUP = {
        "Afleveret": AssignmentStatuses.HANDED_IN,
        "Venter": AssignmentStatuses.WAITING
    }

    ATTRIBUTES = ["week", "group", "title", "deadline", "student_hours",
                  "status", "absence", "waiting_for", "note", "grade",
                  "student_note", "id"]

    def __init__(self, raw_tag, tz=DEFAULT_TZ):
        self.week = None
        self.group = None
        self.title = None
        self.deadline = None
        self.student_hours = None
        self.status = None
        self.absence = None
        self.waiting_for = None
        self.note = None
        self.grade = None
        self.student_note = None
        self.id = None

        self.tz = tz

        # Initial unused element
        raw_tag.contents.pop(0)

        # Week
        week_tag = raw_tag.contents.pop(0)
        self.week = int(week_tag.span.text)

        # Group
        group_tag = raw_tag.contents.pop(0)
        self.group = group_tag.span.text

        # Title
        title_tag = raw_tag.contents.pop(0)
        self.title = title_tag.span.text

        # Id - based on title_tag
        parsed_url = urlparse(title_tag.span.a["href"])
        parsed_qs = parse_qs(parsed_url.query)

        self.id = "e" + parsed_qs["exerciseid"][0]

        # Deadline
        deadline_tag = raw_tag.contents.pop(0)
        self.deadline = dt_parser.parse(deadline_tag.span.text, dayfirst=True,
                                        yearfirst=False)
        # pylint thinks deadline is a tuple.
        # pylint: disable=no-member
        self.deadline = self.deadline.replace(tzinfo=self.tz)
        # pylint: enable=no-member

        # Student Hours
        student_hours_tag = raw_tag.contents.pop(0)
        number_text = student_hours_tag.span.text.replace(DECIMAL_SEPARATOR,
                                                          ".")
        self.student_hours = float(number_text)

        # Status
        status_tag = raw_tag.contents.pop(0)
        status = status_tag.span.text
        try:
            self.status = self.STATUS_LOOKUP[status]
        except KeyError:
            raise ScrapingError("Unknown value in 'status' field: " + status)

        # Absence
        absence_tag = raw_tag.contents.pop(0)
        if absence_tag.text:
            self.absence = percent2float(absence_tag.text)

        # Waiting For
        waiting_for_tag = raw_tag.contents.pop(0)
        who = waiting_for_tag.span.text
        try:
            self.waiting_for = self.WAITING_FOR_LOOKUP[who]
        except KeyError:
            raise ScrapingError("Unknown value in 'waiting for' field: " + who)

        # Note
        note_tag = raw_tag.contents.pop(0)
        self.note = note_tag.text

        # Grade
        grade_tag = raw_tag.contents.pop(0)
        if grade_tag.text:
            self.grade = int(grade_tag.text)

        # Student Note
        student_note_tag = raw_tag.contents.pop(0)
        self.student_note = student_note_tag.text
