import abc

from collections import Iterable


class Field:

    __slots__ = ('name', 'model', 'key_in_raw', 'default', 'required')

    def __init__(self, key_in_raw, *, name=None, default=None, required=False):
        self.name = name
        self.key_in_raw = key_in_raw
        self.default = default
        self.required = required

    def extract_from_raw(self, raw):
        try:
            return raw[self.key_in_raw]
        except KeyError:
            if self.required:
                raise ValueError('Field {!r} could not be found in raw data'.format(self))

            return self.default

    def try_transform(self, original_value):
        try:
            converted_value = original_value
            return converted_value
        except Exception as e:
            raise e

    @property
    def name_in_model(self):
        return Field.name_to_private_name(self.name)

    @classmethod
    def name_to_private_name(cls, name):
        return '_' + name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return getattr(instance, self.name_in_model, self.default)

    def __set__(self, instance, value):
        setattr(instance,
                self.name_in_model,
                self.try_transform(value))

    def __delete__(self, instance):
        raise AttributeError('Attribute deletion is not allowed')


class EventAdapterBase(abc.ABCMeta):

    def __new__(cls, name, bases, attrs, **kwargs):
        parents = [base for base in bases if isinstance(base, EventAdapterBase)]
        super_new = super().__new__

        # Excludes EventAdapter and other direct subclasses of EventAdapterBase
        # from initialization.
        # EventAdapterBase -> EventAdapter -> SomeEvent
        if not parents:
            return super_new(cls, name, bases, attrs, **kwargs)

        # The instance of the model is needed for easier handling of the code
        new_class = super_new(cls, name, bases, attrs, **kwargs)

        # Assign fields from parents.
        # Fields consists of local and parent fields.
        fields = {
            name: field
            for parent in parents
            if hasattr(parent, '_fields') and isinstance(parent._fields, Iterable)
            for name, field in parent._fields.items()
        }

        for name, attr in attrs.items():
            if isinstance(attr, Field) and name != 'type':
                field = attr
                fields[name] = field
                field.name = name
                field.model = new_class

        new_class._adapts_keys = set([field.key_in_raw for field in fields.values()])
        new_class._fields = fields

        return new_class


class EventAdapter(metaclass=EventAdapterBase):

    _key_for_event_type = 't'

    def __init__(self, data, **kwargs):
        self.state = kwargs.get('state')
        self._extra_data = self.find_extra_data(data)

        for field in self._fields.values():
            setattr(
                self,
                field.name,
                field.extract_from_raw(data))

    @classmethod
    def extract_event_type_from_raw(cls, raw):
        return raw.get(cls._key_for_event_type)

    @classmethod
    def create(cls, data, **kwargs):
        """Create a new instance of a model using a raw data."""
        instance = cls(data, **kwargs)
        return instance

    @classmethod
    def create_as_dict(cls, raw):
        return {
            name: field.try_transform(raw)
            for name, field in cls._fields.items()
        }

    @classmethod
    def find_extra_data(cls, raw):
        """Search and return fields not defined in the Model definition."""
        return {
            name: value
            for name, value in raw.items()
            if name not in cls._adapts_keys
        }

    @property
    def _fields(self):
        return self.__class__._fields

    @classmethod
    def _local_fields(cls):
        return {
            name: field
            for name, field in cls._fields.items()
            if field.model is cls
        }
