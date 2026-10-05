from fastapi.testclient import TestClient
from kestrel_router.app import app

c = TestClient(app)


def test_health_needs_no_key():
    r = c.get("/health").json()
    assert r["ok"] and r["needs_api_key"] is False


def test_route_returns_team_and_reasons():
    r = c.post("/route", json={"request_text": "water purifier leaking water from bottom", "product_family": "Water Purifier"}).json()
    assert r["team"] == "Repairs" and r["reasons"] and r["paid_api_calls"] == 0


def test_paid_but_not_billing():
    r = c.post("/route", json={"request_text": "installer did not turn up for room heater, i paid extra for this"}).json()
    assert r["team"] == "Installs & Demo"


def test_empty_text_rejected_politely():
    assert c.post("/route", json={"request_text": ""}).status_code == 422


def test_broken_characters_survive():
    r = c.post("/route", json={"request_text": "urgÃ©nt: installer did not turn up for room heater asap"}).json()
    assert r["team"] == "Installs & Demo"


def test_screen_served():
    assert "Route this request" in c.get("/").text
