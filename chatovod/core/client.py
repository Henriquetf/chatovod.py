import asyncio
import logging

from .chat import Chat
from .http import HTTPClient
from .client_user import ClientUser

log = logging.getLogger(__name__)


class Client:

    def __init__(self, chat_name, custom=False, loop=None):
        self.host = chat_name if custom else '{}.chatovod.com'.format(chat_name)
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.user = ClientUser(client=self)
        self.http = HTTPClient(host=self.host, loop=loop)
        self.chat = Chat(client=self, user=self.user, http=self.http, loop=self.loop)

    def run(self, *args, **kwargs):
        loop = self.loop

        start_coro = self.start(*args, **kwargs)
        task = loop.create_task(start_coro)

        def on_task_done(future):
            loop.stop()

        task.add_done_callback(on_task_done)

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
        self.chat._listen()

        while True:
            try:
                event = yield from self.chat._get_event()
            except:
                # TODO: handle exception
                raise
            else:
                if isinstance(event, list):
                    yield from self.chat._handle_event_stream(event)
                else:
                    yield from self.chat._handle_event(event)

    @asyncio.coroutine
    def close(self):
        # TODO: Only if signed in
        # yield from self.http.leave_chat()
        # TODO: Only if logged in
        # yield from self.http.logout()
        ...
        # yield from self.http.close()

    @asyncio.coroutine
    def login(self, email, password):
        log.info('Attempting to login')
        yield from self.http.login(email, password)
