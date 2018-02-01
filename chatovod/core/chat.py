from .http import HTTPClient
from collections import deque, OrderedDict


class ChatState:

    def __init__(self, client, http):
        self.client = client
        self._http = http

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

    def handle_start(self, data):
        for _raw in data:
            transformed, raw = transform_event(_raw)
            event = raw.get('t')

            if event in ('set_option', 'chat_emojis', 'error'):
                handler = getattr(self, 'handle_' + event, None)

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
                log.info('Unhandled event "{}", transformed: {}'.format(_raw, transformed))

    def handle_set_option(self, raw):
        option = raw['option']
        value = raw.get('value')

        if option == 'nick':
            self._user.nickname = value
        elif option == 'signedIn':
            self._user.signed_in = value
        elif option == 'wid':
            self._http.window_id = value
        else:
            log.info('Unhandled option {} {}'.format(option, raw))

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
