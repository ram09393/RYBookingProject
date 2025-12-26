from unittest import result

import allure
from pydantic import ValidationError
from core.models.booking import BookingResponse
import pytest


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
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']["bookingdates"]["checkin"] == booking_data['bookingdates']['checkin']
    assert response['booking']["bookingdates"]["checkout"] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


def test_create_booking_with_random_data(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")


def test_create_booking_invalid_date_format(api_client, booking_dates):
    booking_data = {
        "firstname": "Pavel",
        "lastname": "Popov",
        "totalprice": 1000,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "25-Dec-2025",  # Неправильный формат даты
            "checkout": "30-Dec-2025"  # Неправильный формат даты
        },
        "additionalneeds": "Service"
    }

    response = api_client.create_booking(booking_data)
    expected_statuses = [200, 400, 500]  # Ожидаемые коды: ошибка валидации или внутренний сбой
    message = response.get("message", "")

    assert response[
               "status_code"] in expected_statuses, f"Ошибка при попытке создать бронь без фамилии: ожидалось одно из {expected_statuses}, получено {response['status_code']}. Сообщение: {message}"

    if response["status_code"] == 400:
        assert "lastname" in message.lower(), "Сообщение об ошибке не содержит корректные данные поля"


def test_create_booking_checkout_before_checkin(api_client, booking_dates):
    booking_data = {
        "firstname": "Maria",
        "lastname": "Novikova",
        "totalprice": 10000,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-12-30",  # Позднее
            "checkout": "2025-12-25"  # Ранее
        },
        "additionalneeds": "President Luxe"
    }

    response = api_client.create_booking(booking_data)
    expected_statuses = [200, 400, 500]  # Ожидаемые коды: ошибка валидации или внутренний сбой
    message = response.get("message", "")

    assert response[
               "status_code"] in expected_statuses, f"Ошибка при попытке создать бронь без фамилии: ожидалось одно из {expected_statuses}, получено {response['status_code']}. Сообщение: {message}"

    if response["status_code"] == 400:
        assert "lastname" in message.lower(), "Сообщение об ошибке не содержит корректные данные поля"


def test_create_booking_max_string_length(api_client):
    max_name = "A" * 255  # Максимальная длина строки (например, 255 символов)
    booking_data = {
        "firstname": max_name,
        "lastname": max_name,
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-12-25",
            "checkout": "2025-12-30"
        },
        "additionalneeds": max_name
    }

    response = api_client.create_booking(booking_data)
    expected_statuses = [200, 400, 500]  # Ожидаемые коды: ошибка валидации или внутренний сбой
    message = response.get("message", "")

    assert response[
               "status_code"] in expected_statuses, f"Ошибка при попытке создать бронь без фамилии: ожидалось одно из {expected_statuses}, получено {response['status_code']}. Сообщение: {message}"

    if response["status_code"] == 400:
        assert "lastname" in message.lower(), "Сообщение об ошибке не содержит корректные данные поля"


def test_create_booking_missing_lastname(api_client):
    booking_data = {
        "firstname": "Vasily",
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-12-25",
            "checkout": "2025-12-30"
        },
        "additionalneeds": "Room service"
    }

    with pytest.raises(Exception) as excinfo:
        api_client.create_booking(booking_data)
