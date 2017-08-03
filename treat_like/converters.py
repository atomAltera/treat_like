from datetime import datetime

from django.contrib.gis.geos import GEOSGeometry

from .validators import provided


class MetaConverter(type):
    pass


class Converter(metaclass=MetaConverter):
    def need_to_convert(self, value):
        return value is not None

    def convert(self, value):
        return value

    def get_message(self):
        return 'invalid format'


class by_default(Converter):
    def need_to_convert(self, value):
        return not self._validator.validate(value)

    def __init__(self, default_value):
        self._default_value = default_value
        self._validator = provided()

    def convert(self, value):
        return self._default_value


class blank_by_default(by_default):
    def __init__(self):
        super().__init__('')


class null_by_default(by_default):
    def __init__(self):
        super().__init__(None)


class model_of(Converter):
    def __init__(self, model_class):
        self._model_class = model_class
        self._model_getter = self._model_class.objects.get

    def convert(self, value):
        return self._model_getter(pk=value)

    def get_message(self):
        return '{name} with such id not found'.format(name=self._model_class.__name__)


class coordinates(Converter):
    def convert(self, value):
        lat, lng = (v.strip() for v in value.split(','))
        return lat, lng


class geos_coordinates(coordinates):
    def convert(self, value):
        lat, lng = super().convert(value)
        return GEOSGeometry('POINT({LAT} {LON})'.format(LAT=lat, LON=lng), srid=4326)


class csv(Converter):
    def convert(self, value):
        return value.split(',')

    def get_message(self):
        return 'unable to represent as comma separated values'


class logical(Converter):
    def need_to_convert(self, value):
        return True

    def convert(self, value):
        if isinstance(value, str):
            value = value.lower()

            if value in ('true', 'yes', 'y', '1'):
                return True

            if value in ('false', 'no', 'n', '0'):
                return False

        return bool(value)


class timestamp(Converter):
    def convert(self, value):
        return datetime.fromtimestamp(value)

    def get_message(self):
        return 'unable to represent as timestamp'


class datetime_in(Converter):
    def __init__(self, template):
        self._template = template

    def convert(self, value):
        return datetime.strptime(value, self._template)

    def get_message(self):
        return 'unable to represent as {template}'.format(template=self._template)


class date_in(datetime_in):
    def convert(self, value):
        return super().convert(value).date()

    def get_message(self):
        return 'unable to represent as {template}'.format(template=self._template)


class time_in(datetime_in):
    def convert(self, value):
        return super().convert(value).time()

    def get_message(self):
        return 'unable to represent as {template}'.format(template=self._template)


class integer(Converter):
    def convert(self, value):
        return int(value)

    def get_message(self):
        return 'unable to represent as integer'


class real(Converter):
    def convert(self, value):
        return float(value)

    def get_message(self):
        return 'unable to represent as float'


class lowercased(Converter):
    def convert(self, value):
        return value.lower()

    def get_message(self):
        return "Invalid format"


class uppercased(Converter):
    def convert(self, value):
        return value.upper()

    def get_message(self):
        return "Invalid format"


class stripped(Converter):
    def convert(self, value):
        return value.strip()

    def get_message(self):
        return "Invalid format"
