from commons.app_errors import AppError


class OnlyCommentActivityTypeAllowedError(AppError):
    message_template = 'Разрешено создавать только активности типа "comment"'
    code = "activities.only_comment_type_allowed"
