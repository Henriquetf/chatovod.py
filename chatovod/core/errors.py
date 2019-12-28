from chatovod.api.event_adapter import ErrorAdapter


class ChatovodException(Exception):
    """Base exception for errors caused by the library."""


class HTTPException(ChatovodException):
    """ """


class ChatovodConnectionError(HTTPException):
    """ """


class ConnectionReset(ChatovodConnectionError):
    """ """


class Forbidden(HTTPException):
    """ """


class UnavailableName(Forbidden):
    """ """


class InvalidLogin(HTTPException):
    """The provided login or password is incorrect."""


def error_factory(raw):
    error = ErrorAdapter.adapt(raw)
    error_type = error["type"]

    if error_type == "connection":
        if error["group"] == "reset":
            return ConnectionReset
        else:
            return ChatovodConnectionError
    elif error_type == "auth":
        if error["group"] == "alreadySignedIn":
            return UnavailableName
        else:
            return Forbidden
    else:
        return HTTPException
