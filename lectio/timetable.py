"""
Contains functions and classes related to the lectio timetable.
"""
from urllib.parse import urlparse, parse_qs
import html.parser
import re

import datetime
import pytz

from .config import DEFAULT_TZ
from .types import PeriodStatuses, LectioType


class Period(LectioType):
    """
    Represents a Period in a student's Lectio timetable.
    """
    CHANGED = "Ændret!"
    CANCELLED = "Aflyst!"
    ATTRIBUTES = ["status", "starttime", "endtime", "topic", "groups",
                  "teachers", "teachers_short", "rooms", "resources",
                  "links", "homework", "note", "id"]

    def __init__(self, raw_tag, tz=DEFAULT_TZ):
        self.status = None
        self.starttime = None
        self.endtime = None
        self.topic = None
        self.groups = None
        self.teachers = None
        self.teachers_short = None
        self.rooms = None
        self.resources = None
        self.links = None
        self.homework = None
        self.note = None
        self.id = None

        self.tz = tz

        self.data = raw_tag["title"]

        # Id
        parsed_url = urlparse(raw_tag["href"])
        parsed_qs = parse_qs(parsed_url.query)

        print("URL: " + str(parsed_url))
        print("QS: " + str(parsed_qs))

        if "absid" in parsed_qs:
            self.id = parsed_qs["absid"][0]
        elif "ProeveholdId" in parsed_qs:
            self.id = "p" + parsed_qs["ProeveholdId"][0]
        else:
            raise KeyError("Could not find an id in parsed query string.")

        # Remove empty elements, remove left and right whitespacing
        self.lines = [x.lstrip().rstrip() for x in self.data.split("\n") if x]

        # Decode xml chars
        parser = html.parser.HTMLParser()
        self.lines = [parser.unescape(x) for x in self.lines]

        # Status line, this isn't always present
        if self.lines[0] in (self.CHANGED, self.CANCELLED):
            status_line = self.lines.pop(0)

            if status_line == self.CHANGED:
                self.status = PeriodStatuses.CHANGED

            elif status_line == self.CANCELLED:
                self.status = PeriodStatuses.CANCELLED

        else:
            self.status = PeriodStatuses.NOTHING

        # Date line, always present
        p = r'^(?P<startday>\d+)\/(?P<startmonth>\d+)-(?P<startyear>\d{4}) (?P<starthour>\d{2}):(?P<startminute>\d{2})'
        p += r' til '
        p += r'(?P<endday>\d*)(?:\/*)(?P<endmonth>\d*)(?:-*)(?P<endyear>\d*)(?: *)(?P<endhour>\d{2}):(?P<endminute>\d{2})$'
        DATE_LINE_PATTERN = re.compile(p)
        date_line = self.lines.pop(0)
        result = re.match(DATE_LINE_PATTERN, date_line)

        startday = int(result.group("startday"))
        startmonth = int(result.group("startmonth"))
        startyear = int(result.group("startyear"))
        starthour = int(result.group("starthour"))
        startminute = int(result.group("startminute"))

        endday = result.group("endday")
        if not endday:
            endday = result.group("startday")
        endday = int(endday)

        endmonth = result.group("endmonth")
        if not endmonth:
            endmonth = result.group("startmonth")
        endmonth = int(endmonth)

        endyear = result.group("endyear")
        if not endyear:
            endyear = result.group("startyear")
        endyear = int(endyear)

        endhour = int(result.group("endhour"))
        endminute = int(result.group("endminute"))

        self.starttime = datetime.datetime(startyear, startmonth, startday,
                                           starthour, startminute)
        self.endtime = datetime.datetime(endyear, endmonth, endday, endhour,
                                         endminute)

        # convert to UTC
        self.starttime = self.tz.localize(self.starttime).astimezone(pytz.utc)
        self.endtime = self.tz.localize(self.endtime).astimezone(pytz.utc)

        # topic line, rarely present
        if not self.lines[0].startswith("Hold: "):
            topic_line = self.lines.pop(0)
            self.topic = topic_line

        # group line, always present
        group_line = self.lines.pop(0)
        self.groups = [x.lstrip().rstrip() for x in group_line[len("Hold: "):].split(",")]

        # We need to return if we have no more data to process
        if not self.lines:
            return

        # teachers line, almost always present
        if (self.lines[0].startswith("Lærer: ")
                or self.lines[0].startswith("Lærere: ")):

            teachers_line = self.lines.pop(0)
            # remove lead
            teachers_line = teachers_line.split(" ", 1)[-1]
            self.teachers = [x.lstrip().rstrip() for x in teachers_line.split(",")]

        # teachers short
        TEACHER_INITIAL_PATTERN = re.compile(r"\((\w+)\)")
        if self.teachers is not None:
            self.teachers_short = []

            for teacher in self.teachers:
                match = TEACHER_INITIAL_PATTERN.search(teacher)
                if match is not None:
                    self.teachers_short.append(match.group(1))
                else:
                    self.teachers_short.append(teacher)

        # We need to return if we have no more data to process
        if not self.lines:
            return

        # room line, always present if teacher present
        if (self.lines[0].startswith("Lokale: ")
                or self.lines[0].startswith("Lokaler: ")):

            room_line = self.lines.pop(0)
            # remove lead
            room_line = room_line.split(" ", 1)[-1]
            self.rooms = [x.lstrip().rstrip() for x in room_line.split(",")]

        # We need to return if we have no more data to process
        if not self.lines:
            return

        # Resource line
        if (self.lines[0].startswith("Resource: ")
                or self.lines[0].startswith("Ressourcer: ")):

            resource_line = self.lines.pop(0)
            # remove lead
            resource_line = resource_line.split(" ", 1)[-1]
            self.resources = [x.lstrip().rstrip() for x in resource_line.split(",")]

        # We need to return if we have no more data to process
        if not self.lines:
            return

        # Links line
        if (self.lines[0].startswith("Link: ")
                or self.lines[0].startswith("Links: ")):

            link_line = self.lines.pop(0)
            # remove lead
            link_line = link_line.split(" ", 1)[-1]

            LINK_PATTERN = re.compile(r'^(?P<link>\d+).*$')
            result = re.match(LINK_PATTERN, link_line)
            self.links = int(result.group("link"))

        # We need to return if we have no more data to process
        if not self.lines:
            return

        # Homework lines
        if self.lines[0].startswith("Lektier:"):
            self.lines.pop(0)  # Delete this line
            homework_lines = []
            while not self.lines[0].startswith("Note:"):
                homework_lines.append(self.lines.pop(0))
                if not self.lines:
                    break

            self.homework = "\n".join(homework_lines)

        # We need to return if we have no more data to process
        if not self.lines:
            return

        # Note lines
        if self.lines[0].startswith("Note:"):
            self.lines.pop(0)  # Delete this line
            note_lines = []
            while True:
                note_lines.append(self.lines.pop(0))
                if not self.lines:
                    break

            self.note = "\n".join(note_lines)

        return

    @staticmethod
    def is_period(tag):
        """
        Used by BeautifulSoup to determine whether a tag is a period.
        """
        return all((tag.name == "a",
                    "s2skemabrik" in tag.get("class", []),
                    "s2bgbox" in tag.get("class", [])))
