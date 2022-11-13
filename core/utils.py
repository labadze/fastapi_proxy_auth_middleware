"""
 Generate Access token to set as HTTP-Only Cookies
"""
import base64
import datetime
import os

import jwt
from cryptography.x509 import load_pem_x509_certificate

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


async def decode_back_end_token(encoded: str):
    options = {
        'verify_signature': False,
        'verify_exp': False,  # Skipping expiration date check
        'verify_aud': False
    }
    public_key_cert = b"-----BEGIN CERTIFICATE-----\nMIIClzCCAX8CBgGEcGBSXzANBgkqhkiG9w0BAQsFADAPMQ0wCwYDVQQDDARmYXB5MB4XDTIyMTExMzA5NDI1MVoXDTMyMTExMzA5NDQzMVowDzENMAsGA1UEAwwEZmFweTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAIMcKfI1wwT/7z+ulGSTu27TSzQiuP86YzoGRXZAyR/+8/8rdYKX7zYNqwi75tRWHtU32rKzs1FC2k4aBYlrDxRsfjKkAz0b6nmHMPtphOQEQZz/yL1nupHxBWs1sOl8pe9MX0aCbDZr4HV9sV9f7uRkEWC4C18wy6LLYFbJctYk0+U03AXZqvkKmIfUyZFYjw/9t767+PFbpw3AKwxvmAse2E1UFb/QPsAzcTsfBp0Z6nTJHGbTQX1TqDvkZ8oLPYocjHw09qE8iZMf0UKYj5RPReulLmgJUc+lQzhKHlujekg1V7FTpZt6iR/qXBH0mK4Y26lAqUvC47KTgOFwM7sCAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAUDZ1YoF+mMpzg3h6u6VC4d8iEW/4SkKlgU5y51bjrLu5WlmTZxFI5lfOTDnnHWYLacrXRYyIVZarBd87lH0EzSN1Cs416xMaQCZVHhPzqj0Uzdb6ojOFPXcLqDLR48VeRQVgBuLHx/l44mP95QbwKjGuL6pHFR1/ivuAK5hi3A8drx8PLLxPZNzg/L1bXtqTfisvKOM8zsPCSiZZMGjZ97feZ6yIPsWEBE8q/f8vycYYG7jcIlXxd3gF3Vsovpn8cVA71c9eimd6x2c2oF5TybRkMSvPNBHCnY2txCmXR043zA2Esj/Gqj7rqeOPyxTC0KZuvvN5F7ciOXB0IN73ug==\n-----END CERTIFICATE-----"
    cert_obj = load_pem_x509_certificate(public_key_cert)
    public_key = cert_obj.public_key()
    result = jwt.decode(encoded, public_key, algorithms=["RS256"], options=options)
    print(result)
