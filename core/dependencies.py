import base64
import os
from typing import Union

import jwt
from fastapi import Cookie, HTTPException
from starlette import status


async def check_http_cookies(session_state: Union[str, None] = Cookie(None)):
    if session_state is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized...",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif session_state == 'deleted':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized...",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        options = {
            'verify_signature': False,
            'verify_exp': False,  # Skipping expiration date check
            'verify_aud': False
        }
        decoded_jwt_result = jwt.decode(jwt=session_state.encode("utf-8"), key=os.getenv("JWT_KEY"), algorithms=["HS512"],
                                        options=options)
        decoded_ext_id = base64.b64decode(decoded_jwt_result.get("sub")).decode('utf-8')
        return {
            "session_token": session_state,
            "user_id": decoded_ext_id,
            "access_token": base64.b64decode(decoded_jwt_result.get("access_token")).decode('utf-8'),
        }

