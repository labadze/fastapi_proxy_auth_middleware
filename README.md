# Fast Api based back-end


## Known issues

 - Swagger openapi does not support HTTP-Only Cookie auth anymore 

## Installation

 - Make sure python is installed on your instance
 - Clone or download code
 - Go to project directory and install required packages `pip install -r requirements.txt`

## Create virtual environment

Follow instructions from urls provided bellow:

[https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)


## Follow setup for keycloak

Described here: 

[https://github.com/labadze/fast_api_keycloak_auth_proxy](https://github.com/labadze/fast_api_keycloak_auth_proxy)

## Environment variables
First set following env variables:

    DATABASE_URL=postgresql+asyncpg://<username>:<password>@127.0.0.1:5432/<database_name>
    JWT_ISSUER=
    JWT_KEY=
    JWT_KID=
    KEYCLOAK_SERVER_URL=
    KEYCLOAK_CLIENT_ID=
    KEYCLOAK_CLIENT_SECRET=
    KEYCLOAK_ADMIN_CLIENT_SECRET=
    KEYCLOAK_REALM=
    KEYCLOAK_CALLBACK_URL=
    BACK_END_URL=

 - Make sure that you've created database and have full access to it.
 - For unix type systems use `export` for MS Windows use `SET` before variable values

## Run migrations to create required tables in your database

Make sure that your database server is running

Run:
 - `alembic upgrade head`

This will create required tables and required relations

## Run your application

Make sure keycloak and back-end is set up and running

and after run

    `uvicorn run main:app --reload --port 8090`
your app will run on [http://localhost:8090](http://localhost:8090)

## Folder stricture

    .
    ├── ...
    ├── api                           # Static folder files and folders located here are accessable for browsers
    │   ├── account.py                          # !!!IMPORTTANT!!! Your content (IMAGES) must be here...
    │   └── items.py                       # Stylesheet CSS for goo visual
    ├── core                        # Here are files which python renders in browser
    │   └── index.html                   # Main file which is shown for user at start, most operations are called from here
    ├── .gitignore                       # Requered to prevent load venv to git repository
    ├── app.py                           # Programmatically everything nice happens here
    ├── data.json                        # Here is stored annotations data, coordinates, other values including image names from img folder
    ├── LICENSE                          # Standard license from upwork copied here
    ├── main.cmd                         # Start application script for MS Windows users
    ├── main.sh                          # Start application script for Linux users
    ├── README.md                        # you're here
    ├── requirements.txt                 # Installed packeges via pip are stored here.
    ├── setup.sh                         # Setup script for Linux users
    └── setup.cmd                        # Setup script for MS Windows users



