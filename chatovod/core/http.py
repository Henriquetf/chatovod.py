import aiohttp
import asyncio
import json

from chatovod.api.endpoints import APIEndpoint as Endpoints
from chatovod.api.endpoints import MakeRoute


class HTTPClient:

    def __init__(self, host, secure=True, client=None, loop=None):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self._session = aiohttp.ClientSession(loop=self.loop)

        self.session_id = None
        self.csrf_token = None
        self.window_id = 0

        self.host = host
        self.secure = secure
        self.url = self.make_url(host=self.host, secure=self.secure)

        # TODO: define the user-agent
        self.user_agent = ''

    @asyncio.coroutine
    def request(self, route, headers=None, csrf_token=None, session_id=None, **kwargs):
        method = route.method
        url = route.url

        kwargs['headers'] = {
            'User-Agent': self.user_agent
        }
        if headers:
            kwargs['headers'].update(headers)

        response = yield from self._session.request(method, url, **kwargs)

        if 200 <= response.status < 300:
            text = yield from response.text(encoding='utf-8')
            return text

    def session_id_type(self):
        return 'ssid' if self.secure else 'sid'

    @classmethod
    def make_url(cls, host, secure):
        return ('https' if secure else 'http') + '://' + host

    @asyncio.coroutine
    def chat_bind(self):
        route = MakeRoute(Endpoints.CHAT_BIND, base=self.url)
        return self.request(route)

    @asyncio.coroutine
    def fetch_info(self):
        route = MakeRoute(Endpoints.CHAT_INFO_FETCH, base=self.url)
        return self.request(route)

    @asyncio.coroutine
    def fetch_session(self):
        route = MakeRoute(Endpoints.CHAT_SESSION_FETCH, base=self.url)
        return self.request(route)

    @asyncio.coroutine
    def fetch_bans(self):
        route = MakeRoute(Endpoints.CHAT_BANS_FETCH, base=self.url)
        return self.request(route)

    @asyncio.coroutine
    def fetch_rooms(self):
        route = MakeRoute(Endpoints.CHAT_ROOMS_FETCH, base=self.url)
        return self.request(route)

    @asyncio.coroutine
    def ban(self, nickname, messages=None, room_id=None, ban_time=None, comment=None):
        route = MakeRoute(Endpoints.CHAT_NICKNAME_BAN, base=self.url)

        data = {
            'nick': nickname,
            'roomId': room_id,
            'minutes': ban_time,
            'comment': comment,
            'csrf': self.csrf_token,
        }

        return self.request(route, data=data)

    @asyncio.coroutine
    def unban(self, entries):
        route = MakeRoute(Endpoints.CHAT_NICKNAME_UNBAN, base=self.url)

        data = {
            'entries': entries if isinstance(entries, (str, int)) else ','.join(ban_entries),
            'csrf': self.csrf_token
        }

        return self.request(route, data=data)

    @asyncio.coroutine
    def moderate(self, nickname=None, message=None, room_id=None):
        route = MakeRoute(Endpoints.CHAT_NICKNAME_MODERATE, base=self.url)

        data = {
            'message': message,
            'nick': nickname,
            'roomId': room_id
        }

        return self.request(route, data=data)

    @asyncio.coroutine
    def fetch_nickname_info(self, nicknames):
        route = MakeRoute(Endpoints.CHAT_NICKNAME_FETCH, base=self.url)

        data = [('nick', nickname.lower()) for nickname in nicknames]

        return self.request(route, data=data)

    @asyncio.coroutine
    def open_room(self, room_id):
        route = MakeRoute(Endpoints.ROOM_OPEN, base=self.url)

        return self.request(route)

    @asyncio.coroutine
    def open_room_private(self):
        route = MakeRoute(Endpoints.ROOM_PRIVATE_OPEN, base=self.url)

        return self.request(route)

    @asyncio.coroutine
    def close_room(self):
        route = MakeRoute(Endpoints.ROOM_CLOSE, base=self.url)

        return self.request(route)

    @asyncio.coroutine
    def send_message(self, content, room_id):
        route = MakeRoute(Endpoints.ROOM_MESSAGE_SEND, base=self.url)

        return self.request(route)

    @asyncio.coroutine
    def read_messages(self):
        route = MakeRoute(Endpoints.ROOM_MESSAGES_READ, base=self.url)

        return self.request(route)

    @asyncio.coroutine
    def delete_messages(self):
        route = MakeRoute(Endpoints.ROOM_MESSAGES_DELETE, base=self.url)

        return self.request(route)

    @asyncio.coroutine
    def fetch_messages(self):
        route = MakeRoute(Endpoints.ROOM_MESSAGES_FETCH, base=self.url)

        return self.request(route)

    @asyncio.coroutine
    def enter_chat(self, nickname, limit=80, captcha=None):
        route = MakeRoute(Endpoints.USER_CHAT_ENTER, base=self.url)
        if captcha is None:
            captcha = {}

        data = {
            'nick': nickname,
            'limit': limit,
            'wid': self.window_id,
            'csrf': self.csrf_token,
            'captchaSid': captcha.sid,
            'captchaValue': captcha.value,
        }

        return self.request(route, data=data)

    @asyncio.coroutine
    def leave_chat(self):
        route = MakeRoute(Endpoints.USER_CHAT_LEAVE, base=self.url)

        params = {
            'wid': self.window_id,
            'csrf': self.csrf_token,
        }

        return self.request(route, params=params)

    @asyncio.coroutine
    def set_user_age(self):
        route = MakeRoute(Endpoints.USER_AGE_SET, base=self.url)

        return self.request(route)

    @asyncio.coroutine
    def set_user_status(self):
        route = MakeRoute(Endpoints.USER_STATUS_SET, base=self.url)

        return self.request(route)

    @asyncio.coroutine
    def register(self):
        route = MakeRoute(Endpoints.USER_REGISTER, base=self.url)

        return self.request(route)
