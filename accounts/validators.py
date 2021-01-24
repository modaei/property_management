from django.core.exceptions import ValidationError
import re


def validate_phone_number(phone_number):
    rule = re.compile(r'^[0-9]{10,14}$')  # ^[+]?[0-9]{10,14}$
    if not rule.search(phone_number):
        raise ValidationError('Not a valid cell phone number.')


def validate_names(name):
    bad_characters = '^"?()\[]{}\'\^&$!#%-+<>,.;~'
    if any(char in bad_characters for char in name) or len(name) < 3:
        raise ValidationError('Not a valid name.')

    # rule = re.compile(r'^[^"?()\[\]{}\'\^&$!#%-+<>]{3,}$')
    # if not rule.search(name):
    #     raise ValidationError('Not a valid name.')


class DifferentPasswordValidator:
    def validate(self, password, user=None):
        if not user:
            return
        if user.check_password(password):
            raise ValidationError("New password is the same as old password.")

    def get_help_text(self):
        return ""
