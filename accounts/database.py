import sqlite3

DB_FILE = 'accounts/jokerface.db'


def init():
    with sqlite3.connect(DB_FILE) as con:
            cur = con.cursor()

            # USERS
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    email_id TEXT NOT NULL UNIQUE,
                    name TEXT,
                    profile_img TEXT
                )
            ''')

            # JOKERS
            cur.execute('''
                CREATE TABLE IF NOT EXISTS jokers (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    bot_name TEXT,
                    bot_code TEXT,
                    avatar_icon TEXT,
                    avatar_bg_color TEXT,
                    avatar_icon_color TEXT,
                        
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            con.commit()

def sign_in(user_data):
        info = user_data.get("userinfo", {})

        email = info.get('email', '')
        name = info.get('name', '')
        profile_img = info.get('picture', '')


        with sqlite3.connect(DB_FILE) as con:
            cur = con.cursor()

            ### if the user already exists, skip
            cur.execute(
                "SELECT id FROM users WHERE email_id = ?", (email,)
            )
            result = cur.fetchone()
            if result:
                return result[0]

            cur.execute(
                "INSERT INTO users (email_id, name, profile_img) VALUES (?, ?, ?)",
                (email, name, profile_img)
            )
            user_id = cur.lastrowid

            cur.execute(
                """
                INSERT INTO jokers (user_id, bot_name, bot_code, avatar_icon, avatar_bg_color, avatar_icon_color)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, 'Jevilish Jokerbot', 

'''def preflop(self, game_state):
    pass

def postflop(self, game_state):
    pass

def turn(self, game_state):
    pass

def river(self, game_state):
    pass''', 
    
    'sym_s_robot_2', '#808080', '#000000')
            )

            con.commit()
        
        return user_id

def get_user_info(user_id):
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        result = cur.fetchone()
        
        return result

def get_joker_info(user_id):
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        
        cur.execute("SELECT * FROM jokers WHERE user_id = ?", (user_id,))
        result = cur.fetchone()
        
        return result

def save_joker_cosmetics(user_id, bot_name, avatar_icon, bg_color, icon_color):

    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute(
            """
            UPDATE jokers
            SET bot_name = ?, avatar_icon = ?, avatar_bg_color = ?, avatar_icon_color = ?
            WHERE user_id = ?
            """,
            (bot_name, avatar_icon, bg_color, icon_color, user_id)
        )
        con.commit()

def save_joker_code(user_id, bot_code):
     with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute(
            """
            UPDATE jokers
            SET bot_code = ?
            WHERE user_id = ?
            """,
            (bot_code, user_id)
        )
        con.commit()