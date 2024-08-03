from typing import Any, Mapping, Sequence, Type

from pydantic import BaseModel
from helper_i18n import CustomException


class DocsHandler:
    def __init__(
        self,
        exceptions: Sequence[CustomException],
        responses: Sequence[Mapping[int, Type[BaseModel]]],
    ) -> None:
        self.exceptions = exceptions
        self.responses = responses

    def get_docs(self) -> dict[Any, dict[str, Any]] | None:
        docs: dict[Any, dict[str, Any]] = {}
        exceptions = self.get_exceptions()
        responses = self.get_responses()
        docs.update(exceptions)
        docs.update(responses)
        return docs

    def get_exceptions(self) -> dict[int, dict[str, Any]]:
        exceptions: dict[int, dict[str, Any]] = {}
        for exception in self.exceptions:
            exceptions[exception.status_code] = self.get_exception_content(
                exception.to_dict()
            )
        return exceptions

    def get_responses(self) -> dict[int, dict[str, Any]]:
        responses: dict[int, dict[str, Any]] = {}
        for response in self.responses:
            for status_code, response_data in response.items():
                responses[status_code] = self.get_response_content(response_data)
        return responses

    def get_exception_content(self, exception_data: dict[str, Any]) -> dict[str, Any]:
        content: dict[str, Any] = {
            "content": {
                "application/json": exception_data,
            },
            "description": exception_data["example"]["message"],
        }
        return content

    def get_response_content(self, response_data: Type[BaseModel]) -> dict[str, Any]:
        content: dict[str, Any] = {"model": response_data}
        return content
