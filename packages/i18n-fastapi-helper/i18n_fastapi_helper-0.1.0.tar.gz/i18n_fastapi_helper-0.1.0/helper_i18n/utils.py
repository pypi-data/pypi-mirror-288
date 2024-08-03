import json
from typing import Any

from helper_i18n.typing import I18nDict


def check_i18n_file_format(i18n_json: dict[str, Any]) -> bool:
    if "exception" not in i18n_json or "message" not in i18n_json:
        return False
    if not isinstance(i18n_json["exception"], dict) or not isinstance(
        i18n_json["message"], dict
    ):
        return False
    return True


def load_i18n_file(i18n_paths: dict[str, str]) -> dict[str, I18nDict]:
    i18_n_json: dict[str, I18nDict] = {}
    for language, i18n_path in i18n_paths.items():
        with open(i18n_path, "r") as file:
            i18n_json = json.load(file)
        if not check_i18n_file_format(i18n_json):
            raise ValueError(f"Invalid i18n file format {i18n_path}")
        i18_n_json[language] = i18n_json
    return i18_n_json
