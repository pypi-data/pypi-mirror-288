from typing import TypedDict

errors = list[dict[str, str]]


class I18nDict(TypedDict):
    exception: dict[str, str]
    message: dict[str, str]
