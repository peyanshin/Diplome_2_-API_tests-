import requests

from url import *


def make_request(method: str, url: str, headers: dict = None, json: dict = None, **kwargs) -> requests.Response:
    """
    Универсальная функция для отправки HTTP‑запросов.
    """
    response = requests.request(method, url, headers=headers, json=json, **kwargs)
    return response


def create_user(payload: dict) -> requests.Response:
    """Создание пользователя"""
    return requests.post(f"{BASE_URL}{CREATE_USER_ENDPOINT}", json=payload)

def login_user(email: str, password: str) -> requests.Response:
    """Авторизация пользователя"""
    return requests.post(f"{BASE_URL}{LOGIN_USER_ENDPOINT}", json={"email": email, "password": password})

def logout_user(refresh_token: str) -> requests.Response:
    """Выход пользователя из системы"""
    return requests.post(f"{BASE_URL}{LOGOUT_USER_ENDPOINT}", json={"token": refresh_token})

def delete_user(access_token: str) -> requests.Response:
    """Удаление пользователя"""
    headers = {"Authorization": f"Bearer {access_token}"}
    return requests.delete(f"{BASE_URL}{DELETE_USER_ENDPOINT}", headers=headers)


def create_order(access_token: str, payload: dict) -> requests.Response:
    """
    Создание заказа (требуется авторизация).
    """
    url = BASE_URL + CREATE_ORDER_ENDPOINT
    headers = {
        "Content-Type": "application/json",
        "Authorization": access_token
    }
    return make_request("POST", url, headers=headers, json=payload)

def create_order_unauthorized(payload: dict) -> requests.Response:
    """
    Создание заказа без авторизации (для проверки 401 статуса).
    """
    url = BASE_URL + CREATE_ORDER_ENDPOINT
    headers = {"Content-Type": "application/json"}
    return make_request("POST", url, headers=headers, json=payload)


def generate_unique_email() -> str:
    """Генерация уникального email"""
    import time
    timestamp = int(time.time() * 1000)
    return f"test-user_{timestamp}@yandex.ru"

def assert_response_status(response: requests.Response, expected_status: int, error_msg: str):
    """
    Проверка статуса ответа API
    """
    assert response.status_code == expected_status, \
        f"{error_msg}: Expected {expected_status}, got {response.status_code}. Response: {response.text}"

def assert_response_contains_message(response: requests.Response, expected_message: str, error_msg: str):
    """
    Проверка наличия сообщения в теле ответа
    """
    response_message = response.json().get("message", "")
    assert expected_message in response_message, \
        f"{error_msg}: Expected '{expected_message}', got '{response_message}'"
