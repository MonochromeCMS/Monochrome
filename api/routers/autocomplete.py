from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import is_connected, auth_responses
from ..db import get_db
from ..models.chapter import Chapter


router = APIRouter(prefix="/autocomplete", tags=["Autocomplete"], dependencies=[Depends(is_connected)])


get_responses = {
    **auth_responses,
    200: {
        "description": "A list of scan groups",
        "model": List[str],
    },
}


@router.get("/groups", response_model=List[str], responses=get_responses)
async def get_scan_groups(
    db_session: AsyncSession = Depends(get_db),
):
    groups = await Chapter.get_groups(db_session)
    if "no group" not in groups:
        groups.append("no group")
    return groups
