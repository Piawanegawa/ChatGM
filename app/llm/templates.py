from __future__ import annotations

from app.models.schemas import Scene

SYSTEM_PROMPT = (
    "Du bist ein Co-Dungeon-Master. Improvisiere nur innerhalb der aktuellen "
    "Szene. Biete Vorschläge an, triff keine Entscheidungen."
)

DEVELOPER_PROMPT = (
    "Liefere ausschließlich valides JSON entsprechend dem vorgegebenen Schema."
)


def user_prompt(scene: Scene, checks: list[dict], monster: dict) -> str:
    """Build the user prompt for the LLM."""
    lines = [
        f"Szene: {scene.title}",
    ]
    if scene.description:
        lines.append(scene.description)
    if checks:
        lines.append("Vorgeschlagene Checks:")
        for c in checks:
            lines.append(f"- {c['reason']} (Skill: {c['skill']}, DC {c['dc']})")
    if monster:
        lines.append(f"Möglicher Gegner: {monster.get('name')} - {monster.get('type')}")
    return "\n".join(lines)
