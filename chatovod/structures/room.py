from chatovod.api.states import RoomType


class Room:
    """Represents a Chatovod room."""

    __slots__ = (
        "id",
        "type",
        "name",
        "can_be_closed",
        "display_user_flow",
        "welcome_message",
    )

    def __init__(self, *, data):
        self.id = data["room_id"]
        self.type = RoomType(data.get("type"))

        self.name = data.get("name")
        self.can_be_closed = data.get("can_be_closed", False)
        self.display_user_flow = data.get("display_user_flow", False)

        self.welcome_message = None


class PublicRoom(Room):
    ...


class PrivateRoom(Room):
    ...
