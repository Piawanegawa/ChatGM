from __future__ import annotations

from pathlib import Path
import logging

import pytest
from fastapi import HTTPException

from app.llm.templates import DEVELOPER_PROMPT, SYSTEM_PROMPT
from app.llm.validate import validate_with_retry

SAMPLES = Path("tests/golden_samples")


def test_validate_success() -> None:
    sample = SAMPLES.joinpath("compose_scene_valid.json").read_text()

    def llm_stub(_: list[dict]) -> str:
        return sample

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "developer", "content": DEVELOPER_PROMPT},
    ]
    result = validate_with_retry(llm_stub, messages)
    assert result.scene_id == 1


def test_validate_retry(caplog) -> None:
    caplog.set_level(logging.INFO)
    responses = [
        SAMPLES.joinpath("compose_scene_missing_field.json").read_text(),
        SAMPLES.joinpath("compose_scene_valid.json").read_text(),
    ]

    def llm_stub(_: list[dict]) -> str:
        return responses.pop(0)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    result = validate_with_retry(llm_stub, messages)
    assert result.narration
    assert any("invalid on attempt 1" in r.message for r in caplog.records)


def test_validate_fail_after_retries() -> None:
    sample = SAMPLES.joinpath("compose_scene_missing_field.json").read_text()

    def llm_stub(_: list[dict]) -> str:
        return sample

    with pytest.raises(HTTPException):
        validate_with_retry(llm_stub, [])
