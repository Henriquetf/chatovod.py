
class Unset:
    """Placeholder for values where None is allowed."""

    def __nonzero__(self):
        return False

    def __bool__(self):
        return False


UNSET = Unset()


class Field:
    """

    name becomes _name
    """

    __slots__ = ('name', 'field_type', 'converter', 'raw_key_name', 'default', 'required')

    def __init__(self, field_type, raw_key_name, default=None, required=False):
        self.field_type = field_type
        self.raw_key_name = raw_key_name
        self.default = default
        self.required = required

    @property
    def attr_name_in_model(self):
        return '_' + self.name

    def extract_from_raw(self, raw):
        try:
            return raw[self.raw_key_name]
        except KeyError:
            if self.required:
                raise ValueError('Field {!r} could not be found in raw data'.format(self))

            return self.default

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return getattr(instance, self.attr_name_in_model, self.default)

    def __set__(self, instance, value):
        setattr(instance, self.attr_name_in_model, self.field_type(value))

    def __delete__(self, instance, owner):
        raise AttributeError('Attribute deletion is not allowed')


class ExtraField(Field):
    """A field which does not contain a key in the event object,
    thus cannot be extracted directly.
    The event object is passed to the converter function."""

    __slots__ = ()

    def __init__(self, converter):
        self.converter = converter

    def extract_from_raw(self, raw):
        return self.converter(raw)


class DefaultField(Field):

    __slots__ = ()

    def __init__(self, default, raw_key_name=None):
        super().__init__(
            field_type=type(default), raw_key_name=None, default=default, required=False)

    def extract_from_raw(self, raw):
        return self.default
