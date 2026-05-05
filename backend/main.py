from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import init_db
from app.api.features import router as features_router

app = FastAPI(title="AutoSoil Logger Map1 API")

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

@app.get("/")
def read_root():
    return {"message": "Map1 Backend is running."}