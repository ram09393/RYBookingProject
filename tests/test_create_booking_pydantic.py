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
        print(e.json())
        raise


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
    expected_status = [200]
    message = response.get("message", "")


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
    expected_status = [200]
    message = response.get("message", "")


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
    booking_details = response["booking"]

    expected_status = [200]
    message = response.get("message", "")

    assert booking_details["firstname"] == booking_data["firstname"], \
        f"Имя не совпадает: ожидалось {booking_data['firstname']}, пришло {booking_details['firstname']}"

    assert booking_details["lastname"] == booking_data["lastname"], \
        f"Фамилия не совпадает: ожидалось {booking_data['lastname']}, пришло {booking_details['lastname']}"

    assert booking_details["totalprice"] == booking_data["totalprice"], \
        f"Сумма не совпадает: ожидалось {booking_data['totalprice']}, пришло {booking_details['totalprice']}"

    assert booking_details["depositpaid"] == booking_data["depositpaid"], \
        f"Внесение депозита не совпадает: ожидалось {booking_data['depositpaid']}, пришло {booking_details['depositpaid']}"

    assert booking_details["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"], \
        f"Дата вселения не совпадает: ожидалось {booking_data['bookingdates']['checkin']}, пришло {booking_details['bookingdates']['checkin']}"

    assert booking_details["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"], \
        f"Дата выселения не совпадает: ожидалось {booking_data['bookingdates']['checkout']}, пришло {booking_details['bookingdates']['checkout']}"

    assert booking_details["additionalneeds"] == booking_data["additionalneeds"], \
        f"Дополнительные потребности не совпадают: ожидалось {booking_data['additionalneeds']}, пришло {booking_details['additionalneeds']}"


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
