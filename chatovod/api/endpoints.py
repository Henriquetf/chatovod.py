from collections import namedtuple


Route = namedtuple('Route', 'method url')
Path = namedtuple('Path', 'method path')

def make_route(path, base):
    return Route(method=path.method, url=(base + path.path))


class AccountEndpoint:
    """Endpoints for account management."""

    BASE = 'https://account.chatovod.com'

    LOGIN_PAGE = Route('HEAD', BASE + '/u/login')
    LOGIN = Route('POST', BASE + '/u/login.do')
    LOGOUT = Route('POST', BASE + '/u/logout')

    ASSOCIATE_ACCOUNT = Path('GET', '/widget/login')


class APIEndpoint:
    """Endpoints for the Chatovod chat API."""
    host = 'chatovod.com'

    # Chat
    CHAT_BIND = Path('GET', '/chat/bind')
    CHAT_INFO_FETCH = Path('GET', '/chat/start')
    CHAT_SESSION_FETCH = Path('HEAD', '/')
    CHAT_BANS_FETCH = Path('GET', '/chat/load/banlist')
    CHAT_ROOMS_FETCH = Path('GET', '/chat/load/rooms')

    # Chat - Nickname
    CHAT_NICKNAME_BAN      = Path('POST', '/chat/ban')
    CHAT_NICKNAME_UNBAN    = Path('POST', '/chat/unban')
    CHAT_NICKNAME_MODERATE = Path('GET', '/chat/getChatNickLocalModInfo')
    CHAT_NICKNAME_FETCH    = Path('POST', '/chat/getChatNickLocal')

    # Room
    ROOM_OPEN  = Path('POST', '/chat/openRoom')
    ROOM_PRIVATE_OPEN = Path('POST', '/chat/openPrivate2')
    ROOM_CLOSE = Path('POST', '/chat/closeRoom')

    ROOM_MESSAGE_SEND    = Path('POST', '/chat/send')
    ROOM_MESSAGES_READ   = Path('POST', '/chat/markChannelRead')
    ROOM_MESSAGES_DELETE = Path('POST', '/chat/deleteMessages')
    ROOM_MESSAGES_FETCH  = Path('GET', '/chat/loadLastMessages')

    # User
    USER_CHAT_ENTER = Path('POST', '/chat/auth')
    USER_CHAT_LEAVE = Path('GET', '/chat/signOut')
    USER_AGE_SET    = Path('POST', '/chat/setAge')
    USER_STATUS_SET = Path('POST', '/chat/setStatus')
    USER_REGISTER   = Path('GET', '/register')
