from fastapi import FastAPI
from app.api.v1.auth import router as auth_router

app = FastAPI(title="TaskForge API")

app.include_router(auth_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to TaskForge API!"}