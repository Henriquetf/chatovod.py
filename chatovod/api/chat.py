from .http import HTTPClient
from collections import deque, OrderedDict


class ChatState:

    def __init__(self, client, http):
        self.client = client
        self._http = http

    def reset(self):
        self._users = OrderedDict()
        self._rooms = OrderedDict()
        self._emojis = {}
        self._emojis_groups = []

    @property
    def url(self):
        return self._http.url

    def handle_start(self, data):
        start_data = StartData(data)

        for user_data in start_data['users']:
            user = User(data=user_data, state=self)

        for room_data in start_data['rooms']:
            room = Room(data=room_data, state=self)
            self._add_room(room)

        emojis = start_data['emojis']
        emoji_groups = start_data['emoji_groups']

        client_info = start_data['client_info']
        self._http._window_id = client_info['window_id']

    def handle_user_enter_chat(self, event):
        user = User(data=event, state=self)
        self._add_user(user)

        self.dispatch('user_enter_chat', user)

    def handle_user_leave_chat(self, event):
        user = self.get_user(event['nickname'])
        self._remove_user(user)

        self.dispatch('user_leave_chat', user)

    def handle_user_enter_room(self, event):
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
