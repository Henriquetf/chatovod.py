from chatovod.api.states import AccountService, RoomType, Group, Status, Gender
from chatovod.structures.model import Model
from chatovod.structures.field import Field


class EventAdapter(Model):

    _key_for_event_type = 't'

    @classmethod
    def extract_event_type_from_raw(cls, raw):
        return raw.get(cls._key_for_event_type)


class TryAutoLogin(EventAdapter):
    """
    """
    type = 'tal'


class SO(EventAdapter):
    """
    """
    type = 'so'


class CLS(EventAdapter):
    """
    """
    type = 'cls'


class CPO(EventAdapter):
    """
    """
    type = 'cpo'


class TabActivate(EventAdapter):
    """Event that changes the focus of the current selected room.

    Attributes
    ----------
    room : int
        The ID of the room which received the focus.
    scope : str
        The type of the focused object. Only has 'room' right now, which
        changes the focus of the current room.
    window : str
        The ID of the window which changed the selected room.
    """
    type = 'ta'

    room = Field(int, 'id')
    window = Field(int, 'iwid')
    scope = Field(str, 'type')


class EmojiList(EventAdapter):
    """Event that defines a list of the available emojis in the chat.

    Attributes
    ----------
    emojis : list
        A list of the available emojis.
    groups : list
        A list of emoji groups.
    default_path : str
        The base path for the default emojis provided by the service.
        Does not contain a transfer protocol. It must be defined by the client.
    custom_path : str
        The base path for custom emojis created by the chat owner.
        Does not contain a default transfer protocol,
        it must be defined by the client.
        None if there are not custom emojis.
    """
    type = 'sl'

    emojis = Field(list, 'smileys')
    groups = Field(list, 'cats')
    default_path = Field(str, 'dp')
    custom_path = Field(str, 'p')


class Error(EventAdapter):
    """Event that defines errors received by the API.

    This defines denied access and welcome messages.

    Attributes
    ----------
    description : str
        The explanation of the error provided by the API.
    group : str
        The generic type of the error.
    category : str
        The specific type, subgroup, of the error.
    """
    type = 'error'

    description = Field(str, 'error')
    group = Field(str, 'et')
    category = Field(str, 'est')


class ModerateInfo(EventAdapter):
    """Information of the user that can be seen only by a moderator.

    Attributes
    ----------
    banned : bool
        Whether the nickname is banned from the chat or not.
    message_ip : str
        IP of the user at the moment that the message was sent.
        None if a message was not specified.
    ip : str
        Last IP of the user.
        None if a user was not specified.
    location : str
        Last location of the user.
        None if there's no location.
    user_agent : str
        Last User Agent string of the user.
        None if there's no user agent.
    last_login : int
        UTC Timestamp of the last time the user logged into the chat.
        None if the nickname is not registered in the chat.
    registered_timestamp : int
        UTC Timestamp of when the nickname was registered in the chat.
        None if the nickname is not registered in the chat.
    nick_id : int
        ID of the nickname of the user.
        None if the nickname is not registered in Chatovod.
    nickname_created_timestamp : int
        UTC Timestamp of when the nickname was created in Chatovod.
        None if the nickname is not registered in Chatovod.
    account_id : int
        ID of the account of the user.
        None if the user is not logged into an account.
    account_service_name : int
        The type of service of the account.
        None if the user is not logged into an account.
    account_service_domain : int
        The domain of the service of the account.
        None if the user is not logged into an account.
    """
    type = 'mi'

    message_ip = Field(str, 'messageIp')

    ip = Field(str, 'lastIp')
    location = Field(str, 'lastIpGeo')

    user_agent = Field(str, 'lastUserAgent')

    nick_id = Field(int, 'nickId')
    account_id = Field(int, 'accountId')

    last_login = Field(int, 'lastEnterToChat')

    nickname_created_at = Field(int, 'createdInChat')
    registered_timestamp = Field(int, 'created')

    account_service_name = Field(AccountService, 'accountType')
    account_service_domain = Field(str, 'accountTypeTitle')

    banned = Field(bool, 'banned', default=False)


class RoomCount(EventAdapter):
    """Event that determines the amount of public rooms in the chat.

    Attributes
    ----------
    count : int
        The amount of public rooms in the chat.
    """
    type = 'urc'

    count = Field(int, 'count')


