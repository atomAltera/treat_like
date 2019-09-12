from treat_like import ProcessException


class TreatResults:
    class _CorrectnessTracker:
        def __init__(self, errors, track_correct):
            self._errors = errors
            self._track_correct = track_correct

        def __getattr__(self, item):
            if self._track_correct:
                return item not in self._errors
            else:
                return item in self._errors

    class _ErrorMessageTracker:
        def __init__(self, errors):
            self._errors = errors

        def __getattr__(self, item):
            return self._errors.get(item, '')

    def __init__(self):
        self._values = dict()

        self._general_errors = set()

    def put(self, field_name, success, result, ex):
        self._values[field_name] = (success, result, ex)

        return self

    def put_error(self, field_name, message):
        if field_name in self._values:
            existing = self._values[field_name]
            value = existing[1]
        else:
            value = None

        return self.put(field_name, False, value, ProcessException(field_name, message))

    def put_general_error(self, message):
        self._general_errors.add(message)

    @property
    def has_errors(self):
        has_field_errors = not all(map(lambda r: r[0], self._values.values()))
        has_general_errors = self._general_errors

        return has_field_errors or has_general_errors

    @property
    def errors(self):
        return dict(map(lambda v: (v[2].name, v[2].message), filter(lambda v: not v[0], self._values.values())))

    @property
    def general_errors(self):
        return list(self._general_errors)

    @property
    def has_error_in(self):
        return self._CorrectnessTracker(self.errors, False)

    @property
    def has_correct(self):
        return self._CorrectnessTracker(self.errors, True)

    @property
    def error_message_of(self):
        return self._ErrorMessageTracker(self.errors)

    def __getattr__(self, item):
        if item in self._values:
            return self._values.get(item, (False, None, None))[1]
