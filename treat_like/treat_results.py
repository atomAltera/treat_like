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

        self._errors = None
        self._has_errors = None

    def put(self, field_name, success, result, ex):
        self._values[field_name] = (success, result, ex)

        self._errors = None
        self._has_errors = None
        return self

    @property
    def has_errors(self):
        if self._has_errors is None:
            self._has_errors = not all(map(lambda r: r[0], self._values.values()))

        return self._has_errors

    @property
    def errors(self):
        if self._errors is None:
            self._errors = dict(map(lambda v: (v[2].name, v[2].message), filter(lambda v: not v[0], self._values.values())))

        return self._errors

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
