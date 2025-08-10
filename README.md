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

## Tests

```bash
uv run pytest
```
