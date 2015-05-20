"""
Contains utility functions and classes used by pylectio.
"""

from re import _pattern_type


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


def lookup_values(values, lookup_table):
    """
    Looks up a list of ``values``, replacing each ``value`` with the
    respective ``value`` in ``lookup_table``.

    The keys of ``lookup_table`` can be ``re.RegexObject`` or ``str``.
    """
    new_values = []

    for value in values:
        found = False
        for k, v in lookup_table.items():
            if isinstance(k, _pattern_type):
                if k.match(value):
                    new_values.append(v)
                    found = True
                    break
            else:
                if value == k:
                    new_values.append(v)
                    found = True
                    break

        if not found:
            new_values.append(value)

    return new_values


def percent2float(percent):
    """
    Converts a string with a percentage to a float.
    """
    percent = percent.replace(" ", "")
    percent = percent.strip("%")

    return float(percent) / 100
