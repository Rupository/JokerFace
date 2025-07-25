# a login page+handler for users to connect google accounts

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Request
from starlette.responses import RedirectResponse

from nicegui import app, ui

from accounts import database

GOOGLE_CLIENT_ID = '...'
GOOGLE_CLIENT_SECRET = '...'

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id = GOOGLE_CLIENT_ID,
    client_secret = GOOGLE_CLIENT_SECRET,
    client_kwargs = {'scope': 'openid email profile'},
)

@app.get('/auth')
async def google_oauth(request: Request) -> RedirectResponse:

    try:
        user_data = await oauth.google.authorize_access_token(request) # type: ignore
    except OAuthError as e:
        print(f'OAuth error: {e}')
        return RedirectResponse('/')  # or return an error page/message
    
    app.storage.user['user_id'] = database.sign_in(user_data)

    return RedirectResponse('/')
    
def logout() -> None:
    app.storage.user['user_id'] = 0
    ui.navigate.to('/')

def get_user_data(request: Request):
    url = request.url_for('google_oauth')
    return oauth.google.authorize_redirect(request, url) # type: ignore