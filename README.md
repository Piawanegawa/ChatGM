# ChatGM

Backend-Prototyp für ein textbasiertes Abenteuer-Spiel auf Basis von FastAPI.

## Setup

```bash
pip install uv
uv venv
source .venv/bin/activate
uv pip install -e .[dev]
pre-commit install
```

## Entwicklung

Server starten:

```bash
uv run uvicorn app.main:app --reload
```

Gesundheitscheck:

```bash
curl http://localhost:8000/health
# {"ok": true}
```

Szene abrufen:

```bash
curl http://localhost:8000/scene/1
```

Szene komponieren (Mock-LLM):

```bash
curl -X POST http://localhost:8000/llm/compose_scene \
  -H 'Content-Type: application/json' \
  -d '{"scene_id": 1, "party": {"members": ["A"]}}'
# {
#   "scene_id": 1,
#   "narration": "Die Helden betreten eine dunkle Höhle.",
#   "options": [{"prompt": "Nach Fallen suchen", "check": {"skill": "perception", "dc": 12, "on_success": "Du findest eine Falle.", "on_fail": "Du löst eine Falle aus."}}],
#   "combat_if_triggered": {"monsters": ["Goblin"], "tactics": "Hinterhalt aus dem Schatten", "terrain": "Höhle", "scaling": "medium"},
#   "state_updates": []
# }
```

State-Update:

```bash
curl -X POST http://localhost:8000/state/apply \
  -H 'Content-Type: application/json' \
  -d '{"updates": [{"op": "set", "key": "foo", "value": 1}]}'
# {"ok": true}
```

## Encounter-Heuristik

- Ein Gegner pro Gruppenmitglied als Basis.
- Ab Durchschnittslevel >=3 erscheint ein zusätzlicher Mob.
- Ab Level >=5 (falls verfügbar) wird der letzte Gegner durch eine Boss-Variante ersetzt.
- Optional kann Terrain für den Encounter angegeben werden.

## Tests

```bash
uv run pytest
```

## SRD

Monsterstatblocks stammen aus dem *System Reference Document 5.1* von Wizards of the Coast
und stehen unter der [Creative Commons Attribution 4.0 International Lizenz](https://creativecommons.org/licenses/by/4.0/).
