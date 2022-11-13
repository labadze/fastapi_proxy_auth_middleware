import base64
from typing import Union

from fastapi import APIRouter, Header
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import Response, JSONResponse

from core.httpx_processor import end_session
from core.ipd_config import idp
from core.schemas import JWTProperties
from core.utils import sign_jwt, decode_back_end_token

router = APIRouter(
    prefix="/public",
    tags=["auth-flow"],
    # dependencies=[Depends(get_token_header)],
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
        print(exchange_result)
        # TODO decode token at back-end
        # Store token in database
        # Generate session token with inserted id
        # Update value in database
        await decode_back_end_token(encoded=str(exchange_result).replace("Bearer ", ""))

        if exchange_result is not None:
            response.status_code = status.HTTP_201_CREATED
            jwt_props = JWTProperties(
                user_id="uno",
                user_role="root",
                audience="user",
                expires_in=60 * 8
            )
            token = await sign_jwt(properties=jwt_props)
            response = JSONResponse(content={
                "success": True
            })
            response.set_cookie(
                key="session_key",
                value=token,
                httponly=True,
                secure=True,
                samesite="none",
                max_age=1800,
                expires=1800,
                path='/',
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
async def delete_cookie(response: Response, keycloak_log_out_encoded_uri: Union[str, None] = Header(default=None)):
    response.delete_cookie(key="session_key", path='/', domain=None)
    response = JSONResponse(content={
        "success": True
    })
    await end_session(logout_url=base64.b64encode(keycloak_log_out_encoded_uri.encode('utf-8')).decode("utf-8"))
    return response


@router.get("/log_out", tags=["auth-flow"])
def logout():
    # urllib.parse.quote("Müller".encode('utf8'))
    return {
        "log_out_url": idp.logout_uri
    }
