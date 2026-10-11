
from fastapi.testclient import TestClient

from engine.api import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["simulation_only"] is True


def test_green_payment():
    response = client.post(
        "/score",
        json={}
    )

    assert response.status_code == 200
    assert response.json()["tier"] == "GREEN"
    assert response.json()["simulation_only"] is True


def test_amber_payment():
    response = client.post(
        "/score",
        json={
            "on_call": True,
            "payee_first_time": True
        }
    )

    assert response.status_code == 200
    assert response.json()["tier"] == "AMBER"


def test_red_payment():
    response = client.post(
        "/score",
        json={
            "remote_access_active": True,
            "payee_first_time": True
        }
    )

    assert response.status_code == 200
    assert response.json()["tier"] == "RED"


def test_invalid_vpa_similarity():
    response = client.post(
        "/score",
        json={
            "vpa_lookalike_score": 1.5
        }
    )

    assert response.status_code == 422
