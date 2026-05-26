from fastapi import FastAPI

app = FastAPI(title="TaskForge API")


@app.get("/")
async def root():
    return {"message": "Welcome to TaskForge API!"}