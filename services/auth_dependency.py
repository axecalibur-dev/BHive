import os
import jwt
from fastapi import HTTPException, status, Header
from typing import Dict


def check_authorization(authorization: str = Header(None)) -> Dict[str, str]:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing inside header.",
        )

    try:
        token = authorization
        secret_key = os.getenv('SECRET_SIGNING_KEY')

        payload = jwt.decode(token, secret_key, algorithms=["HS256"])

        email = payload.get("email")
        user_id = payload.get("user_id")

        if not all([email, user_id]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token data",
            )

        return {"email": email, "user_id": user_id}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
