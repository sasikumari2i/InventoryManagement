from django.core.validators import RegexValidator

class ValidationConstants:
    """Regex Validator strings defined here"""

    PHONE_NUMBER_REGEX = RegexValidator(r'[6-9][0-9]{9}', 'Enter a valid phone number')
    NAME_REGEX = RegexValidator(r'[A-Za-z]+([ ][a-zA-Z]+)*', 'Enter a valid name')