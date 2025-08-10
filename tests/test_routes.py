from fastapi.testclient import TestClient

from app.main import app
from app.state.db import get_state


def test_health() -> None:
    with TestClient(app) as client:
        res = client.get("/health")
        assert res.status_code == 200
        assert res.json() == {"ok": True}


def test_get_scene() -> None:
    with TestClient(app) as client:
        res = client.get("/scene/1")
        assert res.status_code == 200
        assert res.json()["id"] == 1


def test_state_apply() -> None:
    with TestClient(app) as client:
        res = client.post(
            "/state/apply",
            json={"updates": [{"op": "set", "key": "foo", "value": 1}]},
        )
        assert res.status_code == 200
        assert res.json() == {"ok": True}
    assert get_state("foo") == 1
