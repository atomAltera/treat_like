from django.db.models import Q


class MetaValidator(type):
    pass


class Validator(metaclass=MetaValidator):
    def need_to_validate(self, value):
        return value is not None

    def validate(self, value):
        return False

    def get_message(self):
        return None


class provided(Validator):
    def need_to_validate(self, value):
        return True

    def validate(self, value):
        return bool(value)

    def get_message(self):
        return 'this field is required'


class longer_then(Validator):
    def __init__(self, length):
        super().__init__()
        self._length = length

    def validate(self, value):
        return len(value) > self._length

    def get_message(self):
        return 'must be longer then {length}'.format(length=self._length)


class shorter_then(Validator):
    def __init__(self, length):
        super().__init__()
        self._length = length

    def validate(self, value):
        return len(value) < self._length

    def get_message(self):
        return 'must be shorter then {length}'.format(length=self._length)


class exact(Validator):
    def __init__(self, length):
        super().__init__()
        self._length = length

    def validate(self, value):
        return len(value) == self._length

    def get_message(self):
        return 'must be exact {length} in length'.format(length=self._length)


class gt(Validator):
    def __init__(self, x):
        super().__init__()
        self._x = x

    def validate(self, value):
        return value > self._x

    def get_message(self):
        return 'must be greater then {x}'.format(x=self._x)


class lt(Validator):
    def __init__(self, x):
        super().__init__()
        self._x = x

    def validate(self, value):
        return value < self._x

    def get_message(self):
        return 'must be less then {x}'.format(x=self._x)


class equal_to(Validator):
    def __init__(self, another_value):
        super().__init__()
        self._another_value = another_value

    def validate(self, value):
        return value == self._another_value

    def get_message(self):
        return 'is not equal to specified value'


class unique_in(Validator):
    def __init__(self, model_class, field, ignoring_id=None):
        super().__init__()
        self._model_class = model_class
        self._field = field
        self._ignoring_id = ignoring_id

    def validate(self, value):
        try:
            if self._ignoring_id is not None:
                self._model_class.objects.get(Q(**{self._field: value}), ~Q(id=self._ignoring_id))
            else:
                self._model_class.objects.get(Q(**{self._field: value}))

            return False
        except self._model_class.DoesNotExist:
            return True

    def get_message(self):
        return 'must be unique in {model}.{field}'.format(model=self._model_class.__name__, field=self._field)


class secure_for_password(Validator):
    def __init__(self):
        super().__init__()

    def validate(self, value):
        return len(value) >= 8

    def get_message(self):
        return 'is too shot to be a password'
