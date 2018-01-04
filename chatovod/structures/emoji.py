from collections import OrderedDict


class Emoji:
    """Represents an emoji object.

    Attributes
    ----------
    client : Client
        The client that instantiated the object.
    group : EmojiGroup
        The group of the emoji.
    width : int
        The width in pixels of the emoji.
    height : int
        The height in pixels of the emoji.
    placeholder : str
        The text that is substituted into the emoji picture.
    default : bool
        Whether the emoji is a default emoji provided by Chatovod or not.
    path : str
        The URL path of the emoji.
    vip : bool
        Determines if an emoji can be used only by VIP users.
    """

    def __init__(self, *, event):
        self.width = event.get('w')
        self.height = event.get('h')
        self.placeholder = event.get('c')
        self.is_default = event.get('default', True)
        self.path = event.get('i')
        self.vip = event.get('p', False)
        self.group_id = event.get('s')

    @property
    def url(self):
        if self.default:
            return self.chat.emoji_base_path + self.path
        else:
            return self.chat.custom_emoji_base_path + self.path

    @property
    def chat(self):
        return self.client.chat

    @property
    def group(self):
        return self.chat.groups.get(self.group_id)


class EmojiGroup:
    """Represents a group of emojis.

    Attributes
    ----------
    client : Client
        The client that instantiated the object.
    id : int
        The ID of the emoji group.
    name : str
        The name of the group.
    emojis : OrderedDict
        A dictionary with all emojis in the group.
    """

    def __init__(self, client, event):
        self.client = client
        self.id = event.pop('id')
        self.name = event.pop('t')
        self.emojis = OrderedDict()

    def _add_emoji(self, emoji):
        self.emojis[emoji.placeholder] = emoji
