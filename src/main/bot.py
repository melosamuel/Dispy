from discord import ui
from discord.ext import commands

from models.Hero import Hero

import discord
import json
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

class RPGCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="register", help="Starts hero registration")
    async def register(self, ctx: discord.ApplicationContext):
        conn = sqlite3.connect("rpg.db")
        cursor = conn.cursor()

        jobs = utils.jobs()
        username = ctx.author.name
        username = username.lower()

        try:
            cursor.execute("INSERT INTO players (username) VALUES (?)", (username,))
        except sqlite3.IntegrityError:
            log.info(f"User {username} alredy registered")
        finally:
            cursor.execute("SELECT id FROM players WHERE username == ?", (username,))
            player = cursor.fetchone()

        await ctx.send("``` Hi, there! \nLet's create your character. First, what's his name: ```")
        name = await bot.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        name = name.content
        name = name.lower()

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

            cursor.execute("INSERT INTO heroes (user, name, age, job, level, xp, defense, dexterity, hp, strength, wisdom) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (player[0], name, age, choice, 0, 0, job["defense"], job["dexterity"], job["hp"], job["strength"], job["wisdom"]))

            time.sleep(1)

            await ctx.send("``` Hero created successfully. ```")

            conn.commit()
            conn.close()

            return None

        for button in buttons:    
            button.callback = callback
            view.add_item(button)

        await ctx.send(f"**Select your class**", view=view)

    @commands.command(name="add_story", help="Uploads a story as a JSON file")
    async def add_story(self, ctx: discord.ApplicationContext):
        if not ctx.message.attachments:
            await ctx.send("``` Please, append a JSON file. See the bot guide if you need help. ```")
            return
        
        uploaded_json = ctx.message.attachments[0]
        if not uploaded_json.filename.endswith('.json'):
            await ctx.send("``` Please, the file must be a valid JSON. ```")
            return
        
        json_content = await uploaded_json.read()
        try:
            data = json.loads(json_content)
        except json.JSONDecodeError:
            await ctx.send("``` This JSON file is malformatted. Please, see: ``` [How to add stories](https://github.com/melosamuel/Dispy/blob/master/README.md)")
            return

        if 'name' not in data or 'resume' not in data or 'progresses' not in data:
            await ctx.send("```The correct JSON file must have 'name', 'description' and 'progresses' fields. ```")
            return

        conn = sqlite3.connect('rpg.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO stories (name, resume) VALUES (?, ?)', (data['name'], data['resume']))
            story_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            await ctx.send(f"Story {data['name']} already registered.")
            conn.close()
            return
        
        for progress in data['progresses']:
            cursor.execute('INSERT INTO progress (story_id, description) VALUES (?, ?)', (story_id, progress['description']))
            progress_id = cursor.lastrowid

            try:
                for choice in progress['choices']:
                    cursor.execute('INSERT INTO choices (progress_id, title, response) VALUES (?, ?, ?)', (progress_id, choice['title'], choice['response']))
            except KeyError:
                continue

        conn.commit()
        conn.close()

        await ctx.send(f"``` Story {data['name'].capitalize()} successfully added. ```")

bot.add_cog(RPGCog(bot))

if __name__ == "__main__":
    __init__()
    bot.run(ENV["TOKEN"])