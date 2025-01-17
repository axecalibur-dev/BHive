import re
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession


class UserProfileRequestDto(BaseModel):
    user_id: UUID = Field(..., description="The ID of the user must be a valid UUID")


class BuyMutualFundsRequestDto(BaseModel):
    ISIN: str = Field(..., description="The ISIN of the mutual fund unit.")
    no_of_units: int = Field(..., description="The amount of funds required to buy a fund.")
