from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException

from Pydantic.public.response_dto import SignUpResponseDto
from database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from Pydantic.public.request_dto import SignUpRequestDto, LoginRequestDto
from response_builder.builder import HttpResponse
from services.public_services import PublicService

router = APIRouter()


@router.post("/public/signup")
async def perform_signup(signup_data: SignUpRequestDto, db: AsyncSession = Depends(get_db)):
    print("API:", flush=True)
    print(db, flush=True)
    print("API:", flush=True)
    try:
        new_user, access_token, refresh_token = await PublicService.signup_user(signup_data, db)
        return HttpResponse(
            status_code=200,
            status="Success",
            message="User created successfully",
            data=SignUpResponseDto(
                id=str(new_user.id),  # Convert UUID to string
                email=new_user.email,
                access_token=access_token,
                refresh_token=refresh_token
            ))

    except Exception as e:
        print("EX:", flush=True)
        print(str(e), flush=True)
        print("Ex:", flush=True)
        return HttpResponse(
            status_code=400,
            status="Failure",
            message=str(e),
            data={})


@router.post("/public/login")
async def perform_login(login_data: LoginRequestDto, db: AsyncSession = Depends(get_db)):
    try:
        new_user, access_token, refresh_token = await PublicService.login_user(login_data, db)
        return HttpResponse(
            status_code=201,
            status="Success",
            message="User logged in.",
            data=SignUpResponseDto(
                id=str(new_user.id),
                email=new_user.email,
                access_token=access_token,
                refresh_token=refresh_token
            ))

    except Exception as e:
        return HttpResponse(
            status_code=400,
            status="Failure",
            message=str(e),
            data={})
