from __future__ import annotations

from pydantic import BaseModel, Field

from app.models.schemas import StateUpdate


class CheckSpec(BaseModel):
    skill: str
    dc: int
    on_success: str
    on_fail: str


class Option(BaseModel):
    prompt: str
    check: CheckSpec


class CombatInfo(BaseModel):
    monsters: list[str]
    tactics: str
    terrain: str
    scaling: str


class LLMOutput(BaseModel):
    scene_id: int
    narration: str
    options: list[Option]
    combat_if_triggered: CombatInfo | None = Field(default=None)
    state_updates: list[StateUpdate] = Field(default_factory=list)
