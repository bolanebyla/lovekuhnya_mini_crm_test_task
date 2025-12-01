from fastapi import Request
from starlette.responses import JSONResponse, Response

from commons.app_errors import AppError


def app_error_handler(request: Request, exc: Exception) -> Response:
    """
    Создаёт обработчик ошибок слоя приложения
    """
    if isinstance(exc, AppError):
        return JSONResponse(
            status_code=400,
            content={
                "message": exc.message,
                "code": exc.code,
            },
        )

    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )
