from __future__ import annotations

from __future__ import annotations

import json
from pathlib import Path

import logging

from fastapi.testclient import TestClient

from app.main import app
from app.routes.llm import get_llm

SAMPLES = Path("tests/golden_samples")


def override(llm_func):
    app.dependency_overrides[get_llm] = lambda: llm_func


def test_compose_scene_ok() -> None:
    sample = SAMPLES / "compose_scene_valid.json"

    def llm_stub(_: list[dict]) -> str:
        return sample.read_text()

    override(llm_stub)
    with TestClient(app) as client:
        res = client.post(
            "/llm/compose_scene", json={"scene_id": 1, "party": {"members": ["A"]}}
        )
    app.dependency_overrides.clear()
    assert res.status_code == 200
    assert res.json() == json.loads(sample.read_text())


def test_compose_scene_retry(caplog) -> None:
    caplog.set_level(logging.INFO)
    responses = [
        (SAMPLES / "compose_scene_missing_field.json").read_text(),
        (SAMPLES / "compose_scene_valid.json").read_text(),
    ]

    def llm_stub(_: list[dict]) -> str:
        return responses.pop(0)

    override(llm_stub)
    with TestClient(app) as client:
        res = client.post(
            "/llm/compose_scene", json={"scene_id": 1, "party": {"members": ["A"]}}
        )
    app.dependency_overrides.clear()
    assert res.status_code == 200
    assert res.json()["narration"]
    assert any("invalid on attempt 1" in r.message for r in caplog.records)


def test_compose_scene_fail() -> None:
    sample = (SAMPLES / "compose_scene_missing_field.json").read_text()

    def llm_stub(_: list[dict]) -> str:
        return sample

    override(llm_stub)
    with TestClient(app) as client:
        res = client.post(
            "/llm/compose_scene", json={"scene_id": 1, "party": {"members": ["A"]}}
        )
    app.dependency_overrides.clear()
    assert res.status_code == 422
