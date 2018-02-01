from .http import HTTPClient
from collections import deque, OrderedDict


def _make_room_patch(raw):
    return {
        'room': raw,
        'messages': [],
        'errors': [],
        'has_older_events': None
    }

def transform_start(data):
    patch = {
        'options': [],
        'chat_emojis': [],
        'rooms': {},
    }

    for _raw in data:
        transformed, raw = transform_event(_raw)
        event = raw.get('t')

        if 'room_id' in raw:
            room_id = raw['room_id']
            room = patch['rooms'].get(room_id)

        if event == 'set_option':
            patch['options'].append(raw)
        elif event == 'chat_emojis':
            patch['chat_emojis'].append(raw)
        elif event == 'room_open':
            patch['rooms'][room_id] = _make_room_patch(raw)
        elif event == 'message':
            room['messages'].append(raw)
        elif event == 'error':
            room['errors'].append(raw)
        elif event == 'has_older_events':
            room['has_older_events'] = raw['value']
        else:
            print('Unhandled event "{}", transformed: {}'.format(_raw, transformed))

    return patch


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
        self.handle_chat_emojis(data['chat_emojis'])

        for option in data['options']:
            self.handle_set_option(option)

        for room_info in data['rooms']:
            room_data = room_info['room']
            room = self._create_room(room_data)
            self._add_room(room)

    def handle_set_option(self, raw):
        option = raw['option']
        value = raw.get('value')

        if option == 'nick':
            set_nickname(value)
        elif option == 'wid':
            set_window_id(value)
        elif option == 'signedIn':
            set_signedIn(value)
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
