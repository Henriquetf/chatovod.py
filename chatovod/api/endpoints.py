from typing import NamedTuple


class Route(NamedTuple):
    method: str
    path: str


class AccountEndpoint:
    """Endpoints for account management."""

    BASE = "https://account.chatovod.com"

    LOGIN_PAGE = Route("HEAD", "/u/login")
    LOGIN = Route("POST", "/u/login.do")
    LOGOUT = Route("GET", "/u/logout")

    ASSOCIATE_ACCOUNT = Route("GET", "/widget/login")


class APIEndpoint:
    """Endpoints for the Chatovod chat API."""

    HOST = "chatovod.com"

    # Chat
    CHAT_BIND = Route("GET", "/chat/bind")
    CHAT_INFO_FETCH = Route("GET", "/chat/start")
    CHAT_SESSION_FETCH = Route("HEAD", "/")
    CHAT_BANS_FETCH = Route("GET", "/chat/load/banlist")
    CHAT_ROOMS_FETCH = Route("GET", "/chat/load/rooms")

    # Chat - Nickname
    CHAT_NICKNAME_BAN = Route("POST", "/chat/ban")
    CHAT_NICKNAME_UNBAN = Route("POST", "/chat/unban")
    CHAT_NICKNAME_MODERATE = Route("GET", "/chat/getChatNickLocalModInfo")
    CHAT_NICKNAME_FETCH = Route("POST", "/chat/getChatNickLocal")

    # Room
    ROOM_OPEN = Route("POST", "/chat/openRoom")
    ROOM_PRIVATE_OPEN = Route("POST", "/chat/openPrivate2")
    ROOM_CLOSE = Route("POST", "/chat/closeRoom")

    ROOM_MESSAGE_SEND = Route("POST", "/chat/send")
    ROOM_MESSAGES_READ = Route("POST", "/chat/markChannelRead")
    ROOM_MESSAGES_DELETE = Route("POST", "/chat/deleteMessages")
    ROOM_MESSAGES_FETCH = Route("GET", "/chat/loadLastMessages")

    # User
    USER_CHAT_ENTER = Route("POST", "/chat/auth")
    USER_CHAT_LEAVE = Route("GET", "/chat/signOut")
    USER_AGE_SET = Route("POST", "/chat/setAge")
    USER_STATUS_SET = Route("POST", "/chat/setStatus")
    USER_REGISTER = Route("GET", "/register")
