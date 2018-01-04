import abc

from chatovod.structures.field import Field


class ModelBase(abc.ABCMeta):

    def __new__(cls, name, bases, attrs, **kwargs):
        parents = [base for base in bases if isinstance(base, ModelBase)]
        super_new = super().__new__

        # Excludes Model class and other base classes from initialization
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

    @staticmethod
    def build_from_raw(model, client, raw):
        new_model = model()
        fields = model._fields

        for field in fields.values():
            field_result = field.generate_from_raw(raw)
            setattr(new_model, field.name, field_result)

        return new_model

    @property
    def _fields(self):
        return self.__class__._fields
