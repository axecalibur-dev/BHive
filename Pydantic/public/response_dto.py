from pydantic import BaseModel


class SignUpResponseDto(BaseModel):
    id: str
    email: str
    access_token:str
    refresh_token:str

