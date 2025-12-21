import allure
import pytest
import requests
from pydantic import ValidationError
from self import self
from core.clients.api_client import ApiClient
from urllib3.exceptions import InsecureRequestWarning

from core.clients.endpoints import Endpoints
from core.models.booking import BookingResponse


class Api_Client:
    @pytest.fixture
    def create_booking(self, booking_data):
        response = requests.post("https://restful-booker.herokuapp.com/booking", json=booking_data, verify=False)
        return response


BOOKING_URL = "https://restful-booker.herokuapp.com/booking"
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# - Успешное создание бронирования
@allure.feature('Test Create Booking')
@allure.story('Test successful booking creation')
def test_create_booking_success():
    booking_data = {
        "firstname": "Jack",
        "lastname": "Rain",
        "totalprice": 153,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-12-21",
            "checkout": "2025-12-30"
        },
        "additionalneeds": "Lunch"
    }

    # Отправляем POST-запрос на создание бронирования
    response = requests.post(BOOKING_URL, json=booking_data, verify=False)

    # Проверяем статус-код ответа
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    # Получаем JSON-ответ и проверяем наличие booking_id
    booking_data = response.json()
    assert 'bookingid' in booking_data, "Response not contain booking_id field."


# - Ошибка из-за отсутствия обязательных полей

@allure.feature('Test Create Booking')
@allure.story('Test booking creation with missing fields')
def test_create_booking_missing_fields():
    booking_data = {
        "firstname": "Jimmy",
        "lastname": "Dimple",
        "totalprice": 100,

    }

    # Запрашиваем бронирование с недостаточными полями
    response = requests.post(BOOKING_URL, json=booking_data, verify=False)
    # Проверяем, что сервер вернул статус 400
    assert response.status_code == 500, "Ожидался статус-код 500"

    # Проверяем, что тело ответа содержит правильное сообщение об ошибке
    response_text = response.text.strip()
    expected_message = "Internal Server Error"
    assert expected_message in response_text, f"Ожидалась строка '{expected_message}' в тексте ответа."


# Проверка поведения метода в случае, если сервер вернул таймаут
def test_create_booking_timeout(api_client, mocker):
    # Меняем  post-метод на метод, для получения Timeout
    mocker.patch.object(api_client.session, 'post', side_effect=requests.Timeout)

    # Ожидаем исключение Timeout
    with pytest.raises(requests.Timeout):
        api_client.create_booking(BOOKING_URL, {})
