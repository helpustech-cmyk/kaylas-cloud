import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import router
from app.telegram_bot import router as telegram_router

app = FastAPI(title="kaylas.cloud API", version="1.0.0")

origins = os.getenv("CORS_ORIGINS", "https://kaylas.cloud,https://www.kaylas.cloud,http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
app.include_router(telegram_router, prefix="/api/v1")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"status": "kaylas.cloud API v1"}
