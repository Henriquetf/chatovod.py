import aiohttp
import asyncio
import json

from .endpoints import APIEndpoint as APIE


class HTTPClient:

    def __init__(self, host, secure=True, client=None, loop=None):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self._session = aiohttp.ClientSession(loop=self.loop)

        self.session_id = None
        self.csrf_token = None
        self.window_id = 0

        self.host = host
        self.secure = secure
        self.url = self.make_url(self.host, self.secure)

        # TODO: define the user-agent
        self.user_agent = ''

    @asyncio.coroutine
    def request(self, route, **kwargs):
        method = route.method
        url = route.url

        headers = {
            'User-Agent': self.user_agent
        }

        if 'headers' in kwargs:
            headers = headers.update(kwargs.pop('headers'))

        kwargs['headers'] = headers

        response = yield from self._session.request(method, url, **kwargs)

        if 200 <= response.status < 300:
            text = yield from response.text(encoding='utf-8')
            return text

    @classmethod
    def make_url(cls, host, secure):
        return ('https' if secure else 'http') + '://' + host

    @asyncio.coroutine
    def chat_bind(self):
        return self.request(APIE.CHAT_BIND(self.url))

    @asyncio.coroutine
    def fetch_info(self):
        return self.request(APIE.CHAT_INFO_FETCH(self.url))

    @asyncio.coroutine
    def fetch_session(self):
        route = APIE.CHAT_SESSION_FETCH(self.url)
        return self.request(route)

    @asyncio.coroutine
    def fetch_bans(self):
        route = APIE.CHAT_BANS_FETCH(self.url)
        return self.request(route)

    @asyncio.coroutine
    def fetch_rooms(self):
        route = APIE.CHAT_ROOMS_FETCH(self.url)
        return self.request(route)

    @asyncio.coroutine
    def ban(self, nickname, messages=None, room_id=None, ban_time=None, comment=None):
        route = APIE.CHAT_NICKNAME_BAN(self.url)

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
        route = APIE.CHAT_NICKNAME_UNBAN(self.url)

        data = {
            'entries': entries if isinstance(entries, str) else ','.join(ban_entries),
            'csrf': self.csrf_token
        }

        return self.request(route, data=data)

    @asyncio.coroutine
    def moderate(self, nickname=None, message=None, room_id=None):
        route = APIE.CHAT_NICKNAME_MODERATE(self.url)

        data = {
            'message': message,
            'nick': nickname,
            'roomId': room_id
        }

        return self.request(route, data=data)

    @asyncio.coroutine
    def fetch_nickname_info(self, nicknames):
        route = APIE.CHAT_NICKNAME_FETCH(self.url)

        data = [('nick', nickname) for nickname in nicknames]

        return self.request(route, data=data)

    @asyncio.coroutine
    def open_room(self, room_id):
        route = Endpoint.ROOM_OPEN

        return self.request(route)

    @asyncio.coroutine
    def open_room_private(self):
        route = Endpoint.ROOM_PRIVATE_OPEN

        return self.request(route)

    @asyncio.coroutine
    def close_room(self):
        route = Endpoint.ROOM_CLOSE

        return self.request(route)

    @asyncio.coroutine
    def send_message(self, content, room_id):
        route = Endpoint.ROOM_MESSAGE_SEND

        return self.request(route)

    @asyncio.coroutine
    def read_messages(self):
        route = Endpoint.ROOM_MESSAGES_READ

        return self.request(route)

    @asyncio.coroutine
    def delete_messages(self):
        route = Endpoint.ROOM_MESSAGES_DELETE

        return self.request(route)

    @asyncio.coroutine
    def fetch_messages(self):
        route = Endpoint.ROOM_MESSAGES_FETCH

        return self.request(route)

    @asyncio.coroutine
    def enter_chat(self, nickname, limit=80, captcha=None):
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
    def leave_chat(self):
        route = Endpoint.USER_CHAT_LEAVE

        params = {
            'wid': self.window_id,
            'csrf': self.csrf_token,
        }

        return self.request(route, params=params)

    @asyncio.coroutine
    def set_user_age(self):
        route = Endpoint.USER_AGE_SET

        return self.request(route)

    @asyncio.coroutine
    def set_user_status(self):
        route = Endpoint.USER_STATUS_SET

        return self.request(route)

    @asyncio.coroutine
    def register(self):
        route = Endpoint.USER_REGISTER

        return self.request(route)
