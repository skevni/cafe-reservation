from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    docs_url='/api/v1/docs',
    redoc_url='/api/v1/redoc',
    servers=[
        {
            "url": "/api/v1",
            "description": "Локальный сервер"
        }
    ]
)

app.include_router(main_router)
