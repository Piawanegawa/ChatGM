from __future__ import annotations

import json
from typing import Any

from sqlmodel import Field, Session, SQLModel, create_engine

engine = create_engine("sqlite:///state.db", echo=False)


class State(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: str


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def set_state(key: str, value: Any) -> None:
    data = json.dumps(value)
    with Session(engine) as session:
        state = session.get(State, key)
        if state:
            state.value = data
        else:
            state = State(key=key, value=data)
            session.add(state)
        session.commit()


def get_state(key: str) -> Any:
    with Session(engine) as session:
        state = session.get(State, key)
        if state is None:
            return None
        return json.loads(state.value)
