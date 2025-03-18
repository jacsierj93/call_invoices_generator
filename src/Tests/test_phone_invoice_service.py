import httpretty
from fastapi.testclient import TestClient

from Dto.Models import UserResponse
from main import app

client = TestClient(app)

EXPECTED_RESPONSE = {
    'calls': [{
        'amount': 346.5,
        'duration': 462,
        'phone_number': '+191167980952',
        'timestamp': '2025-01-01T04:02:45Z'
    }],
    'friends_discount': -346.5,
    'gross_total': 346.5,
    'total': 0.0,
    'total_friends_seconds': 462.0,
    'total_international_seconds': 462.0,
    'total_national_seconds': 0.0,
    'user': {
        'address': '7431 Berge Coves',
        'name': 'Deshawn Goodwin',
        'phone_number': '+5411111111111'
    }
}

@httpretty.activate
def test_get_invoice_given_correct_info():
    # Mocking the external API call
    httpretty.register_uri(
        httpretty.GET,
        "https://fn-interview-api.azurewebsites.net/users/+5411111111111",
        body='{"address": "7431 Berge Coves","friends": ["+191167980952","+5491167930920"],"name": "Deshawn Goodwin","phone_number": "+5411111111111"}',
        content_type="application/json",
        status=200  # Define the expected status code
    )
    response = client.post(
        "/get-invoice/",
        json={"phone_number": "+5411111111111", "date_from": "2025-01-01", "date_to": "2025-02-01"},
    )
    assert response.status_code == 200
    assert response.json() == EXPECTED_RESPONSE

@httpretty.activate
def test_return_error_when_user_not_exist():
    # Mocking the external API call
    httpretty.register_uri(
        httpretty.GET,
        "https://fn-interview-api.azurewebsites.net/users/+5411111111111",
        body='{}',
        content_type="application/json",
        status=404  # Define the expected status code
    )
    response = client.post(
        "/get-invoice/",
        json={"phone_number": "+5411111111111", "date_from": "2025-01-01", "date_to": "2025-02-01"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail":"User not found"}


def test_return_error_when_no_calls_in_range():
    # Mocking the external API call
    httpretty.register_uri(
        httpretty.GET,
        "https://fn-interview-api.azurewebsites.net/users/+5411111111111",
        body='{}',
        content_type="application/json",
        status=404  # Define the expected status code
    )
    response = client.post(
        "/get-invoice/",
        json={"phone_number": "+5411111111111", "date_from": "2020-01-01", "date_to": "2020-02-01"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail":"No calls found for the given phone number"}