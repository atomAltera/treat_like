from .template import Template
from .treat_results import TreatResults


class Form:
    def __init__(self):
        self._fields = dict()
        self._locked = False

    def copy(self):
        new_form = Form()
        new_form._fields = {f: (k, t.copy()) for f, (k, t) in self._fields.items()}

        return new_form

    def treat(self, field_name, key_name=None):
        key_name = key_name or field_name

        if field_name in self._fields:
            t = self._fields[field_name][1]
            self._fields[field_name] = (key_name, t)

        else:
            t = Template()
            self._fields[field_name] = (key_name, t)

        return t

    def without(self, *field_names):
        self._fields = {field_name: self._fields[field_name] for field_name in self._fields if field_name not in field_names}

        return self

    def only(self, *field_names):
        self._fields = {field_name: self._fields[field_name] for field_name in self._fields if field_name in field_names}

        return self

    def apply_to(self, dictionary):
        treat_results = TreatResults()

        for field_name, (key_name, template) in self._fields.items():
            value = dictionary.get(key_name)

            success, result, ex = template.apply_to(value, name=key_name)
            treat_results.put(field_name, success, result, ex)

        return treat_results

    def try_fetch(self, field_name, dictionary):
        key_name, template = self._fields[field_name]
        value = dictionary.get(key_name)

        return template.apply_to(value, name=key_name)

    def fetch(self, field_name, dictionary):
        success, result, ex = self.try_fetch(field_name, dictionary)

        if ex:
            raise ex

        return result
