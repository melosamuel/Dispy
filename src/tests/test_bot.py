import discord

def test_bot_can_be_initalized():
    client = discord.Client(intents=discord.Intents.default())

    assert not client is None, f"The bot can't be initialized. Make sure you installed discord.py correctly."