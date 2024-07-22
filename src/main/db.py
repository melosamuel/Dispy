import sqlite3

def __init__():
    conn = sqlite3.connect('rpg.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR UNIQUE       
    )               
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS heroes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user INTEGER NOT NULL,
        name VARCHAR(30) UNIQUE,
        age BIT NOT NULL,
        job VARCHAR(15) NOT NULL,
        level TINYINT NOT NULL,
        xp SMALLINT NOT NULL,
        defense DOUBLE(4, 2) NOT NULL,
        dexterity DOUBLE(4, 2) NOT NULL,
        hp DOUBLE(4, 2) NOT NULL,
        strength DOUBLE(4, 2) NOT NULL,
        wisdom DOUBLE(4, 2)   NOT NULL,    
        FOREIGN KEY (user) REFERENCES players (id)    
    )               
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(60) UNIQUE,
        resume VARCHAR NOT NULL
    )            
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_id INTEGER NOT NULL,
        description VARCHAR NOT NULL,
        FOREIGN KEY (story_id) REFERENCES stories (id)
    )            
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS choices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        progress_id INTEGER NOT NULL,
        title VARCHAR NOT NULL,
        response VARCHAR NOT NULL,
        FOREIGN KEY (progress_id) REFERENCES progress (id)
    )            
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invetory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hero_id INTEGER NOT NULL,
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
        FOREIGN KEY (hero_id) REFERENCES heroes (id)
    )            
    ''')

    conn.commit()
    conn.close()

__init__()