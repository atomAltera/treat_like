from .converters import MetaConverter, Converter
from .exceptions import FormatException, ValidationException
from .validators import MetaValidator, Validator


class Treat:
    def __init__(self, value, name=None):
        self._value = value
        self._name = name

        self._collection_mode = False

    def _like(self, value, converter, message=None):
        if isinstance(converter, MetaConverter):
            converter = converter()

        if isinstance(converter, Converter):
            message = message or converter.get_message()
            converter = converter.convert if converter.need_to_convert(value) else lambda v: v
        else:
            message = message
            converter = converter

        try:
            value = converter(value)
        except Exception as ex:
            raise FormatException(self._name, message)

        return value

    def _must_be(self, value, validator, message=None):
        if isinstance(validator, MetaValidator):
            validator = validator()

        if isinstance(validator, Validator):
            message = message or validator.get_message()
            validator = validator.validate if validator.need_to_validate(value) else lambda v: True
        else:
            message = message
            validator = validator

        if not validator(value):
            raise ValidationException(self._name, message)

    def like(self, converter, message=None):
        if self._collection_mode:
            self._value = tuple(self._like(value=v, converter=converter, message=message) for v in self._value)
        else:
            self._value = self._like(value=self._value, converter=converter, message=message)

        return self

    def must_be(self, validator, message=None):
        if self._collection_mode:
            for v in self._value:
                self._must_be(value=v, validator=validator, message=message)
        else:
            self._must_be(value=self._value, validator=validator, message=message)

        return self

    def each(self):
        self._collection_mode = True
        return self

    def all(self):
        self._collection_mode = False
        return self

    def results(self):
        return self._value
