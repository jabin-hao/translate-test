from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import APP_TITLE, APP_VERSION
from app.translator import load_models
from app.routes.translate import router as translate_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_models()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title=APP_TITLE, version=APP_VERSION, lifespan=lifespan)
    app.include_router(translate_router)
    return app
