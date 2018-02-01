from chatovod.api.event_adapter import adapt_error


class ChatovodException(Exception):
    """Base exception for errors caused by the library."""


class HTTPException(ChatovodException):
    """ """

class ConnectionError(HTTPException):
    """ """

class ConnectionReset(ConnectionError):
    """ """

class Forbidden(HTTPException):
    """ """


def error_factory(raw):
    error = adapt_error(raw)
    error_type = error['type']

    if error_type == 'connection':
        if error['group'] == 'reset':
            return ConnectionReset
        else:
            return ConnectionError
    elif error_type == 'auth':
        return Forbidden
    else:
        return HTTPException
