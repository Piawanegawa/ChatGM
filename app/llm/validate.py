from __future__ import annotations

import json
import logging
from typing import Callable, List, Dict

from fastapi import HTTPException
from jsonschema import ValidationError as JSONValidationError, validate as json_validate
from pydantic import ValidationError as PydanticValidationError

from .output_schema import LLMOutput


Message = Dict[str, str]


def validate_with_retry(
    llm: Callable[[List[Message]], str],
    messages: List[Message],
    max_retries: int = 2,
) -> LLMOutput:
    """Call the LLM and validate the JSON response."""
    schema = LLMOutput.model_json_schema()
    history = list(messages)
    for attempt in range(max_retries + 1):
        raw = llm(history)
        try:
            data = json.loads(raw)
            json_validate(data, schema)
            return LLMOutput.model_validate(data)
        except (
            json.JSONDecodeError,
            JSONValidationError,
            PydanticValidationError,
        ) as exc:
            logging.info("LLM output invalid on attempt %s: %s", attempt + 1, exc)
            if attempt >= max_retries:
                raise HTTPException(
                    status_code=422, detail="Invalid LLM output"
                ) from exc
            history.append({"role": "user", "content": f"Korrigiere das JSON: {exc}"})
    raise HTTPException(status_code=422, detail="Invalid LLM output")
