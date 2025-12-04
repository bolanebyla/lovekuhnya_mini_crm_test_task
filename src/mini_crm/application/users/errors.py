from commons.app_errors import AppError


class UserWithEmailAlreadyExistsError(AppError):
    message_template = 'Пользователь с email "{email}" уже существует'
    code = "users.user_with_email_already_exists_error"
