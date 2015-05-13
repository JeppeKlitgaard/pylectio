"""
Contains utility functions and classes used by pylectio.
"""

from .config import LECTIO_URL


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


def deduplicate_list_of_periods(periods):
    """
    Deduplicates a list of ``Period`` objects, ensuring no two ``Period``s have
    the same id``
    """
    known_ids = []
    result = []

    for period in periods:
        if period.id not in known_ids:
            known_ids.append(period.id)
            result.append(period)

    return result
