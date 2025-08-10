from __future__ import annotations

from typing import Any, Dict, List

from app.srd.lookup import lookup


def build_encounter(req: Dict[str, Any]) -> Dict[str, Any]:
    base_name: str = req.get("base", "goblin")
    party_level: int = int(req.get("party_level", 1))
    party_size: int = int(req.get("party_size", 1))
    terrain: str | None = req.get("terrain")

    base_ref = f"SRD.{base_name}"
    base_stat = lookup(base_ref)

    monsters: List[Dict[str, Any]] = []
    for _ in range(party_size):
        monsters.append(base_stat)

    if party_level >= 3:
        monsters.append(base_stat)

    if party_level >= 5:
        boss_ref = f"SRD.{base_name}_boss"
        try:
            boss_stat = lookup(boss_ref)
            monsters[-1] = boss_stat
        except KeyError:
            pass

    encounter: Dict[str, Any] = {"monsters": monsters}
    if terrain:
        encounter["terrain"] = terrain
    return encounter
