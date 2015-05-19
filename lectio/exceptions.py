"""
Contains exceptions used by pylectio.
"""


class LectioError(Exception):
    """
    A general exception used as a base for other, more specific, exceptions.
    """


class NotLoggedInError(LectioError):
    """
    An exception raised when the user tries to do an action that requires
    authentication when not authenticated.
    """


class SessionClosedError(LectioError):
    """
    An exception raised when the user tries to interact with a closed
    ``Session``.
    """


class AuthenticationError(LectioError):
    """
    An exception raised when the authentication failed.
    """
