from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Path, Query
from fastapi import FastAPI, Depends, HTTPException

from Pydantic.public.response_dto import SignUpResponseDto
from Pydantic.secure.request_dto import UserProfileRequestDto, BuyMutualFundsRequestDto
from database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from Pydantic.public.request_dto import SignUpRequestDto, LoginRequestDto
from response_builder.builder import HttpResponse
from services.auth_dependency import check_authorization
from services.auth_service import AuthServices
from services.mutual_fund_services import MutualFundServices
from services.public_services import PublicService

router = APIRouter()

@router.get("/secure/fund-family-houses")
async def get_fund_family_houses(db: AsyncSession = Depends(get_db), authorization: dict = Depends(check_authorization)):
    try:
        get_fund_family_data = await MutualFundServices.get_all_schemes_service()
        print("STDOUT:", flush=True)
        print(get_fund_family_data, flush=True)
        print("STDOUT:", flush=True)
        return HttpResponse(
            status_code=200,
            status="Success",
            message="Data found.",
            data=get_fund_family_data
        )
    except Exception as e:
        return HttpResponse(
            status_code=400,
            status="Failure",
            message=str(e),
            data={}
        )


@router.get("/secure/schemas-fund-family")
async def get_schemas_fund_family(
    db: AsyncSession = Depends(get_db),
    authorization: dict = Depends(check_authorization),
    fund_family_name: str = Query(..., alias="fund_family_name", description="Name of the fund family")
):
    try:
        get_schemas_fund_family_data = await MutualFundServices.get_schemas_fund_family(fund_family_name=fund_family_name)
        return HttpResponse(
            status_code=200,
            status="Success",
            message="Data found.",
            data=get_schemas_fund_family_data
        )
    except Exception as e:
        return HttpResponse(
            status_code=400,
            status="Failure",
            message=str(e),
            data={}
        )


@router.post("/secure/buy-funds")
async def acquire_mutual_funds_units(
    purchase_data: BuyMutualFundsRequestDto,
    db: AsyncSession = Depends(get_db),
    authorization: dict = Depends(check_authorization),
):
    try:
        # Call the business logic method
        no_of_units, ISIN, amc_code, scheme_name = await MutualFundServices.buy_mutual_funds_units(
            purchase_data=purchase_data,
            db=db,
            authorization=authorization
        )
        return HttpResponse(
            status_code=200,
            status="Success",
            message="Mutual funds acquired.",
            data={
                "Schema Name": scheme_name,
                "AMC_Code": amc_code,
                "ISIN": ISIN,
                "units_bought": no_of_units
            }
        )
    except HTTPException as http_exc:
        # Propagate HTTP exceptions as-is
        raise http_exc
    except Exception as e:
        # Handle other generic exceptions
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )