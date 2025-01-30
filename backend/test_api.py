import pytest
import httpx
import os
from fastapi import FastAPI
from fastapi.testclient import TestClient
from api import app
from utils import validate_imei


client = TestClient(app)


def test_check_imei_valid():
    imei = "356735111052198"
    token = os.getenv('IMEI_CHECK_API_TOKEN')
    response = client.post("/api/check-imei", json={"imei": imei})
    assert response.status_code == 200
    assert "deviceId" in response.json()


def test_check_imei_invalid():
    imei = "123456789012345"
    token = os.getenv('IMEI_CHECK_API_TOKEN')
    response = client.post("/api/check-imei", json={"imei": imei, "token": token})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid IMEI format"


def test_get_services():
    response = client.get("/api/get-services")
    assert response.status_code == 200
    assert "services" in response.json()
