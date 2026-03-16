import pytest
import logging
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
    create_response = create_user(unique_user_payload)
    if create_response.status_code != 200:
        pytest.fail(f"Создание пользователя failed: "f"статус {create_response.status_code}, ответ: {create_response.text}")
    login_response = login_user(unique_user_payload["email"], unique_user_payload["password"])
    if login_response.status_code != 200:
        pytest.fail(f"Авторизация пользователя failed: "f"статус {login_response.status_code}, ответ: {login_response.text}")
    access_token = login_response.json().get("accessToken")
    refresh_token = login_response.json().get("refreshToken")
    if not access_token:
        pytest.fail("В ответе авторизации отсутствует accessToken")
    if not refresh_token:
        pytest.fail("В ответе авторизации отсутствует refreshToken")
    try:
        yield unique_user_payload, access_token, refresh_token
    finally:
        if refresh_token:
            logout_response = logout_user(refresh_token)
            if logout_response.status_code != 200:
                logging.error(f"Logout failed: статус {logout_response.status_code}, "f"ответ: {logout_response.text}")
        if access_token:
            delete_response = delete_user(access_token)
            if delete_response.status_code != 200:
                logging.error(f"Delete failed: статус {delete_response.status_code}, "f"ответ: {delete_response.text}")
