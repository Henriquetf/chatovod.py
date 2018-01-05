import aiohttp
import asyncio

from endpoints import APIEndpoint as Endpoint


class HTTPClient:

    def __init__(self, *, loop=None):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.session_id = None
        self.csrf_token = None

        # TODO: define the user-agent
        self.user_agent = ''

    @asyncio.coroutine
    def request(self, route):

        headers = {
            'User-Agent': self.user_agent
        }

    @asyncio.coroutine
    def chat_bind(self):
        route = Endpoint.CHAT_BIND

        return self.request(route)

    @asyncio.coroutine
    def chat_info_fetch(self):
        route = Endpoint.CHAT_INFO_FETCH

        return self.request(route)

    @asyncio.coroutine
    def chat_session_fetch(self):
        route = Endpoint.CHAT_SESSION_FETCH

        return self.request(route)

    @asyncio.coroutine
    def chat_bans_fetch(self):
        route = Endpoint.CHAT_BANS_FETCH

        return self.request(route)

    @asyncio.coroutine
    def chat_rooms_fetch(self):
        route = Endpoint.CHAT_ROOMS_FETCH

        return self.request(route)

    @asyncio.coroutine
    def chat_nickname_ban(self):
        route = Endpoint.CHAT_NICKNAME_BAN

        return self.request(route)

    @asyncio.coroutine
    def chat_nickname_unban(self):
        route = Endpoint.CHAT_NICKNAME_UNBAN

        return self.request(route)

    @asyncio.coroutine
    def chat_nickname_moderate(self):
        route = Endpoint.CHAT_NICKNAME_MODERATE

        return self.request(route)

    @asyncio.coroutine
    def chat_nickname_fetch(self):
        route = Endpoint.CHAT_NICKNAME_FETCH

        return self.request(route)

    @asyncio.coroutine
    def room_open(self):
        route = Endpoint.ROOM_OPEN

        return self.request(route)

    @asyncio.coroutine
    def room_private_open(self):
        route = Endpoint.ROOM_PRIVATE_OPEN

        return self.request(route)

    @asyncio.coroutine
    def room_close(self):
        route = Endpoint.ROOM_CLOSE

        return self.request(route)

    @asyncio.coroutine
    def room_message_send(self):
        route = Endpoint.ROOM_MESSAGE_SEND

        return self.request(route)

    @asyncio.coroutine
    def room_messages_read(self):
        route = Endpoint.ROOM_MESSAGES_READ

        return self.request(route)

    @asyncio.coroutine
    def room_messages_delete(self):
        route = Endpoint.ROOM_MESSAGES_DELETE

        return self.request(route)

    @asyncio.coroutine
    def room_messages_fetch(self):
        route = Endpoint.ROOM_MESSAGES_FETCH

        return self.request(route)

    @asyncio.coroutine
    def user_chat_enter(self):
        route = Endpoint.USER_CHAT_ENTER

        return self.request(route)

    @asyncio.coroutine
    def user_chat_leave(self):
        route = Endpoint.USER_CHAT_LEAVE

        return self.request(route)

    @asyncio.coroutine
    def user_age_set(self):
        route = Endpoint.USER_AGE_SET

        return self.request(route)

    @asyncio.coroutine
    def user_status_set(self):
        route = Endpoint.USER_STATUS_SET

        return self.request(route)

    @asyncio.coroutine
    def user_register(self):
        route = Endpoint.USER_REGISTER

        return self.request(route)
