from discord import ui

from models.Hero import Hero

import discord
import sqlite3
import time

from db import __init__

import config
import utils

__DIR__ = utils.path()
ENV = config.get_variables()

bot = config.bot()
log = config.log(__DIR__ / "log/", "bot.log")

@bot.event
async def on_ready():
    log.info("Bot started")

@bot.slash_command(name="register", description="Starts character registration")
async def register(ctx: discord.ApplicationContext):
    conn = sqlite3.connect("rpg.db")
    cursor = conn.cursor()

    jobs = utils.jobs()
    username = ctx.author.name

    try:
        cursor.execute("INSERT INTO players (username) VALUES (?)", (username,))
    except sqlite3.IntegrityError:
        log.info(f"User {username} alredy registered")
    finally:
        cursor.execute("SELECT id FROM players WHERE username == ?", (username,))
        player = cursor.fetchone()

    await ctx.respond("``` Hi, there! \nLet's create your character. First, what's his name: ```")
    name = await bot.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
    name = name.content

    cursor.execute("SELECT id FROM heroes WHERE name == ?", (name,))
    existing_hero = cursor.fetchone()
    
    if existing_hero:
        await ctx.send(f"Hero {name} already registered. Try again.")
        conn.close()
        return

    time.sleep(0.5)

    await ctx.send("``` And how old is your hero? ```")
    age = await bot.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
    age = age.content

    time.sleep(1)

    buttons = [ui.Button(label=job, custom_id=job) for job in jobs.keys()]
    view = ui.View()

    async def callback(interaction: discord.Interaction):
        choice = interaction.data['custom_id']
        await interaction.response.send_message(f"``` You've selected {choice}! ```", ephemeral=True)

        job = jobs[f"{choice}"]
        hero = Hero(name, age, choice, 0, 0, job["dexterity"], job["defense"], job["hp"], job["strength"], job["wisdom"])

        cursor.execute("INSERT INTO heroes (user, name, age, job, level, xp, defense, dexterity, hp, strength, wisdom) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (player[0], hero.get_name(), hero.get_age(), hero.get_job(), hero.get_level(), hero.get_xp(), hero.get_defense(), hero.get_dexterity(), hero.get_hp(), hero.get_strength(), hero.get_wisdom()))

        time.sleep(1)

        await ctx.send("``` Hero created successfully. ```")

        conn.commit()
        conn.close()

        return None

    for button in buttons:    
        button.callback = callback
        view.add_item(button)

    await ctx.send(f"**Select your class**", view=view)

if __name__ == "__main__":
    __init__()
    bot.run(ENV["TOKEN"])