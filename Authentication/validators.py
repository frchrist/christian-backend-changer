
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.core import validators



@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r'^\+\d{10,20}$'
    message = _(
        "Entre a valid phone number. This value may contain only digits"
    )
    flags = 0



@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[\w_@]+\Z'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/_ characters.'
    )
    flags = 0
