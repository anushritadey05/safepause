
from fastapi.testclient import TestClient
import requests
from bank.api import app

client = TestClient(app)


def test_bank_home_or_health_endpoint():
    # Check the event endpoint with a normal simulated payment.
    response = client.post(
        "/event",
        json={
            "amount": 500,
            "payee_name": "Test Shop",
            "payee_vpa": "testshop@upi"
        }
    )

    # The bank API should return a successful response.
    assert response.status_code == 200

    data = response.json()
    assert data["simulation_only"] is True
    assert data["status"] == "SIMULATED_APPROVED"


def test_bank_pauses_high_risk_payment():
    response = client.post(
        "/event",
        json={
            "amount": 5000,
            "payee_name": "New Shop",
            "payee_vpa": "newshop@upi",
            "remote_access_active": True,
            "payee_first_time": True
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["simulation_only"] is True
    assert data["status"] == "PAUSED_FOR_REVIEW"
    assert data["risk"]["tier"] == "RED"


def test_bank_requests_confirmation_for_amber():
    response = client.post(
        "/event",
        json={
            "amount": 1000,
            "payee_name": "New Friend",
            "payee_vpa": "friend@upi",
            "on_call": True,
            "payee_first_time": True
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "CONFIRM_WITH_USER"
    assert data["risk"]["tier"] == "AMBER"

    
from unittest.mock import patch


def test_risk_engine_unavailable():
    with patch(
        "bank.api.requests.post",
        side_effect=requests.exceptions.ConnectionError(
        "Risk engine unavailable"
    )
    ):
        response = client.post(
            "/event",
            json={
                "amount": 500,
                "payee_name": "Test Shop",
                "payee_vpa": "testshop@upi"
            }
        )

    assert response.status_code == 503

