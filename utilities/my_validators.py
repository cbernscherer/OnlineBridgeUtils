import re
from wtforms.validators import ValidationError

class MyRegExValidator():
    def __init__(self, regex, message=None):
        self.regex = re.compile(regex)
        self.message = message

        if not self.message:
            self.message = 'Falsche Form'

    def __call__(self, form, field):
        if field.data:
            if not self.regex.match(field.data):
                raise ValidationError(self.message)
