import json
from pathlib import Path

from jsonschema import validate

from app.models.schemas import Adventure


def test_sample_adventure_matches_schema() -> None:
    data = json.loads(Path("app/seed/sample_adventure.json").read_text())
    schema = Adventure.model_json_schema()
    validate(instance=data, schema=schema)
