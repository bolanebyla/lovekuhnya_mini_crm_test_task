from commons.app_errors import AppError
from commons.app_errors.errors import ForbiddenError


class UserWithEmailAlreadyExistsError(AppError):
    message_template = 'Пользователь с email "{email}" уже существует'
    code = "users.user_with_email_already_exists_error"


class InvalidCredentialsError(ForbiddenError):
    message_template = "Неверный email или пароль"
    code = "users.invalid_credentials_error"
