from chatovod.api.states import AccountService, RoomType, Group, Status, Gender
from chatovod.structures.base import Model, Field


class ReceiveEvent:

    EVENTS_MAP = {}

    def __init__(self, event_type):
        self.event_type = event_type

    def __call__(self, model):
        # Register event model
        ReceiveEvent.EVENTS_MAP[self.event_type] = model
        return model


def model_from_event(event):
    event_type = extract_raw_event_type(event)
    return ReceiveEvent.EVENTS_MAP.get(event_type)


def extract_raw_event_type(raw_event):
    return raw_event.get('t')


@ReceiveEvent('tal')
class TryAutoLogin(Model):
    pass


@ReceiveEvent('so')
class SO(Model):
    pass


@ReceiveEvent('cls')
class CLS(Model):
    pass


@ReceiveEvent('cpo')
class CPO(Model):
    pass


@ReceiveEvent('ta')
class TabActivate(Model):
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
    room = Field(int, 'id')
    window = Field(int, 'iwid', default=None)
    scope = Field(str, 'type')


@ReceiveEvent('sl')
class EmojiList(Model):
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
    emojis = Field(list, 'smileys')
    groups = Field(list, 'cats')
    default_path = Field(str, 'dp')
    custom_path = Field(str, 'p', default=None)


@ReceiveEvent('error')
class Error(Model):
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
    description = Field(str, 'error')
    group = Field(str, 'et')
    category = Field(str, 'est')


@ReceiveEvent('mi')
class ModerateInfo(Model):
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
    message_ip = Field('messageIp', default=None)

    ip = Field('lastIp', default=None)
    location = Field(str, 'lastIpGeo', default=None)

    user_agent = Field(str, 'lastUserAgent', default=None)

    nick_id = Field(int, 'nickId', default=None)
    account_id = Field(int, 'accountId', default=None)

    last_login = Field(int, 'lastEnterToChat', default=None)

    nickname_created_at = Field(int, 'createdInChat', default=None)
    registered_timestamp = Field(int, 'created', default=None)

    account_service_name = Field(AccountService, 'accountType', default=None)
    account_service_domain = Field(str, 'accountTypeTitle', default=None)

    banned = Field(bool, 'banned', default=False)


@ReceiveEvent('urc')
class RoomCount(Model):
    """Event that determines the amount of public rooms in the chat.

    Attributes
    ----------
    count : int
        The amount of public rooms in the chat.
    """
    count = Field(int, 'count')


@ReceiveEvent('m')
class Message(Model):
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
    id = Field(int, 'ts')
    room = Field(int, 'r')
    content = Field(str, 'm')
    author = Field(str, 'f')

    old = Field(bool, 's', default=False)
    fetched = Field(bool, 'pp', default=False)

    to = Field(list, 'to')
    cmd_me = Field(bool, 'nh', default=False)

    # Private message
    seen = Field(lambda v: not v, 'u', default=True)
    actions = Field('actions')


@ReceiveEvent('md')
class MessageDelete(Model):
    """Represents a message delete event.

    Attributes
    ----------
    room : int
        The ID of the room where the messages were deleted.
    messages : list
        A list of int timestamps of all deleted messages.
    """
    room = Field(int, 'r')
    messages = Field(list, 'ts')


@ReceiveEvent('pmr')
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
    room = Field(int, 'r')
    since = Field(int, 'fromTime')
    until = Field(int, 'toTime')


@ReceiveEvent('ru')
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
    id = Field(int, 'r')
    name = Field(str, 'title')
    can_close = Field(bool, 'closeable')
    display_user_flow = Field(bool, 'showEnterLeave')


@ReceiveEvent('ro')
class RoomOpen(RoomUpdate):
    """Represents a room open event.

    Attributes
    ----------
    room_type : RoomType
        The type of the room.
    set_focus : bool
        Determines if the focus should be changed to the opened room.
    """

    room_type = Field(RoomType, 'channelType')
    set_focus = Field(bool, 'active', False)


@ReceiveEvent('rc')
class RoomClose(Model):
    """Represents a room close event.

    id : int
        The ID of the room to be closed.
    window : str
        The ID of the window that closed the room.
    """
    id = Field(int, 'r')
    iwid = Field(int, 'iwid', default=0)


@ReceiveEvent('tc')
class RoomClear(Model):
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
    room = Field(int, 'id')
    scope = Field(str, 'type')


@ReceiveEvent('uu')
class UserUpdate:
    """Represents a user update event.

    Attributes
    ----------
    nickname : str
        The nickname of the user.
    id : int
        The ID of the user.
        None if the user is not registered.
    avatar_url : str
        URL of the avatar. Does not contain the transfer protocol.
        None if the user does not have an avatar or not logged into an account.
    group : str
        The group of the user: `user`, `moderator` or `admin`.
        None if `user`.
    status : str
        The current status of the user: `online`, `dnd` or `away`.
        None if `online`.
    gender : int
        The ID of the gender of the user: `none`, `female` or `male`.
        `none`: 0
        `female`: 1
        `male`: 2
        None if `none`.
    nickname_colour : str
        Hex colour of the nickname of the user. Does not start with `0x`.
    message_colour : str
        Hex colour of the messages sent by the user. Does not start with `0x`.
        None if there's no custom colour.
    vip : bool
        Determines if the user is VIP.
    bold_nickname : bool
        Determines if the user has bold nickname.
    bold_message : bool
        Determines if the user has bold message text.
    """
    nickname = Field(str, 'nick')

    id = Field(int, 'id')
    avatar_url = Field(str, 'as')

    group = Field(Group, 'g')
    status = Field(Status, 's')
    gender = Field(Gender, 'sx')

    nickname_colour = Field(Colour, 'c')
    message_colour = Field(Colour, 'tc')

    vip = Field(bool, 'vip', default=False)
    bold_nickname = Field(bool, 'b', default=False)
    bold_message = Field(bool, 'bt', default=False)


@ReceiveEvent('ue')
class UserEnterChat(UserUpdate):
    """Represents a user enter chat event."""


@ReceiveEvent('ul')
class UserLeaveChat(UserUpdate):
    """Represents a user leave chat event.

    Attributes
    ----------
    nickname : str
        The nickname of the user who left the chat.
    """

    nickname = Field(str, 'nick')


@ReceiveEvent('uer')
class UserEnterRoom(MessageBase):
    """Represents a user enter room event."""


@ReceiveEvent('ulr')
class UserLeaveRoom(MessageBase):
    """Represents a user leave room event."""


@ReceiveEvent('ub')
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
    timestamp = Field(int, 'ts')
    author = Field(str, 'modNick')
    nickname = Field(str, 'bannedNick')
    duration = Field(int, 'minutes')
    until = Field(int, 'until')
    comment = Field(str, 'comment')
    room = Field(int, 'r')


@ReceiveEvent('hoe')
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
    room = Field(int, 'r')
    value = Field(bool, 'hasOlderEvents')


@ReceiveEvent('rnd')
class Random:
    """Empty random event.

    Used for nothing(yet?).
    """


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


class BanList:

    data_type = Field(str, 't')
    content = Field(str, 'html')
