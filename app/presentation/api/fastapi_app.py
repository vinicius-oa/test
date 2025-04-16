from fastapi import FastAPI

from infrastructure.config.settings import get_settings
from presentation.api.endpoints import router


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(title=settings.app_name)

    app.include_router(router, prefix="/api")

    return app
