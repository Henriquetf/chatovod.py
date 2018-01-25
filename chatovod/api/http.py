import aiohttp
import asyncio

from .endpoints import APIEndpoint as Endpoint


class HTTPClient:

    def __init__(self, domain, secure=True, client=None, loop=None):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.session_id = None
        self.csrf_token = None
        self._window_id = 0

        self.domain = domain
        self.secure = secure
        self.url = self.make_url(self.domain, self.secure)

        # TODO: define the user-agent
        self.user_agent = ''

    @asyncio.coroutine
    def request(self, route):

        headers = {
            'User-Agent': self.user_agent
        }

    @classmethod
    def make_url(cls, domain, secure):
        return ('https' if secure else 'http') + '://' + domain

    @asyncio.coroutine
    def chat_bind(self):
        return self.request(Endpoint.CHAT_BIND(self.url))

    @asyncio.coroutine
    def chat_info_fetch(self):
        return self.request(Endpoint.CHAT_INFO_FETCH(self.url))

    @asyncio.coroutine
    def chat_session_fetch(self):
        return self.request(Endpoint.CHAT_SESSION_FETCH(self.url))

    @asyncio.coroutine
    def chat_bans_fetch(self):
        route = Endpoint.CHAT_BANS_FETCH(self.url)

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
    def room_open(self, room_id):
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
    def room_message_send(self, content, room_id):
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
    def user_chat_enter(self, nickname, limit=80, captcha=None):
        route = Endpoint.USER_CHAT_ENTER
        if captcha is None:
            captcha = {}

        data = {
            'nick': nickname,
            'limit': limit,
            'wid': self.window_id,
            'csrf': self.csrf_token,
            'captchaSid': captcha['sid'],
            'captchaValue': captcha['value']
        }

        return self.request(route, data=data)

    @asyncio.coroutine
    def user_chat_leave(self):
        route = Endpoint.USER_CHAT_LEAVE

        params = {
            'wid': self.window_id,
            'csrf': self.csrf_token,
        }

        return self.request(route, params=params)

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
