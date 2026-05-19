from pydantic import BaseModel


class CustomError(BaseModel):
    code: int
    message: str
