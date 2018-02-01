import aiohttp
import asyncio
import json
# import yarl

from chatovod.api.endpoints import AccountEndpoint
from chatovod.api.endpoints import APIEndpoint as Endpoints
from chatovod.api.endpoints import make_route as MakeRoute

from chatovod import __version__


class HTTPClient:

    def __init__(self, host, secure=True, client=None, loop=None):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self._session = aiohttp.ClientSession(loop=self.loop)

        self.window_id = 0

        self.host = host
        self.secure = secure
        self.url = self.make_url(host=self.host, secure=self.secure)

        # TODO: define the user-agent
        user_agent = 'ChatovodBot (https://github.com/Coquetoon/chatovod.py {0}) Firefox/Bot'
        self.user_agent = user_agent.format(__version__)

    @property
    def csrf_token(self):
        return self._filter_cookies(self.url).get('csrf').value

    @property
    def session_id(self):
        cookies = self._filter_cookies.get(self.session_id_type)
        return cookies.get('ssid' if self.secure else 'sid').value

    @property
    def account_csrf_token(self):
        return self._filter_cookies(AccountEndpoint.BASE).get('csrf').value

    def _filter_cookies(self, request_url):
        return self._session.cookie_jar.filter_cookies(request_url)

    def _patch_request_data(self, req_data):
        params = req_data.get('params')
        data = req_data.get('data')
        # aiohttp doesn't filter out None parameters
        if params:
            req_data['params'] = {k: v for k, v in params.items() if v is not None}

        if data:
            req_data['data'] = {k: v for k, v in data.items() if v is not None}


    @asyncio.coroutine
    def request(self, route, headers=None, return_raw=False, **kwargs):
        method = route.method
        url = route.url

        self._patch_request_data(kwargs)

        kwargs['headers'] = {'User-Agent': self.user_agent}
        if headers:
            kwargs['headers'].update(headers)

        response = yield from self._session.request(method, url, **kwargs)

        try:
            if return_raw:
                return response

            text = yield from response.text(encoding='utf-8')

            if response.content_type == 'application/json':
                data = json.loads(text)
            else:
                data = text

            if 200 <= response.status < 300:
                return data
        finally:
            # Prevents 'Unclosed connection' and 'Unclosed response'
            yield from response.release()

    def raw_request(self, *args, **kwargs):
        return self.request(*args, return_raw=True, **kwargs)

    @classmethod
    def make_url(cls, host, secure):
        return ('https' if secure else 'http') + '://' + host

    @asyncio.coroutine
    def chat_bind(self):
        route = MakeRoute(Endpoints.CHAT_BIND, base=self.url)
        return self.request(route)

    @asyncio.coroutine
    def fetch_info(self, limit=20):
        route = MakeRoute(Endpoints.CHAT_INFO_FETCH, base=self.url)

        params = {
            'limit': limit
        }

        return self.request(route, params=params)

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
    def open_room(self, room_id, force_active=False, limit=20):
        route = MakeRoute(Endpoints.ROOM_OPEN, base=self.url)

        params = {
            'roomId': room_id,
            'forceActive': force_active,
            'wid': self.window_id,
            'limit': limit,
        }

        return self.request(route)

    @asyncio.coroutine
    def open_room_private(self, nickname, limit=20):
        route = MakeRoute(Endpoints.ROOM_PRIVATE_OPEN, base=self.url)

        params = {
            'nick': nickname,
            'limit': limit,
            'wid': self.window_id,
        }

        return self.request(route, params=params)

    @asyncio.coroutine
    def close_room(self):
        route = MakeRoute(Endpoints.ROOM_CLOSE, base=self.url)

        params = {
            'roomId': room_id,
            'wid': self.window_id,
        }

        return self.request(route, params=params)

    @asyncio.coroutine
    def send_message(self, content, room_id, to=None):
        route = MakeRoute(Endpoints.ROOM_MESSAGE_SEND, base=self.url)

        data = {
            'csrf': self.csrf_token,
            'msg': content,
            'roomId': room_id,
            'to': to,
        }

        return self.request(route, data=data)

    @asyncio.coroutine
    def read_messages(self, room_id, fromTime, toTime):
        route = MakeRoute(Endpoints.ROOM_MESSAGES_READ, base=self.url)

        params = {
            'channelId': room_id,
            'fromTime': from_time,
            'toTime': to_time,
        }

        return self.request(route, params=params)

    @asyncio.coroutine
    def delete_messages(self, room_id, messages):
        route = MakeRoute(Endpoints.ROOM_MESSAGES_DELETE, base=self.url)

        params = {
            'csrf': self.csrf_token,
            'messages': ','.join([str(v) for v in messages]),
            'roomId': room_id,
        }

        return self.request(route, params=params)

    @asyncio.coroutine
    def fetch_messages(self):
        route = MakeRoute(Endpoints.ROOM_MESSAGES_FETCH, base=self.url)

        return self.request(route)

    @asyncio.coroutine
    def enter_chat(self, nickname, limit=20, captcha={}):
        route = MakeRoute(Endpoints.USER_CHAT_ENTER, base=self.url)
        data = {
            'nick': nickname,
            'limit': limit,
            'wid': self.window_id,
            'csrf': self.csrf_token,
            'captchaSid': captcha.get('sid'),
            'captchaValue': captcha.get('value'),
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

    @asyncio.coroutine
    def login(self, email, password):
        # Fetch CSRF token, necessary for posting the login, and session ID
        yield from self._fetch_account_session()
        # Post login
        login_response = yield from self._post_login(email, password)

        # TODO: Implement on login error

        yield from self._associate_account()

    @asyncio.coroutine
    def _fetch_account_session(self):
        return self.raw_request(AccountEndpoint.LOGIN_PAGE)

    @asyncio.coroutine
    def _post_login(self, email, password):
        params = {
            'csrf': self.account_csrf_token,
            'login': email,
            'password': password,
        }

        return self.raw_request(AccountEndpoint.LOGIN, params=params)

    def _associate_account(self):
        route = MakeRoute(AccountEndpoint.ASSOCIATE_ACCOUNT, base=self.url)
        return self.raw_request(route, params={'n': 'ch'})
