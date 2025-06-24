from nicegui import ui

ui.markdown('#### **Design Your Joker**')
with ui.row().classes('items-stretch'):
    with ui.card():
        ui.label("Avatar")
        ui.button('Save')

    with ui.card():
        ui.label = ("Edit JokerBot Code:")
        editor = ui.codemirror(
'''def __init__(self):
    pass
    
def preflop(self, game_state):
    pass

def postflop(self, game_state):
    pass

def turn(self, game_state):
    pass

def river(self, game_state):
    pass''', 

    language='Python', theme='vscodeLightStyle')
        #ui.button('Save')
        editor.classes('h-[50vh]')

ui.run(favicon='🃏', title='Home')

