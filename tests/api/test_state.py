from chatovod.api.states import State


class Language(State):
    default = "pt"
    english = "en"

    def _default(self):
        return self.default


class UserType(State):
    ghost = None
    user = 0
    admin = 1


class RoomType(State):
    empty = None
    public = 0
    private = 1


class TestState:
    def test_create_from(self):
        my_language = "en"

        assert Language.create_from(my_language) == Language.english

    def test_create_from_returns_default_when_state_does_not_contain_none(self):
        my_language = Language.create_from(None)

        assert my_language is not None
        assert my_language == Language.default

    def test_create_from_does_not_return_none_when_state_contains_none(self):
        my_room = RoomType.create_from(None)

        assert my_room is not None
        assert my_room == RoomType.empty

    def test_state_can_be_extended(self):
        assert issubclass(Language, State)

    def test_state_returns_instance(self):
        my_language = Language("en")

        assert isinstance(my_language, State)
        assert isinstance(my_language, Language)

    def test_state_property_is_state_instance(self):
        assert isinstance(UserType.admin, UserType)
        assert isinstance(UserType.admin, State)
        assert not isinstance(UserType.admin, int)

    def test_number_comparison(self):
        user_type = UserType(1)

        assert user_type == UserType.admin
        assert user_type == 1
        assert UserType.admin == 1

    def test_number_inequality(self):
        assert UserType.admin != 0
        assert not (UserType.admin != 1)

    def test_string_comparisony(self):
        my_language = Language("en")

        assert my_language == Language.english
        assert my_language == "en"
        assert Language.english == "en"

    def test_string_inequality(self):
        assert Language.english != "ru"
        assert not (Language.english != "en")

    def test_state_compares_state(self):
        assert UserType.admin == UserType.admin
        assert UserType.user == UserType.user
        assert UserType.user != UserType.admin
        assert UserType.user != RoomType.public
