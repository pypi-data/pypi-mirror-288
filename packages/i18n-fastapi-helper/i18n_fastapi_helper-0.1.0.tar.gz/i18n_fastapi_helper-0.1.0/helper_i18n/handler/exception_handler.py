from typing import Any, Optional, cast
from starlette.applications import Starlette
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from http import HTTPStatus

from helper_i18n.typing import errors
from helper_i18n import CustomException
from helper_i18n.handler.i18n_handler import I18nHandler


class ExceptionHandler:
    def __init__(self, i18n_handler: I18nHandler) -> None:
        self.i18n = i18n_handler

    def include_app(self, app: Starlette):
        app.add_exception_handler(
            RequestValidationError, self.__include_pydantic_exception
        )
        app.add_exception_handler(CustomException, self.__include_custom_exception)

    def __include_pydantic_exception(
        self, request: Request, exception: Exception
    ) -> JSONResponse:
        exception = cast(RequestValidationError, exception)
        errors: list[dict[str, Any]] = []
        for error in exception.errors():
            error_name = error["loc"][1]
            if isinstance(error_name, int):
                error_name = error["loc"][0]
            errors.append(
                {
                    error_name: error["type"],
                }
            )

        return self.__create_response(
            exception.__class__.__name__, request, 422, errors
        )

    def __include_custom_exception(
        self, request: Request, exception: Exception
    ) -> JSONResponse:
        exception = cast(CustomException, exception)
        return self.__create_response(
            exception.i8n_key,
            request,
            exception.status_code,
            exception.errors,
            **exception.params,
        )

    def __create_response(
        self,
        i18n_key: str,
        request: Request,
        status_code: int,
        errors: Optional[errors] = None,
        **params: Any,
    ) -> JSONResponse:
        error = HTTPStatus(status_code).phrase
        language = self.__get_language(request)
        i18n_message = self.i18n.get_exception_message(i18n_key, language, params)
        content: dict[str, list[dict[str, str]] | str] = {
            "error": error,
            "message": i18n_message,
            "path": request.url.path,
        }
        if errors:
            content["errors"] = errors
        return JSONResponse(content=content, status_code=status_code)

    def __get_language(self, request: Request) -> str:
        return request.headers.get("accept-language", self.i18n.default_language)
