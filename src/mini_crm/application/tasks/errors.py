from commons.app_errors import AppError


class TaskDueDateInPastError(AppError):
    message_template = 'Срок задачи ("due_date") не может быть в прошлом. Минимальная дата: сегодня'
    code = "tasks.task_due_date_in_past_error"
