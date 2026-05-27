from fastapi import FastAPI
from app.models.user import User, UserRole

app = FastAPI(title="TaskForge API")


@app.get("/")
async def root():
    return {"message": "Welcome to TaskForge API!"}