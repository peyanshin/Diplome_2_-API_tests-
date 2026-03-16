import allure

from helpers import *
from data import *


class TestOrderCreation:
    @allure.title("Тест на создание заказа с ингредиентами под авторизацией")
    def test_create_order_with_ingredients(self, registered_user):
        _, access_token, _ = registered_user
        with allure.step("Отправка запроса на создание заказа с ингредиентами"):
            response = create_order(access_token, ORDER_PAYLOAD_WITH_INGREDIENTS)
        with allure.step("Проверка статуса ответа (200)"):
            expected_status = EXPECTED_STATUSES["created"]
            actual_status = response.status_code
            assert actual_status == expected_status, ASSERT_MESSAGES["order_created_status"].format(expected=expected_status, actual=actual_status, response_text=response.text)
        with allure.step("Проверка наличия order.id"):
            order_id = response.json().get("order", {}).get("id")
            assert order_id is not None, ASSERT_MESSAGES["order_id_missing"]
        with allure.step("Проверка наличия order.number"):
            order_number = response.json().get("order", {}).get("number")
            assert order_number is not None, ASSERT_MESSAGES["order_number_missing"]

    @allure.title("Тест на попытку создания заказа без авторизации")
    def test_create_order_unauthorized(self):
        with allure.step("Отправка запроса на создание заказа без авторизации"):
            response = create_order_unauthorized(ORDER_PAYLOAD_WITH_INGREDIENTS)
        with allure.step("Проверка статуса ответа (401)"):
            expected_status = EXPECTED_STATUSES["unauthorized"]
            actual_status = response.status_code
            assert actual_status == expected_status, ASSERT_MESSAGES["order_unauthorized_status"].format(expected=expected_status, actual=actual_status, response_text=response.text)
        with allure.step("Проверка текста ошибки"):
            expected_message = ERROR_MESSAGES["order_unauthorized"]
            actual_message = response.json().get("message", "")
            assert expected_message in actual_message, ASSERT_MESSAGES["order_unauthorized_message"].format(expected=expected_message, actual=actual_message)

    @allure.title("Тест на попытку создания заказа с неверными хешами ингредиентов")
    def test_create_order_invalid_ingredients(self, registered_user):
        _, access_token, _ = registered_user
        with allure.step("Отправка запроса на создание заказа с неверными хешами ингредиентов"):
            response = create_order(access_token, ORDER_PAYLOAD_INVALID_HASH)
        with allure.step("Проверка статуса ответа (400)"):
            expected_status = EXPECTED_STATUSES["bad_request"]
            actual_status = response.status_code
            assert actual_status == expected_status, ASSERT_MESSAGES["invalid_ingredients_status"].format(expected=expected_status, actual=actual_status, response_text=response.text)
        with allure.step("Проверка текста ошибки"):
            expected_message = ERROR_MESSAGES["invalid_ingredients"]
            actual_message = response.json().get("message", "")
            assert expected_message in actual_message, ASSERT_MESSAGES["invalid_ingredients_message"].format(expected=expected_message, actual=actual_message)

    @allure.title("Тест на попытку создания заказа без ингредиентов")
    def test_create_order_empty_ingredients(self, registered_user):
        _, access_token, _ = registered_user
        with allure.step("Отправка запроса на создание заказа с пустым списком ингредиентов"):
            response = create_order(access_token, ORDER_PAYLOAD_EMPTY_INGREDIENTS)
        with allure.step("Проверка статуса ответа (400)"):
            expected_status = EXPECTED_STATUSES["bad_request"]
            actual_status = response.status_code
            assert actual_status == expected_status, ASSERT_MESSAGES["no_ingredients_status"].format(expected=expected_status, actual=actual_status, response_text=response.text)
        with allure.step("Проверка текста ошибки"):
            expected_message = ERROR_MESSAGES["no_ingredients"]
            actual_message = response.json().get("message", "")
            assert expected_message in actual_message, ASSERT_MESSAGES["invalid_ingredients_message"].format(expected=expected_message, actual=actual_message)
