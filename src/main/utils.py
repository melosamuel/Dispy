from pathlib import Path

import random

def jobs():
    options = {
        "🔥 Mage": {"strength": random.randint(10, 30), "dexterity": random.randint(30, 50), "defense": random.randint(20, 40), "wisdom": random.randint(80, 100), "hp": random.randint(50, 70)},
        "⚔️ Warrior": {"strength": random.randint(70, 90), "dexterity": random.randint(50, 70), "defense": random.randint(60, 80), "wisdom": random.randint(20, 40), "hp": random.randint(90, 110)},
        "🥷 Assassin": {"strength": random.randint(50, 70), "dexterity": random.randint(80, 100), "defense": random.randint(40, 60), "wisdom": random.randint(30, 50), "hp": random.randint(60, 80)},
        "🛡️ Tanker": {"strength": random.randint(60, 80), "dexterity": random.randint(20, 40), "defense": random.randint(80, 100), "wisdom": random.randint(30, 50), "hp": random.randint(100, 120)},
        "✝️ Paladin": {"strength": random.randint(60, 80), "dexterity": random.randint(40, 60), "defense": random.randint(70, 90), "wisdom": random.randint(50, 70), "hp": random.randint(80, 100)},
        "🌎 Adventurer": {"strength": random.randint(40, 60), "dexterity": random.randint(60, 80), "defense": random.randint(50, 70), "wisdom": random.randint(40, 60), "hp": random.randint(70, 90)},
    }

    return options

def path():
    return Path(__file__).resolve().parent