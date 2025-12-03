from fastapi import Request
from starlette.responses import JSONResponse, Response

from commons.app_errors import AppError
from commons.app_errors.errors import ForbiddenError


def app_error_handler(request: Request, exc: Exception) -> Response:
    """
    Создаёт обработчик ошибок слоя приложения
    """
    if isinstance(exc, ForbiddenError):
        return JSONResponse(
            status_code=403,
            content={
                "detail": exc.message if exc.message else "Forbidden",
                "code": exc.code,
            },
        )

    elif isinstance(exc, AppError):
        return JSONResponse(
            status_code=400,
            content={
                "detail": exc.message,
                "code": exc.code,
                "context": exc.context,
            },
        )

    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )
