from pathlib import Path
from urllib.parse import urlparse

from chatovod.api.states import Gender, Group, Status


class AvatarInfo:

    __slots__ = ('type', 'id', 'ts')

    def __init__(self, avatar_url):
        """A function to extract informations from a user avatar URL.

        Example: //a.chatovod.com/n/2000000/a?1470000000

        :param avatar_url: the URL of the avatar.
        """

        # /n|a/000000/X?00000000
        parse_result = urlparse(avatar_url)
        url_path = Path(parse_result.path)

        # url_path.parts returns the split path: ('/', 'n', '3000000', 'a')
        self.type = url_path.parts[1]
        self.user_id = url_path.parts[2]
        self.timestamp = parse_result.query

    @property
    def url(self):
        return


class User:

    __slots__ = ('nickname', 'id', 'gender', 'group', 'status',
                 'nickname_colour', 'message_colour', 'vip',
                 'bold_nickname', 'bold_message')

    def __init__(self, *, event):
        self.nickname = event['nick']
        self.id = str(event.get('id'))

        self.gender = Gender(event.get('sx'))
        self.group = Group(event.get('g'))
        self.status = Status(event.get('s'))

        self.nickname_colour = event.get('c')
        self.message_colour = event.get('tc')

        self.vip = event.get('vip', False)
        self.bold_nickname = event.get('b', False)
        self.bold_message = event.get('tb', False)
