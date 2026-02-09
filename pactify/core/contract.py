from pactify.core.field import Field
from pactify.core.schema import ContractSchema


class ContractMeta(type):
    """
    Metaclass that collects Field definitions from a Contract.
    """

    def __new__(cls, name, bases, attrs):
        fields = {}

        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
                attrs.pop(key)

        attrs["_fields"] = fields
        return super().__new__(cls, name, bases, attrs)


class Contract(metaclass=ContractMeta):
    """
    Base class for all API contracts.
    """

    __version__ = None

    @classmethod
    def schema(cls) -> ContractSchema:
        return ContractSchema(
            name=cls.__name__,
            version=cls.__version__,
            fields=cls._fields,
        )
