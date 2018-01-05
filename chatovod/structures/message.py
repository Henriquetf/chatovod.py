
class MessageBase:

    def __init__(self, *, event):
        self.id = str(event['ts'])

        self._old = event.get('s', False)
        self.fetched = event.get('pp', False)

    @property
    def old(self):
        return self._old or self.fetched


class Message(MessageBase):

    def __init__(self, *, author, room, event):
        self.author = author
        self.room = room

    def _update(self, event):
        self.content = event['m']
        self.to = event.get('to', [])
        self.cmd_me = event.get('nh', False)

        self.seen = not event.get('u', True)
