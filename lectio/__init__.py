#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for interacting with lectio.dk.

Currently supplies the Period class, which represents a period of a lectio
timetable.
"""

__version__ = (0, 0, 4)

# This is by no means beautiful code - scrapers rarely are.

import requests
from bs4 import BeautifulSoup as bs

from urllib.parse import urlparse, parse_qs
import html.parser
import re

from enum import Enum

import datetime
import pytz

LECTIO_URL = (u"https://www.lectio.dk/lectio/{SCHOOL_ID}/SkemaNy.aspx"
              u"?type=elev&elevid={STUDENT_ID}&week={WEEK_ID}")
DEFAULT_TZ = pytz.timezone("Europe/Copenhagen")


def _craft_week_id(week, year):
    """
    Returns a WeekID.
    """
    return str(week).zfill(2) + str(year)


def craft_url(school_id, student_id, week, year):
    """
    Returns a Lectio URL for a given student at a given school for the proper
    week.
    """
    week_id = _craft_week_id(week, year)

    return LECTIO_URL.format(SCHOOL_ID=school_id, STUDENT_ID=student_id,
                             WEEK_ID=week_id)


class PeriodStatuses(Enum):
    """
    Enumerates the statuses that a ``Period`` can have.
    """
    NOTHING = 0
    CANCELLED = 1
    CHANGED = 2


class Period(object):
    """
    Represents a Period in a student's Lectio timetable.
    """
    CHANGED = "Ændret!"
    CANCELLED = "Aflyst!"

    def __init__(self, raw_tag, tz=DEFAULT_TZ):
        self.status = None
        self.starttime = None
        self.endtime = None
        self.topic = None
        self.groups = None
        self.teachers = None
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

        self.id = parsed_qs["id"][0]

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
        """Used by BeautifulSoup to determine whether a tag is a period."""
        return all((tag.name == "a",
                    "s2skemabrik" in tag.get("class", []),
                    "s2bgbox" in tag.get("class", [])))

    def __repr__(self):
        indent = "\t"

        attributes = ["status", "starttime", "endtime", "topic", "groups",
                      "teachers", "rooms", "resources", "links", "homework",
                      "note", "id"]

        x = "<Period>"

        for attribute in attributes:
            attr_line = "{}: {}".format(attribute, getattr(self, attribute))
            x += "\n{}{}".format(indent, attr_line)

        return x


def deduplicate_list_of_periods(periods):
    known_ids = []
    result = []

    for period in periods:
        if period.id not in known_ids:
            known_ids.append(period.id)
            result.append(period)

    return result


def get_periods(school_id, student_id, week, year, tz=DEFAULT_TZ):
    """
    Returns a list of ``Period``s for a given week and year.

    ``tz`` must be set if the localtime of lectio is not Europe/Copenhagen.
    """
    week = str(week)
    year = str(year)

    url = craft_url(school_id, student_id, week, year)
    page = requests.get(url)
    soup = bs(page.text)

    raw_periods = soup.find_all(Period.is_period)

    periods = [Period(raw) for raw in raw_periods]

    periods = deduplicate_list_of_periods(periods)

    return periods
