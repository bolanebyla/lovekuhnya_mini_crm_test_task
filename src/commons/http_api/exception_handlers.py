from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse, Response

from commons.app_errors import AppError
from commons.app_errors.errors import ForbiddenError, NotFoundError


def app_error_handler(request: Request, exc: Exception) -> Response:
    """
    Создаёт обработчик ошибок слоя приложения
    """
    if isinstance(exc, ForbiddenError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": exc.message if exc.message else "Forbidden",
                "code": exc.code,
            },
        )
    elif isinstance(exc, NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": exc.message if exc.message else "Not found",
                "code": exc.code,
            },
        )

    elif isinstance(exc, AppError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": exc.message,
                "code": exc.code,
                "context": exc.context,
            },
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error"},
    )


def validation_exception_handler(request: Request, exc: Exception) -> Response:
    if not isinstance(exc, RequestValidationError):
        raise ValueError(f"Обработчик поддерживает только {RequestValidationError.__name__}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )
