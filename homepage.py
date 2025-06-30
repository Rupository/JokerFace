from nicegui import ui

ui.query('button').classes('rounded-lg')

def icon_select(icon):
    avatar.icon = icon

def bg_colour_select(colour):
    avatar.style(f'background-color: {colour} !important')
    
def main_colour_select(colour):
    avatar.style(f'color: {colour} !important')



ui.html('<span style="color:white"><strong>Design Your Joker</strong></span>').classes('text-2xl')

with ui.row().classes('items-stretch justify-center w-full'):
    with ui.card().classes('rounded-lg'):
        ui.label("Avatar")
        #avatar = ui.avatar('sym_s_robot_2', rounded=True, size='200px', color='grey', text_color="black")

        with ui.column().classes('items-stretch justify-center w-full'):
            avatar = ui.avatar('sym_s_robot_2', rounded=True, size='200px', color='grey', text_color="black").classes('rounded-lg')

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
        
            ui.input(label='Username', placeholder='Jevilish Jokerbot', validation={'Character Limit Exceeded': lambda value: len(value) < 20})
            result = ui.label()

        with ui.row().classes('mt-auto justify-end w-full'):
            ui.button(icon='save')
            ui.button(icon='edit')

    with ui.card().classes('rounded-lg'):
        ui.label("Code")

        with ui.card().classes('rounded-lg no-shadow border-[1px]').style("background-color: white !important;"):
            editor = ui.codemirror(
        '''def preflop(self, game_state):
    pass

def postflop(self, game_state):
    pass

def turn(self, game_state):
    pass

def river(self, game_state):
    pass''', 

                language='Python', theme='githubLight')

            editor.classes('h-[60vh] w-[40vw]')

        with ui.row().classes("mt-auto justify-end w-full"):
            ui.button(icon='save')
            ui.button(icon='edit')

with ui.row().classes('items-stretch w-full justify-center'):

    ui.button("♦️ Warm-up 🤖", color='zinc-800').tooltip("Test out your Joker against a an open source poker bot").style('color:white')
    ui.button("♠️ Versus ♣️", color='Crimson').tooltip("Watch your Joker play a game live against other Jokers made by other players").style('color:white')
    ui.button("📊 Rankings ♥️", color="zinc-800").tooltip("Have your Joker play 100 games against others to guage its overall performance").style('color:white')
      
            
ui.query('body').style(f'background-color: {'SeaGreen'}')
ui.run(favicon='🃏', title='Home', dark=None)