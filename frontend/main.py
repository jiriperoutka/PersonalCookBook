from nicegui import ui, app
from pages.home import home_page
from pages.new_recipe import new_recipe_page
from pages.upload_test import upload_test_page
from pages.recipe_detail import recipe_detail_page
from pages.edit_recipe import edit_recipe_page
from components.top_bar import render_top_bar

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.base_client.errors import OAuthError
from authlib.jose import jwt, JoseError

from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from starlette.requests import Request

from dotenv import load_dotenv
import os

# --- Načti prostředí ---
load_dotenv()

# --- Auth0 konfigurace ---
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

# --- NiceGUI session + FastAPI session ---
app.add_middleware(SessionMiddleware, secret_key=os.getenv("STORAGE_SECRET", "dev-secret"))

# --- OAuth klient ---
oauth = OAuth()
oauth.register(
    name='auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration',
    redirect_uri=AUTH0_CALLBACK_URL,
)

# --- Session: user_sessions dictionary ---
user_sessions = {}

def get_current_user():
    session_id = app.storage.user.get("id")
    return user_sessions.get(session_id)

# --- Login ---
@app.get('/login')
async def login(request: Request):
    return await oauth.auth0.authorize_redirect(request, AUTH0_CALLBACK_URL)

# --- Callback ---
@app.get('/callback')
async def callback(request: Request):
    try:
        token = await oauth.auth0.authorize_access_token(request)
        id_token = token.get("id_token")

        if not id_token:
            print("❌ ID token chybí:", token)
            return RedirectResponse('/')

        metadata = await oauth.auth0.load_server_metadata()
        claims = jwt.decode(id_token, key=metadata["jwks"])
        claims.validate()

        session_id = request.session.setdefault("id", os.urandom(12).hex())
        app.storage.user["id"] = session_id
        user_sessions[session_id] = claims

        return RedirectResponse('/')

    except OAuthError as e:
        print("❌ OAuth chyba:", e)
        return RedirectResponse('/')
    except JoseError as e:
        print("❌ JWT ověření selhalo:", e)
        return RedirectResponse('/')

# --- Logout ---
@app.get('/logout')
async def logout(request: Request):
    session_id = request.session.get("id")
    if session_id in user_sessions:
        del user_sessions[session_id]
    app.storage.user.clear()
    logout_url = (
        f'https://{AUTH0_DOMAIN}/v2/logout'
        f'?client_id={AUTH0_CLIENT_ID}'
        f'&returnTo=http://localhost:8080'
    )
    return RedirectResponse(logout_url)

# --- Stránky ---
@ui.page("/")
def index():
    user = get_current_user()

    @ui.page("/")
    def index():
        user = get_current_user()

        render_top_bar(user)

        ui.separator()

        if user:
            home_page()
        else:
            ui.label("Pro zobrazení receptů se prosím přihlaste.").classes("mt-4 text-gray-600")

    # Obsah
    if user:
        home_page()
    else:
        ui.label("Pro zobrazení receptů se prosím přihlaste.").classes("mt-4 text-gray-600")

@ui.page("/new")
def new():
    new_recipe_page()

@ui.page("/upload-test")
def upload_test():
    upload_test_page()

@ui.page("/recipe/{recipe_id}")
def recipe_detail(recipe_id: str):
    recipe_detail_page(recipe_id)

@ui.page("/edit/{recipe_id}")
def edit(recipe_id: str):
    edit_recipe_page(recipe_id)

# --- Spuštění ---
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(storage_secret=os.getenv("STORAGE_SECRET", "default-dev-secret"))