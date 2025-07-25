from typing import Optional
from fastapi import Request
from starlette.responses import RedirectResponse

from nicegui import app, ui

import HomePage
from accounts import authentication, database


database.init()

@ui.page('/')
async def landing_page(request: Request) -> Optional[RedirectResponse]:

    user_id = app.storage.user.get('user_id', 0)

    if user_id:

        for _ in range(100):
            ui.navigate.history.push('/')

        HomePage.create(user_id)

        return None
    
    else:

        return await authentication.get_user_data(request)


ui.run(host='127.0.0.1', favicon='🃏', title='Home', dark=None, storage_secret='im the finder dodge girl')