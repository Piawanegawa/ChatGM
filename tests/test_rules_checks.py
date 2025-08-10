from fastapi.testclient import TestClient

from app.main import app


def test_rules_checks() -> None:
    payload = {
        "scene": {"description": "A locked door in a dark room"},
        "party": {"members": ["a", "b", "c"]},
    }
    with TestClient(app) as client:
        res = client.post("/rules/checks", json=payload)
        assert res.status_code == 200
        data = res.json()["checks"]
        assert 2 <= len(data) <= 4
        first = data[0]
        assert {"skill", "dc", "reason", "on_success", "on_fail"} <= first.keys()
        for check in data:
            assert 5 <= check["dc"] <= 30
