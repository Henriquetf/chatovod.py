
ADAPTERS_MAP = {}


def transform(data, transforms):
    return {
        transforms.get(k, k): v
        for k, v in data.items()
    }


class EventAdapterMeta(type):

    def __new__(cls, name, bases, namespace, **kwds):
        inst = type.__new__(cls, name, bases, namespace)

        event_type = namespace.get('type')
        if event_type is not None:
            ADAPTERS_MAP[event_type] = inst

        return inst


class EventAdapter(metaclass=EventAdapterMeta):

    @classmethod
    def adapt(cls, data):
        transformed = transform(data, cls.transforms)

        # Patch the type of the event
        try:
            new_type = getattr(cls, 'new_type')
        except AttributeError:
            pass
        else:
            transformed['t'] = new_type

        return transformed


class SetOptionAdapter(EventAdapter):
    type = 'so'
    new_type = 'set_option'
    transforms = {
        'k': 'option',
        'v': 'value',
    }


class CLSAdapter(EventAdapter):
    type = 'cls'
    transforms = {
        'accountName': 'email',
        'accountType': 'account_type',
        'accountGroup': 'user_group',
        'lastNick': 'last_nickname',
    }


class ChatEmojisAdapter(EventAdapter):
    type = 'sl'
    new_type = 'chat_emojis'
    transforms = {
        'smileys': 'emojis',
        'cats': 'groups',
        'dp': 'default_path',
        'p': 'custom_path',
    }


class ErrorAdapter(EventAdapter):
    type = 'error'
    transforms = {
        'et': 'type',
        'est': 'group',
        'error': 'description',
        'r': 'room_id',
        'ts': 'timestamp',
    }


class MessageAdapter(EventAdapter):
    type = 'm'
    new_type = 'message'
    transforms = {
        'ts': 'timestamp',
        'f': 'author',
        'm': 'content',
        'r': 'room_id',
        'actions': 'actions',
    }


class MessageDeleteAdapter(EventAdapter):
    type = 'md'
    new_type = 'message_delete'
    transforms = {
        'ts': 'messages',
        'r': 'room_id',
    }


class MessageReadAdapter(EventAdapter):
    type = 'pmr'
    new_type = 'message_read'
    transforms = {
        'fromTime': 'from_ts',
        'toTime': 'until_ts',
    }


class RoomUpdateAdapter(EventAdapter):
    type = 'ru'
    new_type = 'room_update'
    transforms = {
        'closeable': 'can_be_closed',
        'showEnterLeave': 'display_user_flow',
    }


class RoomOpenAdapter(EventAdapter):
    type = 'ro'
    new_type = 'room_open'
    transforms = {
        'r': 'room_id',
        'channelType': 'type',
        'active': 'set_focus',
        'title': 'name',
        'closeable': 'can_be_closed',
        'showEnterLeave': 'display_user_flow',
    }


class RoomCloseAdapter(EventAdapter):
    type = 'rc'
    new_type = 'room_close'
    transforms = {
        'r': 'room_id',
        'iwid': 'window_id',
    }


class HasOlderEventsAdapter(EventAdapter):
    type = 'hoe'
    new_type = 'has_older_events'
    transforms = {
        'r': 'room_id',
        'hasOlderEvents': 'value',
    }


class UserLeaveAdapter(EventAdapter):
    type = 'ul'
    new_type = 'user_leave'
    transforms = {
        'nick': 'nickname',
    }


class UserEnterAdapter(EventAdapter):
    type = 'ue'
    new_type = 'user_enter'
    transforms = {}


class UserEnterRoomAdapter(EventAdapter):
    type = 'uer'
    new_type = 'user_enter_room'
    transforms = {}


class UserLeaveRoomAdapter(EventAdapter):
    type = 'ulr'
    new_type = 'user_leave_room'
    transforms = {}
