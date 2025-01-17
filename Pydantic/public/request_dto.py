from pydantic import BaseModel, EmailStr, field_validator
import re


class SignUpRequestDto(BaseModel):
    email: EmailStr
    password: str

    # Validate 'password' to ensure it's between 6 and 20 characters
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 6 or len(v) > 20:
            raise ValueError('Password must be between 6 and 20 characters')
        return v


class LoginRequestDto(BaseModel):
    email: EmailStr
    password: str


    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 6 or len(v) > 20:
            raise ValueError('Password must be between 6 and 20 characters')
        return v
