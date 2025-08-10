from __future__ import annotations

from typing import Callable

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.llm.output_schema import LLMOutput
from app.llm.templates import DEVELOPER_PROMPT, SYSTEM_PROMPT, user_prompt
from app.llm.validate import validate_with_retry
from app.models.schemas import Party
from app.routes.scene import get_scene
from app.rules.suggest_checks import suggest_checks
from app.srd.lookup import lookup

router = APIRouter()


def default_llm(_: list[dict]) -> str:
    """Placeholder LLM implementation."""
    return "{}"


def get_llm() -> Callable[[list[dict]], str]:
    return default_llm


class ComposeRequest(BaseModel):
    scene_id: int
    party: Party


@router.post("/llm/compose_scene", response_model=LLMOutput)
def compose_scene(
    req: ComposeRequest, llm: Callable[[list[dict]], str] = Depends(get_llm)
) -> LLMOutput:
    scene = get_scene(req.scene_id)
    checks = suggest_checks(scene.model_dump(), req.party.model_dump())
    monster = lookup("SRD.goblin")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "developer", "content": DEVELOPER_PROMPT},
        {"role": "user", "content": user_prompt(scene, checks, monster)},
    ]
    return validate_with_retry(llm, messages)
