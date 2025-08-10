from __future__ import annotations

from typing import Any, Dict, List

DC_BASE = {"easy": 10, "moderate": 15, "hard": 20}


def _clamp_dc(dc: int) -> int:
    """Clamp DC into allowed range of 5-30."""
    return max(5, min(30, dc))


def _apply_party_modifier(dc: int, party: Dict[str, Any]) -> int:
    members = party.get("members", [])
    modifier = len(members) - 3
    if modifier > 5:
        modifier = 5
    if modifier < -5:
        modifier = -5
    return _clamp_dc(dc + modifier)


def dc_for(difficulty: str, party: Dict[str, Any]) -> int:
    base = DC_BASE[difficulty]
    return _apply_party_modifier(base, party)


def suggest_checks(
    scene: Dict[str, Any], party: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Suggest 2-4 ability checks for a scene."""
    suggestions: List[Dict[str, Any]] = []
    desc = (scene.get("description") or "").lower()

    if "locked" in desc or "lock" in desc:
        suggestions.append(
            {
                "skill": "thieves_tools",
                "dc": dc_for("moderate", party),
                "reason": "Ein Schloss blockiert den Weg",
                "on_success": "Das Schloss öffnet sich",
                "on_fail": "Das Schloss bleibt verschlossen",
            }
        )

    if "dark" in desc:
        suggestions.append(
            {
                "skill": "perception",
                "dc": dc_for("easy", party),
                "reason": "Es ist dunkel",
                "on_success": "Du erkennst mehr Details",
                "on_fail": "Du über siehst etwas Wichtiges",
            }
        )

    if "climb" in desc or "wall" in desc:
        suggestions.append(
            {
                "skill": "athletics",
                "dc": dc_for("hard", party),
                "reason": "Eine Wand muss erklettert werden",
                "on_success": "Du erreichst den oberen Rand",
                "on_fail": "Du fällst herunter",
            }
        )

    if not suggestions:
        suggestions.append(
            {
                "skill": "perception",
                "dc": dc_for("moderate", party),
                "reason": "Allgemeine Umsicht",
                "on_success": "Du findest nützliche Hinweise",
                "on_fail": "Du bemerkst nichts Besonderes",
            }
        )

    if len(suggestions) == 1:
        suggestions.append(
            {
                "skill": "survival",
                "dc": dc_for("easy", party),
                "reason": "Orientierung in der Umgebung",
                "on_success": "Du findest den besten Pfad",
                "on_fail": "Du verirrst dich kurz",
            }
        )

    return suggestions[:4]
