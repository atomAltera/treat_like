class ProcessException(Exception):
    def __init__(self, name, message):
        self.name = name
        self.message = message


class FormatException(ProcessException):
    pass


class ValidationException(ProcessException):
    pass
