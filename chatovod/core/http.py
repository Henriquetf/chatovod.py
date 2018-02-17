import aiohttp
import asyncio
import json
import logging

from yarl import URL

from chatovod import __version__
from chatovod.api.endpoints import AccountEndpoint, Route
from chatovod.api.endpoints import APIEndpoint as Endpoints

from .errors import error_factory, InvalidLogin

logger = logging.getLogger(__name__)


class HTTPClient:

    def __init__(self, host, secure=True, client=None, loop=None):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self._session = aiohttp.ClientSession(loop=self.loop)

        self.window_id = 0

        self.host = host
        self.secure = secure

        scheme = 'https' if secure else 'http'
        self.url = URL.build(scheme=scheme, host=host)

        user_agent = 'ChatovodBot (https://github.com/Coquetoon/chatovod.py {0}) Firefox/Bot'
        self.user_agent = user_agent.format(__version__)

    @property
    def csrf_token(self):
        return self._filter_cookies(self.url).get('csrf').value

    @property
    def session_id(self):
        cookies = self._filter_cookies.get(self.session_id_type)
        return cookies.get('ssid' if self.secure else 'sid').value

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
            is_json = response.content_type == 'application/json'

            if is_json:
                data = json.loads(text)
            else:
                data = text

            if 200 <= response.status < 300:
                if is_json:
                    if isinstance(data, dict) and data.get('t') == 'error':
                        error = error_factory(data)
                        raise error

                logger.debug('"%s %s" has received %s', method, url, data)
                return data

        finally:
            # Prevents 'Unclosed connection' and 'Unclosed response'
            yield from response.release()

    def raw_request(self, *args, **kwargs):
        return self.request(*args, return_raw=True, **kwargs)

    @asyncio.coroutine
    def close(self):
        yield from self._session.close()

    def chat_bind(self):
        route = Route(path=Endpoints.CHAT_BIND, url=self.url)
        return self.request(route)

    def fetch_info(self, limit=20):
        route = Route(path=Endpoints.CHAT_INFO_FETCH, url=self.url)

        params = {
            'limit': limit
        }

        return self.request(route, params=params)

    def fetch_session(self):
        route = Route(path=Endpoints.CHAT_SESSION_FETCH, url=self.url)
        return self.request(route)

    def fetch_bans(self):
        route = Route(path=Endpoints.CHAT_BANS_FETCH, url=self.url)
        return self.request(route)

    def fetch_rooms(self):
        route = Route(path=Endpoints.CHAT_ROOMS_FETCH, url=self.url)
        return self.request(route)

    def ban(self, nickname, messages=None,
            room_id=None, ban_time=None, comment=None):
        route = Route(path=Endpoints.CHAT_NICKNAME_BAN, url=self.url)

        data = {
            'nick': nickname,
            'roomId': room_id,
            'minutes': ban_time,
            'comment': comment,
            'csrf': self.csrf_token,
        }

        return self.request(route, data=data)

    def unban(self, entries):
        route = Route(path=Endpoints.CHAT_NICKNAME_UNBAN, url=self.url)

        data = {
            'entries': entries if isinstance(entries, (str, int)) else ','.join(ban_entries),
            'csrf': self.csrf_token
        }

        return self.request(route, data=data)

    def moderate(self, nickname=None, message=None, room_id=None):
        route = Route(path=Endpoints.CHAT_NICKNAME_MODERATE, url=self.url)

        data = {
            'message': message,
            'nick': nickname,
            'roomId': room_id
        }

        return self.request(route, data=data)

    def fetch_nickname_info(self, nicknames):
        route = Route(path=Endpoints.CHAT_NICKNAME_FETCH, url=self.url)

        data = [('nick', nickname.lower()) for nickname in nicknames]

        return self.request(route, data=data)

    def open_room(self, room_id, force_active=False, limit=20):
        route = Route(path=Endpoints.ROOM_OPEN, url=self.url)

        params = {
            'roomId': room_id,
            'forceActive': force_active,
            'wid': self.window_id,
            'limit': limit,
        }

        return self.request(route)

    def open_room_private(self, nickname, limit=20):
        route = Route(path=Endpoints.ROOM_PRIVATE_OPEN, url=self.url)

        params = {
            'nick': nickname,
            'limit': limit,
            'wid': self.window_id,
        }

        return self.request(route, params=params)

    def close_room(self):
        route = Route(path=Endpoints.ROOM_CLOSE, url=self.url)

        params = {
            'roomId': room_id,
            'wid': self.window_id,
        }

        return self.request(route, params=params)

    def send_message(self, content, room_id, to=None):
        route = Route(path=Endpoints.ROOM_MESSAGE_SEND, url=self.url)

        data = {
            'csrf': self.csrf_token,
            'msg': content,
            'roomId': room_id,
            'to': to,
        }

        return self.request(route, data=data)

    def read_messages(self, room_id, fromTime, toTime):
        route = Route(path=Endpoints.ROOM_MESSAGES_READ, url=self.url)

        params = {
            'channelId': room_id,
            'fromTime': from_time,
            'toTime': to_time,
        }

        return self.request(route, params=params)

    def delete_messages(self, room_id, messages):
        route = Route(path=Endpoints.ROOM_MESSAGES_DELETE, url=self.url)

        params = {
            'csrf': self.csrf_token,
            'messages': ','.join([str(v) for v in messages]),
            'roomId': room_id,
        }

        return self.request(route, params=params)

    def delete_message(self, room_id, message_id):
        return self.delete_messages(room_id, [message_id])

    def fetch_messages(self):
        route = Route(path=Endpoints.ROOM_MESSAGES_FETCH, url=self.url)

        return self.request(route)

    def enter_chat(self, nickname, limit=20, captcha={}):
        route = Route(path=Endpoints.USER_CHAT_ENTER, url=self.url)
        data = {
            'nick': nickname,
            'limit': limit,
            'wid': self.window_id,
            'csrf': self.csrf_token,
            'captchaSid': captcha.get('sid'),
            'captchaValue': captcha.get('value'),
        }

        return self.request(route, data=data)

    def leave_chat(self):
        route = Route(path=Endpoints.USER_CHAT_LEAVE, url=self.url)

        params = {
            'wid': self.window_id,
            'csrf': self.csrf_token,
        }

        return self.request(route, params=params)

    def set_user_age(self):
        route = Route(path=Endpoints.USER_AGE_SET, url=self.url)

        return self.request(route)

    def set_user_status(self):
        route = Route(path=Endpoints.USER_STATUS_SET, url=self.url)

        return self.request(route)

    def register(self):
        route = Route(path=Endpoints.USER_REGISTER, url=self.url)

        return self.request(route)

    @asyncio.coroutine
    def login(self, email, password):
        # Fetch CSRF token, necessary for posting the login, and session ID
        yield from self._fetch_account_session()
        # Post login
        login_response = yield from self._post_login(email, password)

        if login_response.headers['Location'] != 'https://account.chatovod.com/u/':
            raise InvalidLogin()

        yield from self._associate_account()

    def logout(self):
        return self.raw_request(AccountEndpoint.LOGOUT)

    def _fetch_account_session(self):
        return self.raw_request(AccountEndpoint.LOGIN_PAGE)

    def _post_login(self, email, password):
        params = {
            'csrf': self._filter_cookies(AccountEndpoint.BASE).get('csrf').value,
            'login': email,
            'password': password,
        }

        return self.raw_request(AccountEndpoint.LOGIN, params=params, allow_redirects=False)

    def _associate_account(self):
        route = Route(path=AccountEndpoint.ASSOCIATE_ACCOUNT, url=self.url)
        return self.raw_request(route, params={'n': 'ch'})
