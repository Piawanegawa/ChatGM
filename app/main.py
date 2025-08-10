from fastapi import FastAPI

from app.routes.scene import router as scene_router
from app.routes.state import router as state_router
from app.state.db import init_db

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}


app.include_router(scene_router)
app.include_router(state_router)
