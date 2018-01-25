from collections import namedtuple


Route = namedtuple('Route', 'method url')

class Path(namedtuple('Path', 'method path')):
    def __call__(self, url):
        return Route(self.method, url + self.path)


class Method:
    GET = 'GET'
    POST = 'POST'
    HEAD = 'HEAD'


class AccountEndpoint:
    """Endpoints for account management."""

    host = 'https://account.chatovod.com'

    LOGIN_PAGE = Route(Method.HEAD, host + '/u/login')
    LOGIN = Route(Method.POST, host + '/u/login.do')
    LOGOUT = Route(Method.POST, host + '/u/logout')


class APIEndpoint:
    """Endpoints for the Chatovod chat API."""
    host = 'chatovod.com'

    # Chat
    CHAT_BIND = Path(Method.GET, '/chat/bind')
    CHAT_INFO_FETCH = Path(Method.GET, '/chat/start')
    CHAT_SESSION_FETCH = Path(Method.HEAD, '/')
    CHAT_BANS_FETCH = Path(Method.GET, '/chat/load/banlist')
    CHAT_ROOMS_FETCH = Path(Method.GET, '/chat/load/rooms')

    # Chat - Nickname
    CHAT_NICKNAME_BAN      = Path(Method.POST, '/chat/ban')
    CHAT_NICKNAME_UNBAN    = Path(Method.POST, '/chat/unban')
    CHAT_NICKNAME_MODERATE = Path(Method.GET, '/chat/getChatNickLocalModInfo')
    CHAT_NICKNAME_FETCH    = Path(Method.POST, '/chat/getChatNickLocal')

    # Room
    ROOM_OPEN  = Path(Method.POST, '/chat/openRoom')
    ROOM_PRIVATE_OPEN = Path(Method.POST, '/chat/openPrivate2')
    ROOM_CLOSE = Path(Method.POST, '/chat/closeRoom')

    ROOM_MESSAGE_SEND    = Path(Method.POST, '/chat/send')
    ROOM_MESSAGES_READ   = Path(Method.POST, '/chat/markChannelRead')
    ROOM_MESSAGES_DELETE = Path(Method.POST, '/chat/deleteMessages')
    ROOM_MESSAGES_FETCH  = Path(Method.GET, '/chat/loadLastMessages')

    # User
    USER_CHAT_ENTER = Path(Method.POST, '/chat/auth')
    USER_CHAT_LEAVE = Path(Method.GET, '/chat/signOut')
    USER_AGE_SET    = Path(Method.POST, '/chat/setAge')
    USER_STATUS_SET = Path(Method.POST, '/chat/setStatus')
    USER_REGISTER   = Path(Method.GET, '/register')
