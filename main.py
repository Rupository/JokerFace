from typing import Optional
from fastapi import Request
from starlette.responses import RedirectResponse

from nicegui import app, ui
from pages import homepage
from accounts import authentication

@ui.page('/')
async def landing_page(request: Request) -> Optional[RedirectResponse]:

    user_data = app.storage.user.get('user_data', None)

    if user_data:
        for _ in range(49):
            ui.navigate.history.push('http://localhost:8080/')
        
        homepage.create()

        ui.button('Logout', on_click=authentication.logout)
        ui.label(f'Welcome {user_data.get("userinfo", {}).get("name", "")}!')
        return None
    
    else:

        return await authentication.get_user_data(request)


ui.run(host='localhost', favicon='🃏', title='Home', dark=None, storage_secret='im the finder dodge girl')