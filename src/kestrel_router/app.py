"""FastAPI service. Start: uvicorn kestrel_router.app:app --app-dir src"""
import os
from pathlib import Path
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from .model import Router

ROOT = Path(__file__).resolve().parents[2]
MODEL = Path(os.environ.get("ROUTER_MODEL", ROOT / "models" / "router.joblib"))
app = FastAPI(title="Kestrel service-request router", version="1.0")
router = Router(MODEL)


class Request(BaseModel):
    request_text: str = Field(..., min_length=1, examples=["water purifier leaking water from bottom"])
    product_family: Optional[str] = None
    warranty_status: Optional[str] = None
    channel: Optional[str] = None
    created_at_ist: Optional[str] = None
    source: Optional[str] = None
    request_id: Optional[str] = None


@app.post("/route")
def route(req: Request):
    return router.route(req.model_dump())


@app.get("/health")
def health():
    return {"ok": True, "model": MODEL.name, "needs_api_key": False}


@app.get("/")
def screen():
    return FileResponse(ROOT / "static" / "index.html")
