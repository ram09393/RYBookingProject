import requests
import pytest
import allure
from core.clients.api_client import ApiClient


@pytest.fixture(scope="session")
def api_client():
    client = ApiClient()
    client.auth()
    return client


@allure.feature('Test Create Booking')
@allure.story('Test successful booking creation')
def test_create_booking_success(api_client):
    generate_random_booking_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 123,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-12-23",
            "checkout": "2025-12-30"
        },
        "additionalneeds": "Breakfast"
    }

    response = api_client.create_booking(generate_random_booking_data)
    assert response.status_code == 200
    assert response.json()['booking']['firstname'] == generate_random_booking_data['firstname']
    with pytest.raises(AssertionError, match="Excepted status 201 but got 200"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature('Test Create Booking')
@allure.story('Test booking creation with missing fields firstname')
def test_create_booking_missing_firstname(api_client):
    generate_random_booking_data = {
        "lastname": "Doe",
        "totalprice": 123,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-12-22",
            "checkout": "2025-12-31"
        }
    }

    with pytest.raises(requests.exceptions.HTTPError) as e:
        api_client.create_booking(generate_random_booking_data)
    assert e.value.response.status_code == 500


@allure.feature('Test Create Booking')
@allure.story('Test booking creation with missing fields lastname')
def test_create_booking_missing_lastname(api_client):
    generate_random_booking_data = {
        "firstname": "John",
        "totalprice": 123,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-12-03",
            "checkout": "2025-12-12"
        }
    }

    with pytest.raises(requests.exceptions.HTTPError) as e:
        api_client.create_booking(generate_random_booking_data)
    assert e.value.response.status_code == 500


@allure.feature('Test Create Booking')
@allure.story('Test booking creation with invalid totalprice')
def test_create_booking_invalid_totalprice(api_client):
    generate_random_booking_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": "-123",  # Неверное значение цены
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-12-01",
            "checkout": "2025-12-10"
        }
    }

    with pytest.raises(requests.exceptions.HTTPError) as e:
        api_client.create_booking(generate_random_booking_data)
    assert e.value.response.status_code == 400


@allure.feature('Test Create Booking')
@allure.story('Test booking creation with invalid depositpaid')
def test_create_booking_invalid_depositpaid(api_client):
    generate_random_booking_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 123,
        "depositpaid": "yes",  # Неверный тип (должно быть булевое значение)
        "bookingdates": {
            "checkin": "2026-01-05",
            "checkout": "2026-01-20"
        }
    }
    with pytest.raises(requests.exceptions.HTTPError) as e:
        api_client.create_booking(generate_random_booking_data)
    assert e.value.response.status_code == 418


def test_create_booking_empty_body(api_client):
    generate_random_booking_data = {}  # Пустое тело запроса

    with pytest.raises(requests.exceptions.HTTPError) as e:
        api_client.create_booking(generate_random_booking_data)
    assert e.value.response.status_code == 500  # Проверка на ошибку 400
