from .events_collection import EventsCollection


APIEvents = EventsCollection()


@APIEvents.register
class SetOptionAdapter:
    event_type = "so"
    new_type = "set_option"
    transforms = {"k": "option", "v": "value"}


@APIEvents.register
class CLSAdapter:
    event_type = "cls"
    transforms = {
        "accountName": "email",
        "accountType": "account_type",
        "accountGroup": "user_group",
        "lastNick": "last_nickname",
    }


@APIEvents.register
class ChatEmojisAdapter:
    event_type = "sl"
    new_type = "chat_emojis"
    transforms = {
        "smileys": "emojis",
        "cats": "groups",
        "dp": "default_path",
        "p": "custom_path",
    }


@APIEvents.register
class ErrorAdapter:
    event_type = "error"
    transforms = {
        "et": "type",
        "est": "group",
        "error": "description",
        "r": "room_id",
        "ts": "timestamp",
    }


@APIEvents.register
class MessageAdapter:
    event_type = "m"
    new_type = "message"
    transforms = {
        "ts": "timestamp",
        "f": "author",
        "m": "content",
        "r": "room_id",
        "actions": "actions",
    }


@APIEvents.register
class MessageDeleteAdapter:
    event_type = "md"
    new_type = "message_delete"
    transforms = {"ts": "messages", "r": "room_id"}


@APIEvents.register
class MessageReadAdapter:
    event_type = "pmr"
    new_type = "message_read"
    transforms = {"fromTime": "from_ts", "toTime": "until_ts"}


@APIEvents.register
class RoomUpdateAdapter:
    event_type = "ru"
    new_type = "room_update"
    transforms = {"closeable": "can_be_closed", "showEnterLeave": "display_user_flow"}


@APIEvents.register
class RoomOpenAdapter:
    event_type = "ro"
    new_type = "room_open"
    transforms = {
        "r": "room_id",
        "channelType": "type",
        "active": "set_focus",
        "title": "name",
        "closeable": "can_be_closed",
        "showEnterLeave": "display_user_flow",
    }


@APIEvents.register
class RoomCloseAdapter:
    event_type = "rc"
    new_type = "room_close"
    transforms = {"r": "room_id", "iwid": "window_id"}


@APIEvents.register
class HasOlderEventsAdapter:
    event_type = "hoe"
    new_type = "has_older_events"
    transforms = {"r": "room_id", "hasOlderEvents": "value"}


@APIEvents.register
class UserLeaveAdapter:
    event_type = "ul"
    new_type = "user_leave"
    transforms = {"nick": "nickname"}


@APIEvents.register
class UserEnterAdapter:
    event_type = "ue"
    new_type = "user_enter"
    transforms = {}


@APIEvents.register
class UserEnterRoomAdapter:
    event_type = "uer"
    new_type = "user_enter_room"
    transforms = {}


@APIEvents.register
class UserLeaveRoomAdapter:
    event_type = "ulr"
    new_type = "user_leave_room"
    transforms = {}
