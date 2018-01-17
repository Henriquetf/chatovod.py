from collections import namedtuple


Route = namedtuple('Route', 'method path')


class Method:
    GET = 'GET'
    POST = 'POST'
    HEAD = 'HEAD'


class AdminEndpoint:
    host = 'admin.chatovod.com'


class AccountEndpoint:
    """Endpoints for account management."""

    host = 'account.chatovod.com'

    LOGIN_PAGE = Route(Method.HEAD, '/u/login')
    LOGIN = Route(Method.POST, '/u/login.do')
    LOGOUT = Route(Method.POST, '/u/logout')


class APIEndpoint:
    """Endpoints for the Chatovod chat API."""
    host = 'chatovod.com'

    # Chat
    CHAT_BIND = Route(Method.GET, '/chat/bind')
    CHAT_INFO_FETCH = Route(Method.GET, '/chat/start')
    CHAT_SESSION_FETCH = Route(Method.HEAD, '/')
    CHAT_BANS_FETCH = Route(Method.GET, '/chat/load/banlist')
    CHAT_ROOMS_FETCH = Route(Method.GET, '/chat/load/rooms')

    # Chat - Nickname
    CHAT_NICKNAME_BAN      = Route(Method.POST, '/chat/ban')
    CHAT_NICKNAME_UNBAN    = Route(Method.POST, '/chat/unban')
    CHAT_NICKNAME_MODERATE = Route(Method.GET, '/chat/getChatNickLocalModInfo')
    CHAT_NICKNAME_FETCH    = Route(Method.POST, '/chat/getChatNickLocal')

    # Room
    ROOM_OPEN  = Route(Method.POST, '/chat/openRoom')
    ROOM_PRIVATE_OPEN = Route(Method.POST, '/chat/openPrivate2')
    ROOM_CLOSE = Route(Method.POST, '/chat/closeRoom')

    ROOM_MESSAGE_SEND    = Route(Method.POST, '/chat/send')
    ROOM_MESSAGES_READ   = Route(Method.POST, '/chat/markChannelRead')
    ROOM_MESSAGES_DELETE = Route(Method.POST, '/chat/deleteMessages')
    ROOM_MESSAGES_FETCH  = Route(Method.GET, '/chat/loadLastMessages')

    # User
    USER_CHAT_ENTER = Route(Method.POST, '/chat/auth')
    USER_CHAT_LEAVE = Route(Method.GET, '/chat/signOut')
    USER_AGE_SET    = Route(Method.POST, '/chat/setAge')
    USER_STATUS_SET = Route(Method.POST, '/chat/setStatus')
    USER_REGISTER   = Route(Method.GET, '/register')
