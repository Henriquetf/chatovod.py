import asyncio

from chatovod.core.chat import ChatState
from chatovod.core.http import HTTPClient


class Client:

    def __init__(self, chat_name, custom=False, loop=None):

        if custom:
            host = chat_name
        else:
            host = '{}.chatovod.com'.format(chat_name)

        self._host = host
        self._loop = loop if loop else asyncio.get_event_loop()
        self._http = HTTPClient(host=self._host, loop=loop)
        self._state = ChatState(client=self, http=self._http)
