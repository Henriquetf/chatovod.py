import asyncio

from abc import ABCMeta, abstractmethod


class Message(metaclass=ABCMeta):

    __slots__ = ()

    @asyncio.coroutine
    def delete_later(self):
        self.chat._add_message_to_delete(self)

    @asyncio.coroutine
    def delete(self):
        yield from self.chat._http.delete_message(self.room.id, self.id)

    async def send(self, content):
        room = self._get_room()

        return await self._state.http.room_message_send(content, room.id)
