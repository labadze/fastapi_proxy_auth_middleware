from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import Response

from core.ipd_config import idp

router = APIRouter(
    prefix="/public",
    tags=["auth-flow"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


# Auth Flow

@router.get("/login-link", tags=["auth-flow"])
def login_redirect(response: Response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, PATCH, GET, DELETE, OPTIONS'
    return jsonable_encoder({
        "login_url": idp.login_uri
    })


@router.get("/callback", tags=["auth-flow"])
def callback(session_state: str, code: str, response: Response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000/callback'
    response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, PATCH, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Origin, Accept'
    exchange_result = idp.exchange_authorization_code(session_state=session_state, code=code)
    print(exchange_result)
    if exchange_result is not None:
        response.status_code = status.HTTP_201_CREATED
        token = "PROXY_ACCESS_TOKEN"
        response.set_cookie(
            "Authorization",
            value=f"Bearer {token}",
            httponly=True,
            secure=True,
            samesite="none",
            max_age=1800,
            expires=1800,
        )
        return {
            "success": True
        }


@router.get("/logout", tags=["auth-flow"])
def logout():
    return idp.logout_uri
