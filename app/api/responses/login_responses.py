from starlette import status

from app.schemas.auth import AuthToken
from app.schemas.custom_error import CustomError

LOGIN_INVALID_RESPONSE = {
    'description': 'Неверные имя пользователя и пароль',
    'content': {
        'application/json': {
            'schema': CustomError.model_json_schema(),
            'example': {
                'code': 0,
                'message': 'string'
            }
        }
    }
}

LOGIN_OK_RESPONSE = {
    'description': 'Успешно',
    'content': {
        'application/json': {
            'schema': AuthToken.model_json_schema(),
            'example': {
                'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx',
                'token_type': 'bearer'
            }
        }
    }
}

LOGIN_RESPONSES = {
    status.HTTP_200_OK: LOGIN_OK_RESPONSE,
    status.HTTP_422_UNPROCESSABLE_CONTENT: LOGIN_INVALID_RESPONSE,
}
