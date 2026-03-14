import allure

from helpers import *
from data import *


class TestUserCreation:
    @allure.title("Тест на создание уникального пользователя")
    def test_create_unique_user(self, registered_user):
        user_payload, access_token, refresh_token = registered_user
        with allure.step("Проверка успешного создания пользователя"):
            assert access_token is not None, ASSERT_MESSAGES["access_token_missing"]
            assert refresh_token is not None, ASSERT_MESSAGES["refresh_token_missing"]

    @allure.title("Тест на попытку создания уже зарегистрированного пользователя")
    def test_create_existing_user(self):
        with allure.step("Отправка запроса на создание существующего пользователя"):
            response = create_user(EXISTING_USER_PAYLOAD)
        with allure.step("Проверка статуса ответа (403)"):
            expected_status = EXPECTED_STATUSES["user_exists"]
            actual_status = response.status_code
            assert actual_status == expected_status, ASSERT_MESSAGES["user_exists_status"].format(actual=actual_status, response_text=response.text)
        with allure.step("Проверка текста ошибки"):
            expected_message = ERROR_MESSAGES["user_exists"]
            actual_message = response.json().get("message", "")
            assert expected_message in actual_message, ASSERT_MESSAGES["error_message_mismatch"].format(expected=expected_message, actual=actual_message)

    @allure.title("Тест на попытку создания пользователя без обязательного поля")
    def test_create_user_missing_field(self):
        with allure.step("Отправка запроса без обязательного поля"):
            response = create_user(MISSING_FIELD_PAYLOAD)
        with allure.step("Проверка статуса ответа (403)"):
            expected_status = EXPECTED_STATUSES["missing_fields"]
            actual_status = response.status_code
            assert actual_status == expected_status, ASSERT_MESSAGES["missing_fields_status"].format(actual=actual_status, response_text=response.text)
        with allure.step("Проверка текста ошибки"):
            expected_message = ERROR_MESSAGES["missing_fields"]
            actual_message = response.json().get("message", "")
            assert expected_message in actual_message, ASSERT_MESSAGES["error_message_mismatch"].format(expected=expected_message, actual=actual_message)
