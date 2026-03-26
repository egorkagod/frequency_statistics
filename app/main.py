from fastapi import FastAPI

from app.public import router as public_router

app = FastAPI()
app.include_router(public_router)