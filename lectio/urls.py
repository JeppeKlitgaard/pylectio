"""
This module is in charge of handling URLs in lectio.
"""
from .config import BASE_URL


def _make_url(school_id, endpoint):
    """
    Crafts an URL based on the ``school_id``, ``endpoint``, and ``query``.

    ``school_id`` is a number as a string object
    Example:
        ``school_id = "248"``

    ``endpoint`` is a string object containing with the endpoint
    Example:
        ``endpoint = "SkemaNy.aspx"``
    """
    url = BASE_URL + school_id + "/" + endpoint

    return url


def make_timetable_url(school_id):
    """
    Returns a Lectio timetable URL for a given student at a given school for
    the proper week.
    """
    return _make_url(school_id, "SkemaNy.aspx")


def make_login_url(school_id):
    """
    Returns a Lectio Login URL.
    """
    return _make_url(school_id, "login.aspx")


def make_frontpage_url(school_id):
    """
    Returns a Lectio Frontpage URL.
    """
    return _make_url(school_id, "forside.aspx")


def make_assignments_overview_url(school_id):
    """
    Returns a Lectio Assignment Overview URL.
    """
    return _make_url(school_id, "OpgaverElev.aspx")
