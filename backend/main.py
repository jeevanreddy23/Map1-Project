from fastapi import FastAPI

app = FastAPI(title="AutoSoil Logger Map1 API")

@app.get(/")
def read_root():
    return {"message": "Welcome to Map1 API"}
