from fastapi import APIRouter, Body, Depends, Response
from fastapi_users import BaseUserManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.responses.login_responses import (
    LOGIN_INVALID_RESPONSE, LOGIN_RESPONSES
)
from app.exceptions.custom_error import CustomError
from app.core.db import get_async_session
from app.core.user import auth_backend, fastapi_users, get_user_manager
from app.models.user import User
from app.schemas.auth import AuthToken, LoginRequest
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.post(
    '/auth/login',
    response_model=AuthToken,
    summary='Получение токена авторизации',
    description='Возвращает токен для последующей авторизации пользователя.',
    tags=['Аутентификация'],
    responses={**LOGIN_RESPONSES, }
)
async def login(
    response: Response,
    body: LoginRequest = Body(
        ...,  # обязательное тело
        description='Учётные данные пользователя для входа'
    ),
):
    """
    Кастомный логин через email/телефон + пароль.
    """
    credentials = {
        'username': body.login,
        'password': body.password
    }

    # Используем стандартный механизм fastapi-users
    try:
        token = await auth_backend.login(response, credentials)
        return token
    except Exception:
        raise CustomError(
            code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            message=LOGIN_INVALID_RESPONSE['description']
        )

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    route for route in users_router.routes if route.name != 'users:delete_user'
]
router.include_router(
    users_router,
    prefix='/users',
    tags=['Пользователи'],
)


@router.post('/users', response_model=UserRead, tags=['Пользователи'])
async def create_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(fastapi_users.current_user(superuser=True)),
    manager: BaseUserManager[User, int] = Depends(get_user_manager),
):
    """
    Создание пользователя (только для суперпользователей).
    """
    try:
        created_user = await manager.create(user_create, safe=False)
        return created_user
    except Exception:
        raise CustomError(
            code=status.HTTP_400_BAD_REQUEST,
            message='Ошибка в параметрах запроса'
        )


@router.get('/users', response_model=list[UserRead], tags=['Пользователи'])
async def list_users(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(fastapi_users.current_user(superuser=True)),
):
    """
    Получение списка всех пользователей (только для суперпользователей).
    """
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users