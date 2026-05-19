from fastapi import HTTPException


class CustomError(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(
            status_code=code,
            detail={
                "code": code,
                "message": message
            }
        )
