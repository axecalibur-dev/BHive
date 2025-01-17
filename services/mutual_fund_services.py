import os

from Pydantic.secure.request_dto import BuyMutualFundsRequestDto
import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from Pydantic.secure.response_dto import GetAllSchemesResponseDto


class MutualFundServices:
    @classmethod
    async def get_all_schemes_service(cls):

        url = "https://" + os.getenv("RAPID_API_URL") + "/latest"
        headers = {
            "x-rapidapi-host": os.getenv("RAPID_API_URL"),
            "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
            "Content-Type": "application/json"
        }
        print("STDOUT:", flush=True)
        print(url, flush=True)
        print("STDOUT:", flush=True)
        # query params from request
        params = {"Scheme_Type": "Open"}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=params)

            # return response.json()
                if response.status_code == 200:
                    data = response.json()
                    scheme_objects = []

                    for item in data:
                        # print("STDOUT:", flush=True)
                        # print(item, flush=True)
                        # print("STDOUT:", flush=True)
                        scheme_object = GetAllSchemesResponseDto(**item)
                        scheme_objects.append(scheme_object)

                    return scheme_objects

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error occurred: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Request error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    @classmethod
    async def get_schemas_fund_family(cls,fund_family_name:str):
        # query params from request
        params = {"Scheme_Type": "Open", "Mutual_Fund_Family": fund_family_name}
        url = "https://" + os.getenv("RAPID_API_URL") + "/latest"
        headers = {
            "x-rapidapi-host": os.getenv("RAPID_API_URL"),
            "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=params)
                print(response.status_code)
                print(response.json())
                print(response.status_code)
                response.raise_for_status()

                if response.status_code == 200:
                    data = response.json()
                    if len(data) == 0:
                        return []

                    scheme_objects = []
                    for item in data:
                        scheme_object = GetAllSchemesResponseDto(**item)

                    return scheme_object

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error occurred: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Request error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )


    @classmethod
    async def buy_mutual_funds_units(cls, purchase_data: BuyMutualFundsRequestDto, db: AsyncSession,authorization:Any):
        # query params from request

        # isin number can be used to uniquely identify a mutual fund.
        params = {"ISIN": purchase_data.ISIN}
        url = "https://" + os.getenv("RAPID_API_URL") + "/master"
        headers = {
            "x-rapidapi-host": os.getenv("RAPID_API_URL"),
            "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=params)
                print("S<<TDOUT:", flush=True)
                print(response.json(), flush=True)
                print("STDO<<UT:", flush=True)
                response.raise_for_status()

                if response.status_code == 200:
                    json_response = response.json()

                    if len(json_response) == 0:
                        raise HTTPException(
                            status_code=400,
                            detail=f"No mutual funds for {purchase_data.ISIN}."
                        )

                    for fund in json_response:

                        #check if this mutual fund is open for acquiring
                        if fund["Purchase_Allowed"] is True:
                            if purchase_data.no_of_units > fund["Minimum_Purchase_Amount"]:
                                #register in db
                                return purchase_data.no_of_units , purchase_data.ISIN , fund["AMC_Code"] , fund["Scheme_Name"]
                            else:
                                raise HTTPException(
                                    status_code=400,
                                    detail=f"Purchase amount is too low. Minimum amount is {fund['Minimum_Purchase_Amount']}."
                                )

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error occurred: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Request error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
