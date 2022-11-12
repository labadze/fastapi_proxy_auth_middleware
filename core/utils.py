"""
 Generate Access token to set as HTTP-Only Cookies
"""
import base64
import datetime
import os

import jwt

from core.schemas import JWTProperties


async def sign_jwt(properties: JWTProperties):
    return jwt.encode(payload={
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=properties.expires_in),
        "nbf": datetime.datetime.now(tz=datetime.timezone.utc),
        "iss": os.getenv("JWT_ISSUER"),
        "sub": base64.b64encode(properties.user_id.encode('utf-8')).decode("utf-8"),
        "aud": base64.b64encode(properties.audience.encode('utf-8')).decode("utf-8"),
        "iat": datetime.datetime.now(tz=datetime.timezone.utc),
        "u_identifier": properties.user_id,
        "user_role": properties.user_role,
    },
        key=os.getenv("JWT_KEY"),
        algorithm="HS512",
        headers={"kid": os.environ.get("JWT_KID")},
    )