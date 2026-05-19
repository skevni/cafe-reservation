from fastapi import APIRouter

from app.api.endpoints import (
    user_router, tech_spec_router
)

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(
    tech_spec_router, prefix='/tech_spec', tags=['Technical Specification']
)
