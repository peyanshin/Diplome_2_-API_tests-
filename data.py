# data.py

VALID_USER_PAYLOAD = {
    "email": "test-user_{}_@yandex.ru",
    "password": "password123",
    "name": "TestUser"
}

EXISTING_USER_PAYLOAD = {
    "email": "existing-user@yandex.ru",
    "password": "password",
    "name": "ExistingUser"
}

MISSING_FIELD_PAYLOAD = {
    "email": "missing-field-user@yandex.ru",
    "name": "MissingFieldUser"
}

VALID_LOGIN_PAYLOAD = {
    "email": "existing-user@yandex.ru",
    "password": "password"
}

INVALID_LOGIN_PAYLOAD = {
    "email": "nonexistent-user@yandex.ru",
    "password": "wrong-password"
}

ORDER_PAYLOAD_WITH_INGREDIENTS = {
    "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
}

ORDER_PAYLOAD_EMPTY_INGREDIENTS = {
    "ingredients": []
}

ORDER_PAYLOAD_INVALID_HASH = {
    "ingredients": ["invalid_hash_123", "another_bad_hash"]
}

EXPECTED_STATUSES = {
    "success": 200,
    "user_exists": 403,
    "missing_fields": 403,
    "unauthorized": 401,  # статус 200 — API не требует авторизации для создания заказа??? БАГ???
    "not_found": 404,
    "created": 201,  # статус 200 — Спецификация API изменилась, и теперь создание заказа отвечает 200??? БАГ???
    "bad_request": 400  # статус 500 — Сервер падает при обработке некорректных хешей ингредиентов??? БАГ???
}

ERROR_MESSAGES = {
    "user_exists": "User already exists",
    "missing_fields": "Email, password and name are required fields",
    "unauthorized": "You should be logged in to perform this action",
    "invalid_token": "Invalid token",
    "invalid_credentials": "email or password are incorrect",
    "login_missing_fields": "Email and password are required",
    
    "order_unauthorized": "You are not authorized to perform this action",
    "invalid_ingredients": "One or more ingredient hashes are invalid",
    "no_ingredients": "Ingredient ids must be provided",
    "jwt_malformed": "jwt malformed"
}

ASSERT_MESSAGES = {
    "missing_id": "В ответе отсутствует поле 'id'",
    "invalid_id_type": "Поле 'id' должно быть целым числом",
    "missing_track": "В ответе отсутствует поле 'track'",
    "missing_orders": "В ответе отсутствует список заказов (поле 'orders')",
    "invalid_orders_type": "Поле 'orders' не является списком",
    
    "create_courier_success_status": "Ожидался статус 201, получен {actual}: {response_text}",
    "user_creation_success_status": "Ожидался статус 200, получен {actual}: {response_text}",
    "user_exists_status": "Ожидался статус 403, получен {actual}: {response_text}",
    "missing_fields_status": "Ожидался статус 403, получен {actual}: {response_text}",
    "unauthorized_status": "Ожидался статус 401, получен {actual}: {response_text}",
    "bad_request_status": "Ожидался статус 400, получен {actual}: {response_text}",
    "error_message_mismatch": "Ожидалось сообщение '{expected}', получено: '{actual}'",
    
    "access_token_missing": "Access token не получен",
    "refresh_token_missing": "Refresh token не получен",
    "login_success_status": "Ожидался статус 200, получен {actual}: {response_text}",
    "invalid_credentials_status": "Ожидался статус 401, получен {actual}: {response_text}",
    "invalid_credentials_message": "Ожидалось сообщение '{expected}', получено: '{actual}'",
    
    "order_created_status": "Ожидался статус {expected}, получен {actual}: {response_text}",
    "order_unauthorized_status": "Ожидался статус {expected}, получен {actual}: {response_text}",
    "invalid_ingredients_status": "Ожидался статус {expected}, получен {actual}: {response_text}",
    "no_ingredients_status": "Ожидался статус {expected}, получен {actual}: {response_text}",
    "order_id_missing": "В ответе отсутствует поле 'order.id'",
    "order_number_missing": "В ответе отсутствует поле 'order.number'",
    "invalid_ingredients_message": "Ожидалось сообщение '{expected}', получено: '{actual}'",
    "order_unauthorized_message": "Ожидалось сообщение '{expected}', получено: '{actual}'",
    "unexpected_key_error": "Ошибка ключа в сообщении: ожидалось поле '{expected}', но получено: {actual}"
}

SUCCESS_MESSAGES = {
    "user_created": "User created",
    "login_success": "Login successful",
    "order_created": "Order created"
}
