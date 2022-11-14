import os

from fastapi import FastAPI
from fastapi_keycloak import FastAPIKeycloak, OIDCUser, UsernamePassword, HTTPMethod, KeycloakUser, KeycloakGroup

app = FastAPI()
idp = FastAPIKeycloak(
    server_url=os.getenv("KEYCLOAK_SERVER_URL", default="http://localhost:8080/auth"),
    client_id=os.getenv("KEYCLOAK_CLIENT_ID", default="fapy"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET", default="XzuBCwsaaszhazCc1GNeUKPgTNc9hZAR"),
    admin_client_secret=os.getenv("KEYCLOAK_ADMIN_CLIENT_SECRET", default="tja7jaR7dqdHHacrGqY1aGH8FlsoSId4"),
    realm=os.getenv("KEYCLOAK_REALM", default="fapy"),
    callback_uri=os.getenv("BACK_END_URL", default="http://localhost:3000/callback"),
)
idp.add_swagger_config(app)
