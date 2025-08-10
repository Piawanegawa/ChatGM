from fastapi import APIRouter

from app.models.schemas import StateUpdateRequest
from app.state.db import set_state

router = APIRouter()


@router.post("/state/apply")
def apply_state(req: StateUpdateRequest) -> dict[str, bool]:
    for update in req.updates:
        if update.op == "set":
            set_state(update.key, update.value)
    return {"ok": True}
