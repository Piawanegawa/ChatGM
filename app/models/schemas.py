from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class Check(BaseModel):
    id: int
    description: str


class Encounter(BaseModel):
    id: int
    description: str


class Scene(BaseModel):
    id: int
    title: str
    description: str | None = None
    encounters: list[Encounter] = []
    checks: list[Check] = []


class Chapter(BaseModel):
    id: int
    title: str
    scenes: list[Scene] = []


class Adventure(BaseModel):
    id: int
    title: str
    chapters: list[Chapter] = []


class Party(BaseModel):
    members: list[str]


class StateUpdate(BaseModel):
    op: Literal["set"]
    key: str
    value: Any


class StateUpdateRequest(BaseModel):
    updates: list[StateUpdate]
