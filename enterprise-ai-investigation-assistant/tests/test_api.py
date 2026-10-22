from fastapi.testclient import TestClient

from investigation_assistant.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_cases_returns_only_synthetic_examples() -> None:
    response = client.get("/cases")

    assert response.status_code == 200
    cases = response.json()
    assert len(cases) == 2
    assert cases[0]["case_id"] == "CASE-1001"
    assert "fabricated" in cases[0]["summary"]


def test_unknown_case_returns_not_found() -> None:
    response = client.get("/cases/CASE-9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Case not found"}
