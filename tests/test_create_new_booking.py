import allure
import pytest
import requests

from core.clients.endpoints import Endpoints


# Каждая функция проверяет разные сценарии:
# - успешное создание брони
# - ошибка из-за отсутствия полей
# - ошибка с сервером (некорректные данные)


@allure.feature('Test Create Booking')
@allure.story('Test successful booking creation')
def test_create_booking_success(api_client, mocker, mock_response=None):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"booking_id": 2}
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    response = api_client.create_booking(
        url="https://restful-booker.herokuapp.com/",

        booking_data={
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 133,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-10-01",
                "checkout": "2025-10-10"
            },
            "additionalneeds": "Lunch"
        })

    assert response['booking_id'] == 2, f"Expected booking_id 1 but got {response['booking_id']}"


@allure.feature('Test Create Booking')
@allure.story('Test booking creation with missing fields')
def test_create_booking_missing_fields(api_client, mocker, mock_response=None):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    with pytest.raises(AssertionError, match="Expected status 200 but got 404"):
        api_client.create_booking({
            "firstname": "Jimmy",
            "lastname": "Dimple",
            "totalprice": 100,
        })


@allure.feature('Test Create Booking')
@allure.story('Test server error during booking creation')
def test_create_booking_server_error(api_client, mocker, mock_response=None, apiclient=None):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    with pytest.raises(AssertionError, match="Expected status 200 but got 500"):
        api_client.create_booking({
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 132,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-10-01",
                "checkout": "2025-10-10"
            }
        })


@allure.feature('Test Create Booking')
@allure.story('Test timeout during booking creation')
def test_create_booking_timeout(api_client, mocker):
    mocker.patch.object(api_client.session, 'post', side_effect=requests.Timeout)

    with pytest.raises(requests.Timeout):
        api_client.create_booking({
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 111,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-13-02",
                "checkout": "2026-13-10"
            }
        })
