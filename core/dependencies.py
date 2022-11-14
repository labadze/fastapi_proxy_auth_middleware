import base64
import os
from typing import Union

import jwt
from fastapi import Cookie, HTTPException
from starlette import status

from db.db_ops import fetch_authorization_artefact_by_ext_id


async def check_http_cookies(session_key: Union[str, None] = Cookie(None)):
    print(session_key)
    if session_key is None:
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
        decoded_jwt_result = jwt.decode(jwt=session_key.encode("utf-8"), key=os.getenv("JWT_KEY"), algorithms=["HS512"],
                                        options=options)
        decoded_ext_id = base64.b64decode(decoded_jwt_result.get("sub")).decode('utf-8')
        storage_result = await fetch_authorization_artefact_by_ext_id(ext_id=decoded_ext_id,
                                                                      session_token=session_key)
        if storage_result is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif storage_result.is_destroyed is True:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            return {
                "user_id": storage_result.user_id,
                "access_token": storage_result.access_token,
            }
