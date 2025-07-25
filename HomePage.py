# main page for bot setup

from nicegui import ui, app

from accounts import authentication, database



def create(user_id):

    user_id = app.storage.user.get('user_id', 0)

    if user_id == 0:
        raise LookupError('No users detected')

    curr_state = {'icon' : database.get_joker_info(user_id)[4],
                'bg_colour' : database.get_joker_info(user_id)[5],
                'main_colour' : database.get_joker_info(user_id)[6],
                'name' : database.get_joker_info(user_id)[2],
                'code': database.get_joker_info(user_id)[3]}

    ui.query('button').classes('rounded-lg')
    ui.query('body').style(f'background-color: {'SeaGreen'}')

    def icon_select(icon):
        curr_state['icon'] = icon
        avatar.icon = icon

    def bg_colour_select(colour):
        curr_state['bg_colour'] = colour
        avatar.style(f'background-color: {colour} !important')
        
    def main_colour_select(colour):
        curr_state['main_colour'] = colour
        avatar.style(f'color: {colour} !important')
    
    def save_joker_cosmetics():
        database.save_joker_cosmetics(
            user_id,
            bot_name= curr_state['name'],
            avatar_icon= curr_state['icon'],
            bg_color= curr_state['bg_colour'],
            icon_color= curr_state['main_colour']
        )

        ui.notify('Joker cosmetics saved')
    
    def save_joker_code():
        database.save_joker_code(user_id, bot_code=curr_state['code'])
        ui.notify('Joker code saved')

    ui.html('<span style="color:white"><strong>Design Your Joker</strong></span>').classes('text-2xl')

    with ui.card().classes('fixed top-2 right-2'):

        with ui.row().classes('items-center'):
        
            with ui.avatar():
                ui.image(database.get_user_info(user_id)[3])

            with ui.column().classes('items-center'):
                ui.label(database.get_user_info(user_id)[2])
                ui.button('log out', on_click=lambda: authentication.logout())

    with ui.row().classes('items-stretch justify-center w-full'):
        with ui.card().classes('rounded-lg'):
            ui.label("Avatar")

            with ui.column().classes('items-stretch justify-center w-full'):
                avatar = ui.avatar(icon = curr_state['icon'], 
                                   rounded=True, size='200px', 
                                   color = curr_state['bg_colour'], 
                                   text_color=curr_state['main_colour']).classes('rounded-lg')

                with ui.row().classes('items-stretch justify-center w-full'):
                    with ui.dropdown_button(icon='face'):
                        ui.item('Robot', on_click=lambda: icon_select('sym_s_robot_2'))
                        ui.item('Chip', on_click=lambda: icon_select('sym_s_poker_chip'))
                        ui.item('Dice', on_click=lambda: icon_select('sym_s_casino'))
                        ui.item('Cards', on_click=lambda: icon_select('sym_s_playing_cards'))

                    with ui.dropdown_button(icon='colorize'):
                        with ui.item('Icon', on_click=lambda *args: None):
                            ui.color_picker(on_pick=lambda e: main_colour_select(e.color))
                        with ui.item('Background', on_click=lambda *args: None):
                            ui.color_picker(on_pick=lambda e: bg_colour_select(e.color))
            
                ui.input(label='Name Your Bot', placeholder='Jevilish Jokerbot', 
                         validation={'Character Limit Exceeded': lambda value: len(value) < 20}).bind_value(curr_state, 'name')
                result = ui.label()

            with ui.row().classes('mt-auto justify-end w-full'):
                ui.button(icon='save', 
                          on_click = save_joker_cosmetics)

        with ui.card().classes('rounded-lg'):
            ui.label("Code")

            with ui.card().classes('rounded-lg no-shadow border-[1px]').style("background-color: white !important;"):
                editor = ui.codemirror(value = curr_state['code'], language='Python', theme='githubLight').bind_value(curr_state, 'code')

                editor.classes('h-[60vh] w-[40vw]')

            with ui.row().classes("mt-auto justify-end w-full"):
                ui.button(icon='save', on_click=save_joker_code)

    with ui.row().classes('items-stretch w-full justify-center'):

        ui.button("♦️ Warm-up 🤖", color='zinc-800').tooltip("Test out your Joker against a an open source poker bot").style('color:white')
        ui.button("♠️ Versus ♣️", color='Crimson').tooltip("Watch your Joker play a game live against other Jokers made by other players").style('color:white')
        ui.button("📊 Rankings ♥️", color="zinc-800").tooltip("Have your Joker play 100 games against others to guage its overall performance").style('color:white')