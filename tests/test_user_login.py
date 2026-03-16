import allure

from helpers import *
from data import *


class TestUserLogin:
    @allure.title("Тест на вход под существующим пользователем")
    def test_valid_user_login(self):
        with allure.step("Отправка запроса на авторизацию с валидными данными"):
            response = login_user(VALID_LOGIN_PAYLOAD["email"],VALID_LOGIN_PAYLOAD["password"])
        with allure.step("Проверка статуса ответа (200)"):
            expected_status = EXPECTED_STATUSES["success"]
            actual_status = response.status_code
            assert actual_status == expected_status, (ASSERT_MESSAGES["login_success_status"].format(actual=actual_status, response_text=response.text))
        with allure.step("Проверка наличия accessToken"):
            access_token = response.json().get("accessToken")
            assert access_token is not None, ASSERT_MESSAGES["access_token_missing"]
        with allure.step("Проверка наличия refreshToken"):
            refresh_token = response.json().get("refreshToken")
            assert refresh_token is not None, ASSERT_MESSAGES["refresh_token_missing"]
        with allure.step("Проверка данных пользователя в ответе"):
            user_data = response.json().get("user", {})
            assert user_data.get("email") == VALID_LOGIN_PAYLOAD["email"]
            assert user_data.get("name") is not None

    
    @allure.title("Тест на попытку входа с неверными логином/паролем")
    def test_invalid_user_login(self):
        with allure.step("Отправка запроса на авторизацию с неверными данными"):
            response = login_user(INVALID_LOGIN_PAYLOAD["email"],INVALID_LOGIN_PAYLOAD["password"])
        with allure.step("Проверка статуса ответа (401)"):
            expected_status = EXPECTED_STATUSES["unauthorized"]
            actual_status = response.status_code
            assert actual_status == expected_status, (ASSERT_MESSAGES["invalid_credentials_status"].format(actual=actual_status, response_text=response.text))
        with allure.step("Проверка текста ошибки"):
            expected_message = ERROR_MESSAGES["invalid_credentials"]
            actual_message = response.json().get("message", "")
            assert expected_message in actual_message, (ASSERT_MESSAGES["invalid_credentials_message"].format(expected=expected_message, actual=actual_message))
