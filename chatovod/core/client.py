import asyncio

from chatovod.core.chat import ChatState
from chatovod.core.http import HTTPClient


class Client:

    def __init__(self, chat_name, custom=False, loop=None):

        if custom:
            host = chat_name
        else:
            host = '{}.chatovod.com'.format(chat_name)

        self.host = host
        self.loop = loop if loop else asyncio.get_event_loop()
        self.http = HTTPClient(host=self.host, loop=loop)
        self._state = ChatState(client=self, http=self.http)

    def run(self, *args, **kwargs):

        loop = self.loop

        task = loop.create_task(self.start(*args, **kwargs))
        task.add_done_callback(lambda f: loop.stop())

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            try:
                loop.run_until_complete(self.close())
            finally:
                loop.close()

            return task.result()

    @asyncio.coroutine
    def start(self, *args, **kwargs):
        if len(args) > 0:
            yield from self.login(*args)
        yield from self.init()

    @asyncio.coroutine
    def init(self):
        yield from self.http.fetch_session()
        yield from self.http.fetch_info()

    @asyncio.coroutine
    def close(self):
        # TODO: Only if logged in
        yield from self.http.logout()

        yield from self.http.close()

    @asyncio.coroutine
    def login(self, email, password):
        yield from self.http.login(email, password)
