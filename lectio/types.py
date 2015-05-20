from enum import Enum


class LectioType(object):
    """
    Abstract Base Class for Lectio Types.
    """
    ATTRIBUTES = []

    def __repr__(self):
        indent = "\t"

        x = "<{}>".format(self.__class__.__name__)

        for attribute in self.ATTRIBUTES:
            attr_line = "{}: {}".format(attribute, getattr(self, attribute))
            x += "\n{}{}".format(indent, attr_line)

        return x


class PeriodStatuses(Enum):
    """
    Enumerates the statuses that a ``Period`` can have.
    """
    NOTHING = 0
    CANCELLED = 1
    CHANGED = 2


class AssignmentWaitingFor(Enum):
    STUDENT = 0
    TEACHER = 1


class AssignmentStatuses(Enum):
    HANDED_IN = 0
    WAITING = 1
