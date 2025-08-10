from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.models.schemas import Adventure, Scene

router = APIRouter()

ADVENTURE_PATH = (
    Path(__file__).resolve().parent.parent / "seed" / "sample_adventure.json"
)
ADVENTURE = Adventure.model_validate_json(ADVENTURE_PATH.read_text())


@router.get("/scene/{scene_id}", response_model=Scene)
def get_scene(scene_id: int) -> Scene:
    for chapter in ADVENTURE.chapters:
        for scene in chapter.scenes:
            if scene.id == scene_id:
                return scene
    raise HTTPException(status_code=404, detail="Scene not found")
