from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Получение данных для последующей авторизации."""
    login: str = Field(
        ...,
        title='Login (email or phone)',
        description='Логин пользователя (email или телефон)',
        examples=['admin@example.com', '+79123456789']
    )
    password: str = Field(
        ...,
        description='Пароль пользователя',
        format="password",
    )

    model_config = {
        'json_schema_extra': {
            'example': {
                'login': 'admin@example.com',
                'password': '$ecRet123#'
            }
        }
    }