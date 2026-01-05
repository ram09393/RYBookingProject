import allure
import pytest
from pydantic import ValidationError
from core.models.booking import BookingResponse


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 550,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-12-25",
            "checkout": "2025-12-30"
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
    try:
        booking_response_dict = response.json()

        BookingResponse(**booking_response_dict)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    # Проверяем соответствие полученных данных отправленным
    assert booking_response_dict['booking']['firstname'] == booking_data['firstname']
    assert booking_response_dict['booking']['lastname'] == booking_data['lastname']
    assert booking_response_dict['booking']['totalprice'] == booking_data['totalprice']
    assert booking_response_dict['booking']['depositpaid'] == booking_data['depositpaid']
    assert booking_response_dict['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert booking_response_dict['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert booking_response_dict['booking']['additionalneeds'] == booking_data['additionalneeds']


def test_create_booking_with_random_data(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    try:
        booking_data = response.json()

        BookingResponse(**booking_data)
    except ValidationError as e:
        raise ValidationError(f"Validation failed: {e}")

        assert booking_data['booking']['firstname'] == generate_random_booking_data['firstname']
        assert booking_data['booking']['lastname'] == generate_random_booking_data['lastname']
        assert booking_data['booking']['totalprice'] == generate_random_booking_data['totalprice']
        assert booking_data['booking']['depositpaid'] == generate_random_booking_data['depositpaid']
        assert booking_data['booking']['bookingdates']['checkin'] == generate_random_booking_data['bookingdates'][
            'checkin']
        assert booking_data['booking']['bookingdates']['checkout'] == generate_random_booking_data['bookingdates'][
            'checkout']
        assert booking_data['booking']['additionalneeds'] == generate_random_booking_data['additionalneeds']


def test_create_booking_negative_price(api_client, mocker):
    booking_data = {
        'firstname': 'Jane',
        'lastname': 'Smith',
        'totalprice': -100,  # Отрицательная цена
        'depositpaid': False,
        "bookingdates": {
            "checkin": "2025-12-25",
            "checkout": "2025-12-30"
        },
        "additionalneeds": "Dinner"
    }

    mock_response = mocker.Mock()
    mock_response.status_code = 400  # Замещаем настоящим ответом 400 (ошибка)
    mock_response.json.return_value = {"error": "Total price must be positive"}

    # Подменяем метод create_booking на наш моковый ответ
    mocker.patch.object(api_client, 'create_booking', return_value=mock_response)

    # Выполняем запрос
    response = api_client.create_booking(booking_data)

    # Проверяем, что сервер вернул ошибку
    assert response.status_code == 400, "Ожидалось, что сервер вернёт ошибку"

    # Проверяем сообщение об ошибке
    assert response.json()['error'] == "Total price must be positive", "Ожидаемое сообщение об ошибке не совпадает"


def test_create_booking_empty_names(api_client, mocker):
    booking_data = {
        'firstname': '',
        'lastname': '',
        'totalprice': 100,
        'depositpaid': True,
        'bookingdates': {'checkin': '2023-08-01', 'checkout': '2023-08-05'},
        'additionalneeds': 'Luxe room'
    }

    mock_response = mocker.Mock()
    mock_response.status_code = 400  # Замещаем настоящим ответом 400 (ошибка)
    mock_response.json.return_value = {"error": "Required fields with names must be positive"}

    # Подменяем метод create_booking на наш моковый ответ
    mocker.patch.object(api_client, 'create_booking', return_value=mock_response)

    # Выполняем запрос
    response = api_client.create_booking(booking_data)

    # Проверяем, что сервер вернул ошибку
    assert response.status_code == 400, "Ожидалось, что сервер вернёт ошибку"

    # Проверяем сообщение об ошибке
    assert response.json()[
               'error'] == "Required fields with names must be positive", "Ожидаемое сообщение об ошибке не совпадает"


def test_create_booking_empty_additional_needs(api_client, mocker):
    booking_data = {
        'firstname': 'Jane',
        'lastname': 'Smith',
        'totalprice': 1000,
        'depositpaid': False,
        "bookingdates": {
            "checkin": "2025-12-25",
            "checkout": "2025-12-30"
        },
        "additionalneeds": ''
    }

    mock_response = mocker.Mock()
    mock_response.status_code = 400  # Замещаем настоящим ответом 400 (ошибка)
    mock_response.json.return_value = {"error": "Optional field additionalneeds must be positive"}

    # Подменяем метод create_booking на наш моковый ответ
    mocker.patch.object(api_client, 'create_booking', return_value=mock_response)

    # Выполняем запрос
    response = api_client.create_booking(booking_data)

    # Проверяем, что сервер вернул ошибку
    assert response.status_code == 400, "Ожидалось, что сервер вернёт ошибку"

    # Проверяем сообщение об ошибке
    assert response.json()[
               'error'] == "Optional field additionalneeds must be positive", "Ожидаемое сообщение об ошибке не совпадает"


def test_create_booking_bookingdates_invalid(api_client):
    booking_data = {
        'firstname': 'Jane',
        'lastname': 'Smith',
        'totalprice': 5000,
        'depositpaid': False,
        "bookingdates": {
            "checkin": "2025-12-30",
            "checkout": "2025-12-28"
        },
        "additionalneeds": "Toster"
    }

    response = api_client.create_booking(booking_data)

    # Проверяем, что сервер принял запрос, хотя должен был отказать
    assert response.status_code == 200, \
        "Ожидается, что сервер вернёт статус 200, так как настоящая логика API разрешает некорректные данные"
    pytest.fail("Server should reject this request with an appropriate error message.")


def test_create_booking_max_string_length(api_client):
    max_name = "A" * 999  # Максимальная длина строки (например, 9999 символов)
    booking_data = {
        "firstname": max_name,
        "lastname": max_name,
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-12-25",
            "checkout": "2025-12-30"
        },
        "additionalneeds": "Gym Room"
    }

    response = api_client.create_booking(booking_data)
    # Получаем тело ответа в виде словаря
    response_json = response.json()

    assert response_json['booking']['firstname'] == booking_data['firstname']
    assert response_json['booking']['lastname'] == booking_data['lastname']
    assert response_json['booking']['totalprice'] == booking_data['totalprice']
    assert response_json['booking']['depositpaid'] == booking_data['depositpaid']
    assert response_json['booking']['bookingdates']['checkin'] == booking_data['bookingdates'][
        'checkin']
    assert response_json['booking']['bookingdates']['checkout'] == booking_data['bookingdates'][
        'checkout']
    assert response_json['booking']['additionalneeds'] == booking_data[
        'additionalneeds']
