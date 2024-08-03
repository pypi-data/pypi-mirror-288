from typing import Type
import pytest
from pytest_mock import MockFixture
from helper_i18n.handler.i18n_handler import I18nHandler


@pytest.fixture
def factory_sut():
    return I18nHandler

@pytest.fixture
def sut(mocker: MockFixture):
    mocker.patch("helper_i18n.handler.i18n_handler.load_i18n_file", return_value={"exception": {"valid_key":"valid_value"}, "message": {"valid_key":"valid_value"}})
    return I18nHandler("test")
    

def test_should_use_load_i18n_file_with_i18n_path(factory_sut:Type[I18nHandler], mocker: MockFixture):
    load_spy = mocker.patch("helper_i18n.handler.i18n_handler.load_i18n_file")

    factory_sut("test")

    load_spy.assert_called_once_with("test")
    
def test_should_throw_exception_when_i18n_file_format_is_invalid(factory_sut:Type[I18nHandler], mocker: MockFixture):
    mocker.patch("helper_i18n.handler.i18n_handler.load_i18n_file", side_effect=ValueError)

    with pytest.raises(ValueError):
        factory_sut("test")

def test_should_return_message_in_get_exception_message_if_exist(sut: I18nHandler):
    assert sut.get_exception_message("valid_key") == "valid_value"
    
def test_should_return_key_in_get_exception_message_if_not_exist(sut: I18nHandler):
    assert sut.get_exception_message("invalid_key") == "invalid_key"
    
def test_should_return_message_in_get_message_if_exist(sut: I18nHandler):
    assert sut.get_message("valid_key") == "valid_value"
    
def test_should_return_key_in_get_message_if_not_exist(sut: I18nHandler):
    assert sut.get_message("invalid_key") == "invalid_key"