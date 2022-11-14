from fastapi import APIRouter, Depends
from pydantic import typing

from core.dependencies import check_http_cookies
from core.httpx_processor import fetch_current_user_from_back_end

router = APIRouter(
    prefix="/private",
    tags=["account"],
    # dependencies=[Depends(check_http_cookies)],
    responses={404: {"description": "Not found"}},
)


# Auth Flow

@router.get("/account", tags=["account"])
async def account(user_data: typing.Any = Depends(check_http_cookies)):
    return await fetch_current_user_from_back_end(access_token=user_data.get("access_token"))
