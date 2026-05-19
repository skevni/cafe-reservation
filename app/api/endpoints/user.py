from fastapi import APIRouter, Body, Depends, HTTPException, Response
from fastapi_users import BaseUserManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import auth_backend, fastapi_users, get_user_manager
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.post(
    '/auth/jwt/login',
    summary='Получение токена авторизации',
    description='Возвращает токен для последующей авторизации пользователя.',
    tags=['Аутентификация'],
    response_description='Успешная аутентификация',
    responses={
        200: {
            'description': 'Токен успешно получен',
            'content': {
                'application/json': {
                    'example': {
                        'access_token': (
                            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx'
                        ),
                        'token_type': 'bearer'
                    }
                }
            }
        },
        400: {'description': 'Неверные учётные данные'},
        401: {'description': 'Ошибка аутентификации'}
    }
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
        raise HTTPException(status_code=400, detail='Неверные учётные данные')

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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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