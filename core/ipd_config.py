from fastapi import FastAPI
from fastapi_keycloak import FastAPIKeycloak, OIDCUser, UsernamePassword, HTTPMethod, KeycloakUser, KeycloakGroup

app = FastAPI()
idp = FastAPIKeycloak(
    server_url="http://localhost:8080/auth",
    client_id="fapy",
    client_secret="XzuBCwsaaszhazCc1GNeUKPgTNc9hZAR",
    admin_client_secret="tja7jaR7dqdHHacrGqY1aGH8FlsoSId4",
    realm="fapy",
    callback_uri="http://localhost:3000/callback"
)
idp.add_swagger_config(app)
