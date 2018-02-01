class Message:

    def __init__(self, *, room, data):
        self.id = data['timestamp']

        self.content = data['content']
        self.to = data.get('to', [])
        self.cmd_me = data.get('nh', False)

        self.seen = not data.get('u', True)

        self._old = data.get('s', False)
        self.fetched = data.get('pp', False)
        self.room = room
        self._handle_author(data)

    def _handle_author(self, data):
        self.author = author

    @property
    def old(self):
        return self._old or self.fetched