class Message(EventAdapter):
    """Message received event.

    Attributes
    ----------
    id : int
        ID of the message. The time, in UTC, when the message was sent.
    room : int
        ID of the room where the message was sent.
    content : str
        The text of the message.
    author : str
        The nickname user who sent the message.
    to : list
        A list of strings of all nicknames tagged in the message.
    cmd_me : bool
        Indicates if the message was sent with a `/me` command.
    old : bool
        Determines if the message was sent before the user entered the room.
        Normally gathered from `APIEndpoint.CHAT_INFO_FETCH`.
    fetched : bool
        Determines if the message is old and if it was
        retrieved with `ChatEndpoint.FETCH_MESSAGES`.
    """
    type = 'm'

    room_id = Field(int, 'r')
    actions = Field('actions')


class MessageDelete(EventAdapter):
    """Represents a message delete event.

    Attributes
    ----------
    room : int
        The ID of the room where the messages were deleted.
    messages : list
        A list of int timestamps of all deleted messages.
    """
    type = 'md'

    room = Field(int, 'r')
    messages = Field(list, 'ts')


class MessageRead:
    """Represents a message read event.

    Attributes
    ----------
    room : int
        The room where the message was read.
    since : int
        The oldest timestamp of read messages.
    until : int
        The most recent timestamp of the read messages.
    """
    type = 'pmr'

    room = Field(int, 'r')
    since = Field(int, 'fromTime')
    until = Field(int, 'toTime')


class RoomUpdate:
    """Represents a room update event.

    Attributes
    ----------
    id : int
        The ID of the updated room.
    name : str
        The name of the room.
    can_close : bool
        Determines if the room can be closed by the user or not.
    display_user_flow : true
        Determines if the room will disply user enter and leave messages.
    """
    type = 'ru'

    id = Field(int, 'r')
    name = Field(str, 'title')
    can_close = Field(bool, 'closeable')
    display_user_flow = Field(bool, 'showEnterLeave')


class RoomOpen(RoomUpdate):
    """Represents a room open event.

    Attributes
    ----------
    room_type : RoomType
        The type of the room.
    set_focus : bool
        Determines if the focus should be changed to the opened room.
    """
    type = 'ro'

    room_type = Field(RoomType, 'channelType')
    set_focus = Field(bool, 'active', False)


class RoomClose(EventAdapter):
    """Represents a room close event.

    id : int
        The ID of the room to be closed.
    window : str
        The ID of the window that closed the room.
    """
    type = 'rc'

    id = Field(int, 'r')
    iwid = Field(int, 'iwid', default=0)


class RoomClear(EventAdapter):
    """Represent a room clear event.

    Clears the messages of the room.

    Attributes
    ----------
    room : str
        The ID of the room to be cleared.
    scope : str
        The type of the cleared object. Only has 'room' right now, which
        clears the content of the room.
    """
    type = 'tc'

    room = Field(int, 'id')
    scope = Field(str, 'type')


class UserEnterChat:
    """Represents a user enter chat event."""
    type = 'ue'


class UserLeaveChat:
    """Represents a user leave chat event.

    Attributes
    ----------
    nickname : str
        The nickname of the user who left the chat.
    """
    type = 'ul'

    nickname = Field(str, 'nick')


class UserEnterRoom(MessageBase):
    """Represents a user enter room event."""
    type = 'uer'


class UserLeaveRoom(MessageBase):
    """Represents a user leave room event."""
    type = 'ulr'


class UserBan:
    """Represents a user ban event.

    Attributes
    ----------
    timestamp : int
        UTC timestamp of when the ban happened.
    nickname : str
        The banned nickname.
    duration : int
        The duration of the ban in minutes.
    author : str
        The nickname of the author of the ban.
        None if the author of the ban is hidden.
    until : int
        UTC timestamp of when the ban ends.
    room : int
        The ID of the room where the ban happened.
    comment : str
        The comment of the ban written by the author of the ban.
        None if there is not comment.
    """
    type = 'ub'

    timestamp = Field(int, 'ts')
    author = Field(str, 'modNick')
    nickname = Field(str, 'bannedNick')
    duration = Field(int, 'minutes')
    until = Field(int, 'until')
    comment = Field(str, 'comment')
    room = Field(int, 'r')


class HasOlderMessages:
    """Event that determines if the room has more messages to be displayed.

    This event is received when messages are fetched from a room.

    Attributes
    ----------
    room : int
        The room.
    value : bool
        Whether there are more messages available to be fetched or not.
    """
    type = 'hoe'

    room = Field(int, 'r')
    value = Field(bool, 'hasOlderEvents')


class Random:
    """Empty random event.

    Used for nothing(yet?).
    """
    type = 'rnd'


class Action:
    """Generic event that determines an action that must
    be performed by the user.

    Generally used for defining the minimal age for seeing a chat room.

    Attributes
    ----------
    content : str
        The content of the action.
    type : str
        The type of the action
    data : dict
        A dict containing generic values for the action.
    """
    title = Field(str, 'title')
    type = Field(str, 'type')
    data = Field(dict, 'data')


