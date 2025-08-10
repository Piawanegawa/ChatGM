from fastapi import APIRouter

from app.rules.suggest_checks import suggest_checks

router = APIRouter()


@router.post("/rules/checks")
def post_checks(payload: dict) -> dict:
    scene = payload.get("scene", {})
    party = payload.get("party", {})
    checks = suggest_checks(scene, party)
    return {"checks": checks}
