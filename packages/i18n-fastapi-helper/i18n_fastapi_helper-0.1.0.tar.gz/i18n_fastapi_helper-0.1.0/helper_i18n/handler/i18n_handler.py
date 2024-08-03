from typing import Any
from helper_i18n.utils import load_i18n_file


class I18nHandler:
    def __init__(self, i18npaths: dict[str, str], default_language: str) -> None:
        self.i18n = load_i18n_file(i18npaths)
        self.__define_default_language(default_language)

    def get_exception_message(
        self, key: str, language: str, params: dict[str, Any]
    ) -> str:
        language = self.__get_language(language)
        exception = self.i18n[language]["exception"].get(key, key)
        return exception.format(**params)

    def get_message(self, key: str, language: str, params: dict[str, Any]) -> str:
        language = self.__get_language(language)
        message = self.i18n[language]["message"].get(key, key)
        return message.format(**params)

    def __define_default_language(self, language: str) -> None:
        if language not in self.i18n:
            raise ValueError(f"Language {language} not found in i18n files")
        self.default_language = language

    def __get_language(self, language: str | None = None) -> str:
        languages = language.split(",") if language else []
        for language in languages:
            if language in self.i18n:
                return language
        return self.default_language
