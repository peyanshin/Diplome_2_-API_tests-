import allure

from helpers import *
from data import *


class TestUserCreation:
    @allure.title("Тест на создание уникального пользователя")
    def test_create_unique_user(self, unique_user_payload):
        with allure.step("Создание уникального пользователя"):
            create_response = create_user(unique_user_payload)
            assert create_response.status_code == EXPECTED_STATUSES["success"], (
                ASSERT_MESSAGES["user_creation_success_status"].format(actual=create_response.status_code, response_text=create_response.text))
        with allure.step("Авторизация пользователя"):
            login_response = login_user(unique_user_payload["email"], unique_user_payload["password"])
            assert login_response.status_code == EXPECTED_STATUSES["success"], (ASSERT_MESSAGES["login_success_status"].format(actual=login_response.status_code, response_text=login_response.text))
            access_token = login_response.json().get("accessToken")
            refresh_token = login_response.json().get("refreshToken")
            assert access_token is not None, ASSERT_MESSAGES["access_token_missing"]
            assert refresh_token is not None, ASSERT_MESSAGES["refresh_token_missing"]
        with allure.step("Проверка данных созданного пользователя"):
            user_data = login_response.json()
            assert user_data.get("user", {}).get("email") == unique_user_payload["email"]
            assert user_data.get("user", {}).get("name") == unique_user_payload["name"]


    @allure.title("Тест на попытку создания уже зарегистрированного пользователя")
    def test_create_existing_user(self, registered_user):
        user_payload, _, _ = registered_user
        existing_user_payload = user_payload.copy()
        with allure.step("Отправка запроса на создание существующего пользователя"):
            response = create_user(existing_user_payload)
        with allure.step("Проверка статуса ответа (403)"):
            expected_status = EXPECTED_STATUSES["user_exists"]
            actual_status = response.status_code
            assert actual_status == expected_status, (ASSERT_MESSAGES["user_exists_status"].format(actual=actual_status, response_text=response.text))
        with allure.step("Проверка текста ошибки"):
            expected_message = ERROR_MESSAGES["user_exists"]
            actual_message = response.json().get("message", "")
            assert expected_message in actual_message, (ASSERT_MESSAGES["error_message_mismatch"].format(expected=expected_message, actual=actual_message))


    @allure.title("Тест на попытку создания пользователя без обязательного поля")
    def test_create_user_missing_field(self):
        required_fields = ["email", "password", "name"]
        for field in required_fields:
            with allure.step(f"Отправка запроса без поля {field}"):
                payload = VALID_USER_PAYLOAD.copy()
                payload.pop(field, None)
                response = create_user(payload)
            with allure.step("Проверка статуса ответа (403)"):
                expected_status = EXPECTED_STATUSES["missing_fields"]
                actual_status = response.status_code
                assert actual_status == expected_status, (ASSERT_MESSAGES["missing_fields_status"].format(actual=actual_status, response_text=response.text))
            with allure.step("Проверка текста ошибки"):
                expected_message = ERROR_MESSAGES["missing_fields"]
                actual_message = response.json().get("message", "")
                assert expected_message in actual_message, (ASSERT_MESSAGES["error_message_mismatch"].format(expected=expected_message, actual=actual_message))
