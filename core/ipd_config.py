import os

from fastapi import FastAPI
from fastapi_keycloak import FastAPIKeycloak

app = FastAPI()
idp = FastAPIKeycloak(
    server_url=os.getenv("http://localhost:8080/auth", default="http://localhost:8080/auth"),
    client_id=os.getenv("fapy", default="fapy"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET", default="17uKutcUraGPnBCkINpa8VmVFrLMsvMy"),
    admin_client_secret=os.getenv("KEYCLOAK_ADMIN_CLIENT_SECRET", default="3Xr687BkDuDOZlNdEAEOJ96fFCSon9DL"),
    realm=os.getenv("KEYCLOAK_REALM", default="fapy"),
    callback_uri=os.getenv("KEYCLOAK_CALLBACK_URL", default="http://localhost:3000/callback"),
)
idp.add_swagger_config(app)
