"""
This module is in charge of handling URLs in lectio.
"""

from urllib.parse import urlencode

from .config import BASE_URL


def _make_url(school_id, endpoint, query={}):
    """
    Crafts an URL based on the ``school_id``, ``endpoint``, and ``query``.

    ``school_id`` is a number as a string object
    Example:
        ``school_id = "248"``

    ``endpoint`` is a string object containing with the endpoint
    Example:
        ``endpoint = "SkemaNy.aspx"``

    ``query`` is a dictionary containing the keys and values that make up the
    query-string.
    Example:
    ``query = {"type": "elev"}``
    """
    url = BASE_URL + school_id + "/" + endpoint

    if query:
        qs = urlencode(query)
        url += "?" + qs

    return url


def make_timetable_url(school_id, student_id, week, year):
    """
    Returns a Lectio timetable URL for a given student at a given school for
    the proper week.
    """
    week_id = str(week).zfill(2) + str(year)

    query = {
        "type": "elev",
        "elevid": student_id,
        "week": week_id
    }

    return _make_url(school_id, "SkemaNy.aspx", query)
