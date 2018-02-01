
ADAPTERS_MAP = {}

def adapter(func):
    func_name = func.__name__
    if not func_name.startswith('adapt_'):
        raise ValueError('{} must start with "adapt_"', func_name)

    event = func_name[6:]

    if not event:
        raise ValueError('Event type cannot be empty')

    ADAPTERS_MAP[event] = func

    return func

@adapter
def adapt_so(data):
    return {
        't': 'set_option',
        'option': data.get('k'),
        'value': data.get('v'),
    }

@adapter
def adapt_cls(data):
    return {
        't': 'cls',
        'email': data.get('accountName'),
        'account_type': data.get('accountType'),
        'user_group': data.get('accountGroup'),
        'last_nickname': data.get('lastNick'),
    }

@adapter
def adapt_sl(data):
    return {
        't': 'chat_emojis',
        'emojis': data.get('smileys'),
        'groups': data.get('cats'),
        'default_path': data.get('dp'),
        'custom_path': data.get('p'),
    }

@adapter
def adapt_error(data):
    return {
        't': 'error',
        'description': data.get('error'),
        'group': data.get('et'),
        'category': data.get('est'),
        'room_id': data.get('r'),
        'timestamp': data.get('ts'),
    }

@adapter
def adapt_mi(data):
    return {
        't': 'moderate_info',

        'message_ip': data.get('messageIp'),
        'last_ip': data.get('lastIp'),

        'location': data.get('lastIpGeo'),
        'user_agent': data.get('lastUserAgent'),

        'nick_id': data.get('nickId'),
        'account_id': data.get('accountId'),

        'last_login': data.get('lastEnterToChat'),
        'nickname_created_at': data.get('createdInChat'),
        'registered_timestamp': data.get('created'),

        'account_service_name': data.get('accountType'),
        'account_service_domain': data.get('accountTypeTitle'),

        'banned': data.get('banned', False),
    }

@adapter
def adapt_m(data):
    return {
        't': 'message',
        'timestamp': data['ts'],
        'author': data['f'],
        'content': data['m'],
        'room_id': data['r'],
        'actions': data.get('actions'),
    }

@adapter
def adapt_md(data):
    return {
        't': 'message_delete',
        'messages': data['ts'],
        'room_id': data['r'],
    }

@adapter
def adapt_pmr(data):
    return {
        't': 'message_read',
        'from_ts': data.get('fromTime'),
        'until_ts': data.get('toTime'),
    }

@adapter
def adapt_ru(data):
    return {
        't': 'room_update',
        'name': data.get('title'),
        'can_be_closed': data.get('closeable'),
        'display_user_flow': data.get('showEnterLeave'),
    }

@adapter
def adapt_ro(data):
    return {
        't': 'room_open',
        'type': data.get('channelType'),
        'set_focus': data.get('active'),
        'name': data.get('title'),
        'can_be_closed': data.get('closeable'),
        'display_user_flow': data.get('showEnterLeave'),
    }

@adapter
def adapt_rc(data):
    return {
        't': 'room_close',
        'window_id': data.get('iwid', 0),
    }

@adapter
def adapt_tc(data):
    return {
        't': 'room_clear_messages',
        'room_id': data['id'],
        'type': data['type'],
    }

@adapter
def adapt_hoe(data):
    return {
        't': 'has_older_events',
        'value': data['hasOlderEvents']
    }

@adapter
def adapt_ul(data):
    return {
        't': 'user_leave',
        'nickname': data['nick']
    }


"""
class UserEnterChat(EventAdapter):
type = 'ue'

class UserEnterRoom(EventAdapter):
type = 'uer'

class UserLeaveRoom(EventAdapter):
type = 'ulr'
"""
