import abc


class Field:
    """
    """

    __slots__ = ('name', 'model', 'transform', 'key_in_raw', 'default', 'required')

    def __init__(self, key_in_raw, *, default=None, transform=None, required=False):
        self.name = None
        self.key_in_raw = key_in_raw
        self.default = default
        self.required = required
        self.transform = transform

    def extract_from_raw(self, raw):
        try:
            return raw[self.key_in_raw]
        except KeyError:
            if self.required:
                raise ValueError('Field {!r} could not be found in raw data'.format(self))

            return self.default

    def try_transform(self, raw):
        # TODO: real implementation
        raw_value = self.extract_from_raw(raw)
        value = raw_value

        return value

    @property
    def name_in_model(self):
        return '_' + self.name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return getattr(instance, self.name_in_model, self.default)

    def __set__(self, instance, value):
        setattr(instance, self.name_in_model, self.try_transform(value))

    def __delete__(self, instance):
        raise AttributeError('Attribute deletion is not allowed')


class ModelBase(abc.ABCMeta):

    def __new__(cls, name, bases, attrs, **kwargs):
        parents = [base for base in bases if isinstance(base, ModelBase)]
        super_new = super().__new__

        # Excludes Model class and othzer base classes from initialization
        if not parents:
            return super_new(cls, name, bases, attrs, **kwargs)

        # Split attrs in two dicts, one containing Field attributes and
        # another without them
        local_fields = {}
        new_attrs = {}

        # Remove Field attributes from `new_attrs` and
        # push them to `local_fields`
        for field_name, field_attr in attrs.items():
            if isinstance(field_attr, Field):
                local_fields[field_name] = field_attr
            else:
                new_attrs[field_name] = field_attr

        # The built model class is needed for easier handling of the code
        new_class = super_new(cls, name, bases, new_attrs, **kwargs)
        new_class._local_fields = local_fields
        new_class._fields = {}

        for field_name, field in local_fields.items():
            field.name = field_name
            field.model = new_class

        # Parent fields are loaded from the upper to the lowest class
        for base in reversed(new_class.mro()):
            if (isinstance(base, ModelBase) and hasattr(base, '_local_fields')):
                new_class._fields.update(base._local_fields)

        return new_class


class Model(metaclass=ModelBase):

    @classmethod
    def build_as_dict(cls, raw):
        return {
            name: field.try_transform(raw)
            for name, field in cls._fields.items()
        }

    @property
    def _fields(self):
        return self.__class__._fields
