import sqlite3

def __init__():
    conn = sqlite3.connect('rpg.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR UNIQUE       
    )               
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS character (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name VARCHAR(30) UNIQUE,
        class VARCHAR(15) NOT NULL,
        level TINYINT NOT NULL,
        xp SMALLINT NOT NULL,
        defense DOUBLE(4, 2) NOT NULL,
        dexterity DOUBLE(4, 2) NOT NULL,
        hp DOUBLE(4, 2) NOT NULL,
        strength DOUBLE(4, 2) NOT NULL,
        wisdom DOUBLE(4, 2)   NOT NULL,    
        FOREIGN KEY (user_id) REFERENCES user (id)    
    )               
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS story (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(60) UNIQUE,
        synopsis VARCHAR NOT NULL
    )            
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY,
        story_id INTEGER NOT NULL,
        description VARCHAR NOT NULL,
        FOREIGN KEY (story_id) REFERENCES stories (id)
    )            
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS choice (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        progress_id INTEGER NOT NULL,
        value VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        response VARCHAR NOT NULL,
        FOREIGN KEY (progress_id) REFERENCES progress (id)
    )            
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_progress (
        user_id INTEGER,
        story_id INTEGER,
        progress_id INTEGER,
        character_id INTEGER,
        PRIMARY KEY (user_id, story_id),
        FOREIGN KEY (user_id) REFERENCES user (id),
        FOREIGN KEY (story_id) REFERENCES story (id),
        FOREIGN KEY (progress_id) REFERENCES progress (id),
        FOREIGN KEY (character_id) REFERENCES character (id)
    )            
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invetory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character_id INTEGER NOT NULL,
        title VARCHAR(30) NULL,
        description VARCHAR NULL,
        add_level TINYINT NULL,
        level_multiplier DOUBLE(4, 2) NULL,
        add_defense DOUBLE(4, 2) NULL,
        defense_multiplier DOUBLE(4, 2) NULL,
        add_dexterity DOUBLE(4, 2) NULL,
        dexterity_multiplier DOUBLE(4, 2) NULL,
        add_hp DOUBLE(4, 2) NULL,
        hp_multiplier DOUBLE(4, 2) NULL,
        add_strength DOUBLE(4, 2) NULL,
        strength_multiplier DOUBLE(4, 2) NULL,
        add_wisdom DOUBLE(4, 2) NULL,  
        wisdom_multiplier DOUBLE(4, 2) NULL,
        FOREIGN KEY (character_id) REFERENCES character (id)
    )            
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS play_now (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        story_id VARCHAR NOT NULL,
        progress_id INTEGER NOT NULL,
        character_id VARCHAR NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user (id),
        FOREIGN KEY (story_id) REFERENCES sotry (id)
        FOREIGN KEY (progress_id) REFERENCES progress (id),
        FOREIGN KEY (character_id) REFERENCES character (id)
    )            
    ''')

    conn.commit()
    conn.close()

__init__()