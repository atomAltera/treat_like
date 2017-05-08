from .exceptions import ProcessException
from .treat import Treat


class Template:
    def __init__(self):
        self._pipe = []

    def copy(self):
        new_template = Template()
        new_template._pipe = [i for i in self._pipe]

        return new_template

    def by(self, template):
        self._pipe.extend(template._pipe)

    def like(self, *converters, message=None):
        for converter in converters:
            self._pipe.append(('like', (converter, message)))

        return self

    def must_be(self, *validators, message=None):
        for validator in validators:
            self._pipe.append(('must_be', (validator, message)))

        return self

    def each(self):
        self._pipe.append(('each', ()))

        return self

    def all(self):
        self._pipe.append(('all', ()))

        return self

    def apply_to(self, value, name=None):
        t = Treat(value, name)

        try:
            for method_name, args in self._pipe:
                method = getattr(t, method_name)
                t = method(*args)

            return True, t.results(), None
        except ProcessException as ex:
            return False, value, ex
