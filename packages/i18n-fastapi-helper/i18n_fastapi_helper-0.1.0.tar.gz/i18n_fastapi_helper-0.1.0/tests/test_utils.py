from typing import Any, Callable
from helper_i18n.utils import load_i18n_file, check_i18n_file_format
import pytest
from pytest_mock import MockFixture
from json import dumps

mock_i18n: dict[str, Any] = {"exception": {}, "message": {}}


@pytest.fixture
def load_sut(mocker: MockFixture):
    mocker.patch("builtins.open", mocker.mock_open(read_data=dumps(mock_i18n)))
    mocker.patch("json.loads", return_value=mock_i18n)
    return load_i18n_file


@pytest.fixture
def check_sut():
    return check_i18n_file_format

def test_load_i18n_file_should_try_open_18n_file(
    load_sut: Callable[[Any], Any], mocker: MockFixture
):
    open_spy = mocker.patch(
        "builtins.open", mocker.mock_open(read_data=dumps(mock_i18n))
    )

    load_sut("test")

    open_spy.assert_called_once_with("test", "r")


def test_handler_should_load_i18n_file(load_sut: Callable[[Any], Any], mocker: MockFixture):
    load_spy = mocker.patch("json.loads", return_value=mock_i18n)

    load_sut("test")

    load_spy.assert_called_once_with(dumps(mock_i18n))


def test_should_raise_exception_when_invalid_i18n_file_format(
    load_sut: Callable[[Any], Any], mocker: MockFixture
):
    mocker.patch("helper_i18n.utils.check_i18n_file_format", return_value=False)

    with pytest.raises(ValueError):
        load_sut("test")

def test_should_return_i18n_file_when_valid_i18n_file_format(
    load_sut: Callable[[Any], Any], mocker: MockFixture
):
    mocker.patch("helper_i18n.utils.check_i18n_file_format", return_value=True)

    assert load_sut("test") == mock_i18n

def test_should_return_false_when_i18n_file_doent_have_exception_or_message(
    check_sut: Callable[[dict[str, Any]], bool]
):
    assert check_sut({'exception':{}}) is False
    assert check_sut({'message':{}}) is False

def test_should_return_false_when_i18n_file_exception_or_message_is_not_dict(
    check_sut: Callable[[dict[str, Any]], bool]
):
    assert check_sut({'exception':[], 'message':{}}) is False
    assert check_sut({'exception':{}, 'message':[]}) is False

def test_should_return_true_when_i18n_file_is_valid(check_sut: Callable[[dict[str, Any]], bool]):
    assert check_sut(mock_i18n) is True