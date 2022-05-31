from django.core.validators import RegexValidator


class ValidationConstants:
    """Regex Validator strings defined here"""

    PHONE_NUMBER_REGEX = RegexValidator(r'[6-9][0-9]{9}', 'Enter a valid phone number')
    NAME_REGEX = RegexValidator(r'^[a-zA-Z\']{4,}(?: [a-zA-Z]+){0,2}$', 'Enter a valid name')
