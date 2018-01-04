from enum import Enum


class AccountService(Enum):
    """Service where the account is registered."""
    guest = 'guest'
    chatovod = 'ch'
    facebook = 'fb'
    google = 'go'
    yandex = 'ya'
    vk = 'vk'
    mail_ru = 'ma'
    ok_ru = 'od'


class Language(Enum):
    """The language used in the interface of the chat service.
    It also determines the language of the messages returned by the API.
    i.e.: error messages and ban list text."""
    default = 'None'
    azeri = 'az'
    dutch = 'nl'
    english = 'en'
    russian = 'ru'
    spanish = 'es'
    tatar = 'tt'
    turkish = 'tr'


class RoomType(Enum):
    """The type of the room."""
    public = 0
    private = 1
    private_mask = 2


class Gender(Enum):
    """The gender of the user."""
    none = 0
    female = 1
    male = 2


class Group(Enum):
    """The group which the user belongs to."""
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'


class Status(Enum):
    """The current availability of the user."""
    online = 'online'
    away = 'away'
    # dnd stands for "do not disturb"
    busy = 'dnd'
    invisible = 'invis'
