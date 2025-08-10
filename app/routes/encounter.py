from fastapi import APIRouter

from app.rules.encounter import build_encounter

router = APIRouter()


@router.post("/encounter/build")
def post_encounter(payload: dict) -> dict:
    return build_encounter(payload)
