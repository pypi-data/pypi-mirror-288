from clearskies.binding_config import BindingConfig
from .have_i_been_pwned import HaveIBeenPwned
from .letters_digits import LettersDigits
from .letters_digits_special_characters import LettersDigitsSpecialCharacters
from .password_validation import PasswordValidation


def have_i_been_pwned():
    return BindingConfig(HaveIBeenPwned)


def letters_digits():
    return BindingConfig(LettersDigits)


def letters_digits_special_characters(special_characters="!@#$%^&*()<>,.?~`"):
    return BindingConfig(LettersDigitsSpecialCharacters, special_characters=special_characters)


def password_validation(password_column_name):
    return BindingConfig(PasswordValidation, password_column_name=password_column_name)


__all__ = [
    "have_i_been_pwned",
    "HaveIBeenPwned",
    "letters_digits",
    "letters_digits_special_characters",
    "LettersDigits",
    "LettersDigitsSpecialCharacters",
    "password_validation",
    "PasswordValidation",
]
