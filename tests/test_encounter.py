from fastapi.testclient import TestClient

from app.main import app


def build(level: int, size: int):
    payload = {"base": "goblin", "party_level": level, "party_size": size}
    with TestClient(app) as client:
        res = client.post("/encounter/build", json=payload)
        assert res.status_code == 200
        return res.json()


def test_scaling() -> None:
    enc1 = build(1, 2)
    assert len(enc1["monsters"]) == 2
    enc3 = build(3, 2)
    assert len(enc3["monsters"]) == 3
    enc5 = build(5, 2)
    assert len(enc5["monsters"]) == 3
    assert enc5["monsters"][-1]["name"].lower() == "goblin boss"
