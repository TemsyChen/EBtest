from fastapi import FastAPI

application = app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hezzo Blurd"}