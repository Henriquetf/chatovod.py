from enum import Enum


class State(Enum):
    @classmethod
    def create_from(cls, value):
        try:
            state = cls(value)
            return state
        except ValueError as e:
            if value is None:
                return cls._default(cls)

            raise e

    def __eq__(self, value):
        if isinstance(value, State):
            return super().__eq__(value)

        return value == self.value

    def __ne__(self, value):
        neq = self.__eq__(value)

        if neq is NotImplemented:
            return NotImplemented

        return not neq


class AccountService(State):
    """Service where the account is registered."""

    guest = None
    chatovod = "ch"
    facebook = "fb"
    google = "go"
    yandex = "ya"
    vk = "vk"
    mail_ru = "ma"
    ok_ru = "od"

    def _default(self):
        return AccountService.guest


class Language(State):
    """The language used in the interface of the chat service.
    It also determines the language of the messages returned by the API.
    i.e.: error messages and ban list text."""

    default = None
    azeri = "az"
    dutch = "nl"
    english = "en"
    russian = "ru"
    spanish = "es"
    tatar = "tt"
    turkish = "tr"

    def _default(self):
        return Language.default


class RoomType(State):
    """The type of the room."""

    public = 0
    private = 1
    _private = 2

    def _default(self):
        return RoomType.public


class Gender(State):
    """The gender of the user."""

    none = None
    female = 1
    male = 2

    def _default(self):
        return Gender.none


class Group(State):
    """The group which the user belongs to."""

    user = None
    moderator = "moderator"
    admin = "admin"

    def _default(self):
        return Group.user


class Status(State):
    """The current availability of the user."""

    online = None
    away = "away"
    dnd = "dnd"
    invisible = "invis"

    def _default(self):
        return Status.online
