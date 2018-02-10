import asyncio
import threading
import logging

from collections import deque, OrderedDict

from .errors import ConnectionReset, ConnectionError
from .http import HTTPClient

log = logging.getLogger(__name__)


class Chat:

    def __init__(self, client, user, http, loop):
        self.client = client
        self.user = user
        self.loop = loop
        self._http = http
        self._event_listener = EventListener(chat=self)
        self._event_handler = EventHandler(chat=self)

    def _listen(self):
        log.debug('Initializing event listener')
        runner = self._event_listener.run()
        self.loop.create_task(runner)

    def reset(self):
        self._users = OrderedDict()
        self._rooms = OrderedDict()
        self._emojis = []
        self._emojis_groups = []
        self._emojis_base_path = None
        self._custom_emojis_base_path = None

    @property
    def url(self):
        return self._http.url

    def _get_user(self, nickname):
        return self.users[nickname.lower()]

    def _add_user(self, user):
        nickname = user.nickname.lower()
        self._users[nickname] = user

    def _remove_user(self, user):
        return self._users.pop(user.nickname.lower())

    def _get_room(self, room_id):
        return self._rooms.get(room_id)

    def _add_room(self, room):
        self._rooms[room.id] = room

    def _remove_room(self, room):
        self._rooms.pop(room.id)

    @asyncio.coroutine
    def _get_event(self):
        event = yield from self._event_listener.event_stream.get()

        if isinstance(event, Exception):
            raise event
        return event

    @asyncio.coroutine
    def _handle_event_stream(self, event_stream):
        ...

    @asyncio.coroutine
    def _handle_event(self, event):
        ...

class EventListener:

    def __init__(self, chat, *args, **kwargs):
        self.chat = chat
        self.event_stream = asyncio.Queue()
        self._closed = asyncio.Event()

    @asyncio.coroutine
    def run(self):
        while not self._closed.is_set():
            try:
                response = yield from self.chat._http.chat_bind()
            except (ConnectionReset, ConnectionError) as e:
                log.warning('A %s error occurred during event bind', e.__name__)
                yield from self.event_stream.put(e)
                self.stop()
            else:
                yield from self.event_stream.put(response)

    def stop(self):
        self._closed.set()


class EventHandler:

    def __init__(self, chat):
        self.chat = chat

    def _(self, data):
        event = data.get('t')

        if issubclass(event, str):
            try:
                handler = getattr(self, 'handle_' + event)
            except AttributeError:
                # log.info('Unhandled event {}')
                ...
            else:
                handler(data)
        else:
            try:
                self._handle_typeless_event(data)
            except AttributeError:
                # log.info('')
                ...

    def _handle_start(self, data):
        for _raw in data:
            transformed, raw = transform_event(_raw)
            event = raw.get('t')
            handle_name = 'handle_' + event

            if event in ('set_option', 'chat_emojis', 'error') and hasattr(self, handle_name):
                handler = getattr(self, handle_name)
                handler(raw)
            elif event == 'room_open':
                room = self._create_room(raw)
                self._add_room(room)
            elif event == 'message':
                message = self._create_message(message)
                self._cache_message(message)
            elif event == 'has_older_events':
                # TODO: Implement this
                ...
            else:
                log.info('Unhandled event %s, transformed: %s', _raw, transformed)

    def handle_set_option(self, raw):
        option = raw['option']
        value = raw.get('value')

        log.debug("Setting option '%s' to '%s'", option, value)

        if option == 'nick':
            self.user.nickname = value
        elif option == 'signedIn':
            self.user.signed_in = value
        elif option == 'wid':
            self._http.window_id = value
        else:
            log.info('Unhandled option %s:%s', option, raw)

    def handle_chat_emojis(self, raw):
        self._emojis_base_path = raw['default_path']
        self._custom_emojis_base_path = raw.get('custom_path')

        for raw_group in raw['groups']:
            group = self._create_emoji_group(raw_group)
            self._add_emoji_group(group)

        for raw_emoji in raw['emojis']:
            emoji = self._create_emoji(raw_emoji)
            self._add_emoji(emoji)

    def handle_error(self, raw):
        ...

    def handle_room_open(self, event):
        pass
