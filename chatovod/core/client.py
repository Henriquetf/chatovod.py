import asyncio
import logging

from .chat import Chat
from .client_user import ClientUser
from .http import HTTPClient

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, chat_name, custom=False, loop=None):
        self.host = chat_name if custom else "{}.chatovod.com".format(chat_name)
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.user = ClientUser(client=self)
        self.http = HTTPClient(host=self.host, loop=loop)
        self.chat = Chat(client=self, user=self.user, http=self.http, loop=self.loop)
        self.event_listener = self.chat._event_listener

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

    async def start(self, *args, **kwargs):
        if len(args) > 0:
            await self.login(*args)
        await self.init()

    async def init(self):
        await self.chat._start()

        while True:
            await self.event_listener.listen()

    async def close(self):
        # TODO: Only if signed in
        # await self.http.leave_chat()
        # TODO: Only if logged in
        # await self.http.logout()
        # await self.http.close()
        ...

    async def login(self, email, password):
        logger.info("Attempting to login")
        await self.http.login(email, password)
