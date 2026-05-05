from fastapi import FastAPI
from app.core.db import init_db

app = FastAPI(title="AutoSoil Logger Map1 API")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Map1 Backend is running."}