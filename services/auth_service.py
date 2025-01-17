import os
from typing import Optional
from urllib.request import Request

import bcrypt  # Importing bcrypt for password hashing
from datetime import datetime, timedelta
import jwt
from fastapi import Header, HTTPException, Depends
from fastapi import FastAPI, HTTPException, status


class AuthServices:

    @classmethod
    def decode_access_token(cls,token: str):
        try:
            payload = jwt.decode(token, os.getenv("SECRET_SIGNING_KEY"), algorithms=os.getenv("SECRET_SIGNING_KEY"))

            return payload
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    @classmethod
    async def perform_hashing(cls, password_string):
        return bcrypt.hashpw(password_string.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @classmethod
    async def generate_access_refresh_token(cls, signup_data):
        access_token_expiration = datetime.utcnow() + timedelta(days=7)  # Access token expires in 7 days
        refresh_token_expiration = datetime.utcnow() + timedelta(days=30)  # Refresh token expires in 30 days

        # Create access token
        access_payload = {
            "exp": access_token_expiration,
            "iat": datetime.utcnow(),
            "type": "access",
            "user_id": str(signup_data.id),
            "email": signup_data.email
        }
        access_token = jwt.encode(access_payload, os.getenv("SECRET_SIGNING_KEY"), algorithm="HS256")

        # Create refresh token
        refresh_payload = {
            "exp": refresh_token_expiration,
            "iat": datetime.utcnow(),
            "type": "refresh",
            "user_id": str(signup_data.id),
        }
        refresh_token = jwt.encode(refresh_payload, os.getenv("SECRET_SIGNING_KEY"), algorithm="HS256")

        return access_token,refresh_token

    # middleware for auth
