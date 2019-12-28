from chatovod.structures import abc as ChatovodABC


class Message(ChatovodABC.Message):
    def __init__(self, *, chat, room, data):
        self.chat = chat
        self.room = room
        self.id = data["timestamp"]
        self.author = data.get("author")

        self.content = data["content"]
        self.to = data.get("to", [])
        self.cmd_me = data.get("nh", False)

        self.seen = not data.get("u", True)

        self._old = data.get("s", False)
        self.fetched = data.get("pp", False)

    @property
    def old(self):
        return self._old or self.fetched
