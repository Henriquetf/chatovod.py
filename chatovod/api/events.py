from .event_adapter import EventAdapter, Field


class TryAutoLogin(EventAdapter):
    type = 'tal'


class SO(EventAdapter):
    type = 'so'


class CLS(EventAdapter):
    type = 'cls'


class CPO(EventAdapter):
    type = 'cpo'


class TabActivate(EventAdapter):
    type = 'ta'

    room_id = Field('id')
    window = Field('iwid')
    scope = Field('type')


class EmojiList(EventAdapter):
    type = 'sl'

    emojis = Field('smileys')
    groups = Field('cats')
    default_path = Field('dp')
    custom_path = Field('p')


class Error(EventAdapter):
    type = 'error'

    description = Field('error')
    group = Field('et')
    category = Field('est')


class ModerateInfo(EventAdapter):
    type = 'mi'

    message_ip = Field('messageIp')
    last_ip = Field('lastIp')

    location = Field('lastIpGeo')
    user_agent = Field('lastUserAgent')

    nick_id = Field('nickId')
    account_id = Field('accountId')

    last_login = Field('lastEnterToChat')
    nickname_created_at = Field('createdInChat')
    registered_timestamp = Field('created')

    account_service_name = Field('accountType')
    account_service_domain = Field('accountTypeTitle')

    banned = Field('banned', default=False)


class RoomCount(EventAdapter):
    type = 'urc'

    count = Field('count')


class WithRoom(EventAdapter):
    room_id = Field('r')


class MessageBase(WithRoom):
    ...


class Message(MessageBase):
    type = 'm'

    actions = Field('actions')


class MessageDelete(WithRoom):
    type = 'md'

    messages = Field('ts')


class MessageRead(WithRoom):
    type = 'pmr'

    since = Field('fromTime')
    until = Field('toTime')


class RoomUpdate(WithRoom):
    type = 'ru'

    name = Field('title')
    can_be_closed = Field('closeable', default=False)
    display_user_flow = Field('showEnterLeave', default=False)


class RoomOpen(RoomUpdate):
    type = 'ro'

    room_type = Field('channelType')
    set_focus = Field('active', default=False)


class RoomClose(WithRoom):
    type = 'rc'

    window = Field('iwid', default=0)


class RoomClear(EventAdapter):
    type = 'tc'

    room_id = Field('id')
    scope = Field('type')


class UserEnterChat(EventAdapter):
    type = 'ue'


class UserLeaveChat(EventAdapter):
    type = 'ul'

    nickname = Field('nick')


class UserEnterRoom(EventAdapter):
    type = 'uer'


class UserLeaveRoom(EventAdapter):
    type = 'ulr'


class UserBan(WithRoom):
    type = 'ub'

    timestamp = Field('ts')
    author = Field('modNick')
    nickname = Field('bannedNick')
    duration = Field('minutes')
    until = Field('until')
    comment = Field('comment')


class HasOlderMessages(WithRoom):
    type = 'hoe'

    value = Field('hasOlderEvents')


class Random(EventAdapter):
    type = 'rnd'


class Action(EventAdapter):
    title = Field('title')
    type = Field('type')
    data = Field('data')
