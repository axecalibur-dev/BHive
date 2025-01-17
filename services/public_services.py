# public_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from database.models import User
import bcrypt  # Importing bcrypt for password hashing

from services.auth_service import AuthServices
from dotenv import load_dotenv

# Load environment variables before the test
load_dotenv()

class PublicService:

    @classmethod
    async def signup_user(cls, signup_data, db: AsyncSession):
        print("RES", flush=True)
        print(db.is_active, flush=True)
        print("RES", flush=True)
        # try:
        result = await db.execute(select(User).filter_by(email=signup_data.email))
        # except Exception as e:
            # print(e)
        user_exists = result.scalar()
        if user_exists:
            raise ValueError("Email already registered")
        hashed_pwd = await AuthServices.perform_hashing(signup_data.password)
        new_user = User(
            email=signup_data.email,
            password=hashed_pwd
        )

        try:
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            access_token,refresh_token = await AuthServices.generate_access_refresh_token(signup_data=new_user)
        except IntegrityError as e:
            raise ValueError("Error saving user to the database.")

        return new_user,access_token,refresh_token

    @classmethod
    async def login_user(cls, signup_data, db: AsyncSession):
        # Query the user by email
        result = await db.execute(select(User).filter(User.email == signup_data.email))
        user = result.scalar()

        # If no user is found, raise an exception
        if not user:
            raise ValueError("No user found with this email")

        # Compare the password with the stored hashed password using bcrypt
        if not bcrypt.checkpw(signup_data.password.encode('utf-8'), user.password.encode('utf-8')):
            raise ValueError("Incorrect password")

        # Generate access and refresh tokens (JWT)
        access_token,refresh_token = await AuthServices.generate_access_refresh_token(signup_data=user)

        # You may want to return the user and tokens
        return user, access_token, refresh_token
