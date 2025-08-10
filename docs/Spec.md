# Projekt-Spezifikation

- Python-Projekt mit FastAPI, Pydantic, SQLModel/SQLite
- Grund-Schemas für Adventure/Chapter/Scene/Checks/Encounter/State
- Basis-Routen: `GET /health`, `GET /scene/{id}`, `POST /state/apply`
- Tests (pytest) inkl. JSON-Schema-Validierung
- Ruff/Black, pre-commit, GitHub Actions (CI: lint+tests)
- Minimaler Seed: 1 Beispiel-Abenteuer mit 1 Szene

Akzeptanzkriterien:

- `uvicorn app.main:app` startet
- `GET /health` liefert `{ "ok": true }`
- `GET /scene/{id}` gibt Szene aus `sample_adventure.json` zurück
- `POST /state/apply` akzeptiert Updates und persistiert
- `pytest` grün in CI, Ruff/Black sauber
