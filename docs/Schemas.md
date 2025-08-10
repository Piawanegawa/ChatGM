# Schemas

Die Anwendung verwendet folgende Pydantic-Modelle:

- `Adventure`
- `Chapter`
- `Scene`
- `Check`
- `Encounter`
- `Party`
- `StateUpdate` / `StateUpdateRequest`
- `LLMOutput` (Co-DM Antwort)

## LLMOutput

```json
{
  "scene_id": 1,
  "narration": "...",
  "options": [
    {
      "prompt": "...",
      "check": {
        "skill": "perception",
        "dc": 12,
        "on_success": "...",
        "on_fail": "..."
      }
    }
  ],
  "combat_if_triggered": {
    "monsters": ["Goblin"],
    "tactics": "...",
    "terrain": "...",
    "scaling": "..."
  },
  "state_updates": []
}
```
