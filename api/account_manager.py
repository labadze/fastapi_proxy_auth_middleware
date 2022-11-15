import datetime
from typing import Union

from fastapi import APIRouter, Depends
from fastapi.params import Header
from pydantic import typing
from starlette.responses import Response, JSONResponse

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


@router.delete("/account/delete_cookie", tags=["auth-flow"])
async def delete_cookie(response: Response, user_data: typing.Any = Depends(check_http_cookies),
                        keycloak_log_out_encoded_uri: Union[str, None] = Header(default=None)):
    response = JSONResponse(content={
        "success": True
    })
    response.delete_cookie(key="session_key", path='/', domain=None)
    response.delete_cookie(key="session_key", domain=None)
    response.set_cookie(
        key="session_state",
        value='deleted',
        httponly=True,
        secure=True,
        samesite='none',
        max_age=1,
        expires=1,
        path='/',
        domain=None
    )
    # await end_session(logout_url=base64.b64encode(keycloak_log_out_encoded_uri.encode('utf-8')).decode("utf-8"))
    return response
