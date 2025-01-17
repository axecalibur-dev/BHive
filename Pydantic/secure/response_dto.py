import re

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession


class GetAllSchemesResponseDto(BaseModel):
    Scheme_Name:str = Field(...,description="Name of the Scheme")
    Scheme_Code:int = Field(...,description="Name of the Scheme Code")
    Scheme_Category:str = Field(...,description="Name of the Category")
    Scheme_Type:str = Field(...,description="Type of scheme")
    Mutual_Fund_Family : str = Field(...,description="Mutual Fund Family Name")
    Net_Asset_Value:float = Field(...,description="NAV - Net Asset Value")
    Date : str = Field(...,description="Date")