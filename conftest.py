import pytest
from helpers import *
from data import *


@pytest.fixture(scope="function")
def unique_user_payload():
    """Подготовка уникального payload для создания пользователя"""
    email = generate_unique_email()
    payload = VALID_USER_PAYLOAD.copy()
    payload["email"] = email
    return payload


@pytest.fixture(scope="function")
def registered_user(unique_user_payload):
    """Создание пользователя перед тестом и его удаление после"""
    """Создание пользователя"""
    create_response = create_user(unique_user_payload)
    assert_response_status(create_response, 200, "Failed to create user")
    """Авторизация пользователя"""
    login_response = login_user(unique_user_payload["email"], unique_user_payload["password"])
    assert_response_status(login_response, 200, "Failed to login user")
    access_token = login_response.json()["accessToken"]
    refresh_token = login_response.json()["refreshToken"]
    yield unique_user_payload, access_token, refresh_token
    """Очистка: выход и удаление пользователя"""
    logout_response = logout_user(refresh_token)
    assert_response_status(logout_response, 200, "Failed to logout user")
    delete_response = delete_user(access_token)
    assert_response_status(delete_response, 200, "Failed to delete user")
