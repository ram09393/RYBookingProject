import requests
import pytest
import allure
from core.clients.api_client import ApiClient


@allure.feature('Test Create Booking')
@allure.story('Test successful booking creation')
def test_create_booking_success(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    booking_details = response["booking"]

    assert booking_details["firstname"] == generate_random_booking_data["firstname"], \
    f"Имя не совпадает: ожидалось {generate_random_booking_data['firstname']}, пришло {booking_details['firstname']}"

    assert booking_details["lastname"] == generate_random_booking_data["lastname"], \
    f"Фамилия не совпадает: ожидалось {generate_random_booking_data['lastname']}, пришло {booking_details['lastname']}"

    assert booking_details["totalprice"] == generate_random_booking_data["totalprice"], \
    f"Сумма не совпадает: ожидалось {generate_random_booking_data['totalprice']}, пришло {booking_details['totalprice']}"

    assert booking_details["depositpaid"] == generate_random_booking_data["depositpaid"], \
    f"Внесение депозита не совпадает: ожидалось {generate_random_booking_data['depositpaid']}, пришло {booking_details['depositpaid']}"

    assert booking_details["bookingdates"]["checkin"] == generate_random_booking_data["bookingdates"]["checkin"], \
    f"Дата вселения не совпадает: ожидалось {generate_random_booking_data['bookingdates']['checkin']}, пришло {booking_details['bookingdates']['checkin']}"

    assert booking_details["bookingdates"]["checkout"] == generate_random_booking_data["bookingdates"]["checkout"], \
    f"Дата выселения не совпадает: ожидалось {generate_random_booking_data['bookingdates']['checkout']}, пришло {booking_details['bookingdates']['checkout']}"

    assert booking_details["additionalneeds"] == generate_random_booking_data["additionalneeds"], \
    f"Дополнительные потребности не совпадают: ожидалось {generate_random_booking_data['additionalneeds']}, пришло {booking_details['additionalneeds']}"

