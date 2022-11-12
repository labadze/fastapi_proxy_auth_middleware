from fastapi import FastAPI
from fastapi_keycloak import FastAPIKeycloak, OIDCUser, UsernamePassword, HTTPMethod, KeycloakUser, KeycloakGroup

app = FastAPI()
idp = FastAPIKeycloak(
    server_url="http://localhost:8080/auth",
    client_id="fapy",
    client_secret="CPbW5J7Ge9pwgFatK4TuV71GVwiLgamv",
    admin_client_secret="l1iBN1Ddv21kfwcCsYM5D2GaxvZmRA2O",
    realm="fapy",
    callback_uri="http://localhost:3000/callback"
)
idp.add_swagger_config(app)
