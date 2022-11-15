import datetime
from typing import Union

from fastapi import APIRouter, Header, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import typing
from starlette import status
from starlette.responses import Response, JSONResponse

from core.dependencies import check_http_cookies
from core.httpx_processor import fetch_current_user_from_back_end
from core.ipd_config import idp
from core.schemas import JWTProperties
from core.utils import sign_jwt

router = APIRouter(
    prefix="/public",
    tags=["auth-flow"],
    responses={404: {"description": "Not found"}},
)


# Auth Flow

@router.get("/login_link", tags=["auth-flow"])
def login_redirect():
    try:
        login_url = idp.login_uri
        return jsonable_encoder({
            "login_url": login_url
        })
    except Exception as e:
        print(e)


@router.get("/callback", tags=["auth-flow"])
async def callback(session_state: str, code: str, response: Response):
    try:
        exchange_result = idp.exchange_authorization_code(session_state=session_state, code=code)
        current_user_result = await fetch_current_user_from_back_end(
            access_token=str(exchange_result).replace("Bearer ", ""))
        response.status_code = status.HTTP_201_CREATED
        response = JSONResponse(content={
            "success": True,
            "data": current_user_result
        })
        jwt_props = JWTProperties(
            user_id=current_user_result.get("ext_id"),
            user_role=str(current_user_result.get("roles")),
            audience="user",
            expires_in=60 * 8,
            access_token=str(exchange_result).replace("Bearer ", "")
        )
        # Generate session token with inserted id
        token = await sign_jwt(properties=jwt_props)
        response.set_cookie(
            key="session_state",
            value=token,
            httponly=True,
            secure=True,
            samesite='none',
            max_age=1800,
            expires=1800,
            # path='/',
            domain=None
        )
        return response
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "success": False,
            "error": e,
        }


@router.delete("/delete_cookie", tags=["auth-flow"])
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
        samesite="none",
        max_age=4,
        expires=3,
        path='/',
        domain=None
    )
    # await end_session(logout_url=base64.b64encode(keycloak_log_out_encoded_uri.encode('utf-8')).decode("utf-8"))
    return response


@router.get("/log_out", tags=["auth-flow"])
def logout():
    # urllib.parse.quote("Müller".encode('utf8'))
    return {
        "log_out_url": idp.logout_uri
    }
