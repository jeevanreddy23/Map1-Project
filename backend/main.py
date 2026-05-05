from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import init_db
from app.api.features import router as features_router
from app.api.export import router as export_router

app = FastAPI(title="AutoSoil Logger Map1 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(features_router, prefix="/api/features", tags=["Features"])
app.include_router(export_router, prefix="/api", tags=["Export"])

@app.get("/")
def read_root():
    return {"message": "Map1 API running.", "docs": "/docs"}