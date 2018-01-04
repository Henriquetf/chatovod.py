from chatovod.api.states import RoomType


class Room:
    """Represents a Chatovod room."""

    __slots__ = ('id', 'type', 'name', 'can_be_closed',
                 'display_user_flow', 'welcome_message')

    def __init__(self, event):
        self.id = event['id']
        self.type = RoomType(event.get('t'))

        self.name = event.get('name')
        self.can_be_closed = event.get('closeable', False)
        self.display_user_flow = event.get('showEnterLeave', False)

        self.welcome_message = None
