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
