import json
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, API_KEY


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


VALID_HEADERS = {"X-API-KEY": API_KEY, "Content-Type": "application/json"}


# ─── Auth Tests ───────────────────────────────────────────────────────────────

def test_missing_api_key(client):
    res = client.post("/sum", json={"numbers": [1, 2, 3]})
    assert res.status_code == 401

def test_invalid_api_key(client):
    res = client.post("/sum",
                      json={"numbers": [1, 2, 3]},
                      headers={"X-API-KEY": "wrong-key", "Content-Type": "application/json"})
    assert res.status_code == 403


# ─── Functional Tests ─────────────────────────────────────────────────────────

def test_basic_sum(client):
    res = client.post("/sum", json={"numbers": [5, 10, 15]}, headers=VALID_HEADERS)
    assert res.status_code == 200
    data = res.get_json()
    assert data["result"] == 30

def test_empty_list(client):
    res = client.post("/sum", json={"numbers": []}, headers=VALID_HEADERS)
    assert res.status_code == 200
    assert res.get_json()["result"] == 0

def test_float_numbers(client):
    res = client.post("/sum", json={"numbers": [1.5, 2.5, 3.0]}, headers=VALID_HEADERS)
    assert res.status_code == 200
    assert res.get_json()["result"] == 7.0

def test_negative_numbers(client):
    res = client.post("/sum", json={"numbers": [-5, -10, 15]}, headers=VALID_HEADERS)
    assert res.status_code == 200
    assert res.get_json()["result"] == 0


# ─── Validation Tests ─────────────────────────────────────────────────────────

def test_missing_numbers_field(client):
    res = client.post("/sum", json={"data": [1, 2]}, headers=VALID_HEADERS)
    assert res.status_code == 400

def test_numbers_not_a_list(client):
    res = client.post("/sum", json={"numbers": 42}, headers=VALID_HEADERS)
    assert res.status_code == 400

def test_non_numeric_values(client):
    res = client.post("/sum", json={"numbers": [1, "two", 3]}, headers=VALID_HEADERS)
    assert res.status_code == 400

def test_invalid_json(client):
    res = client.post("/sum",
                      data="not json",
                      headers={"X-API-KEY": API_KEY, "Content-Type": "application/json"})
    assert res.status_code == 400
