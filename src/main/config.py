from dotenv import load_dotenv

import discord
import logging
import os

def bot():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = discord.Bot(intents=intents)

    return bot

def get_variables():
    load_dotenv()

    TOKEN = os.getenv('TOKEN')

    return {
        "TOKEN": TOKEN
    }

def log(path: str, filename: str):
    path.mkdir(parents=True, exist_ok=True) 
    logging.basicConfig(filename=path / filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logger = logging.getLogger()

    return logger