from discord import ui
from discord.ext import commands

import discord
import json
import sqlite3
import time

from db import __init__

from models.Character import Character
from models.Story import Story
from models.User import User


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
    user: User
    character: Character
    story: Story

    def __init__(self, bot) -> None:
        self.bot = bot
        self.user = None
        self.character = None
        self.story = None

    @commands.command(name="registration", help="Starts user registration")
    async def registration(self, ctx: discord.ApplicationContext):

        conn = sqlite3.connect("rpg.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user WHERE name == ?", (ctx.author.name.lower(),))
        user_exists = cursor.fetchone()

        if user_exists:
            await ctx.send("```You're already registered. ```")
            conn.close()

            self.user = User(user_exists[0], user_exists[1])

            return
        
        cursor.execute("INSERT INTO user (name) VALUES (?)", (ctx.author.name.lower(),))

        await ctx.send("```User successfully registered!```")

        conn.commit()
        conn.close()

    @commands.command(name="add_character", help="Add a new user's character")
    async def add_character(self, ctx: discord.ApplicationContext):
        username = ctx.author.name.lower() if not self.user else self.user.name

        conn = sqlite3.connect("rpg.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user WHERE name == ?", (username,))
        user_exists = cursor.fetchone()

        if not user_exists:
            await ctx.send("```You're not registered. Type !registration```")
            conn.close()

            return
        
        if not self.user:
            self.user = User(user_exists[0], user_exists[1])

        await ctx.send("```Name your character```")
        name = await bot.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        name = name.content.lower()

        cursor.execute("SELECT id FROM character WHERE name == ?", (name,))
        character_exists = cursor.fetchone()

        conn.commit()
        conn.close()

        if character_exists:
            await ctx.send(f"```Character '{name.title()}' already registered.```")
            conn.close()

            return
        
        classes = utils.classes()
        
        buttons = [ui.Button(label=character_class, custom_id=character_class) for character_class in classes.keys()]
        view = ui.View()

        async def callback(interaction: discord.Interaction):
            selected = interaction.data['custom_id']
            await interaction.response.send_message(f"```You've selected {selected.title()}!```", ephemeral=True)

            character_class = classes[f"{selected}"]

            conn = sqlite3.connect("rpg.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO character (user_id, name, class, level, xp, defense, dexterity, hp, strength, wisdom) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.user.get_id(), name, selected, 0, 0, character_class["defense"], character_class["dexterity"], character_class["hp"], character_class["strength"], character_class["wisdom"]))

            conn.commit()
            conn.close()

            await ctx.send("```Character created successfully.```")

        for button in buttons:    
            button.callback = callback
            view.add_item(button)

        await ctx.send(f"**Select your class**", view=view)

    @commands.command(name="add_story", help="Add a new Story")
    async def add_story(self, ctx: discord.ApplicationContext):
        if not ctx.message.attachments:
            await ctx.send("```Append a JSON file. See the bot guide if you need help.``` [How to add stories](https://github.com/melosamuel/Dispy/blob/master/README.md)")
            
            return 
        
        uploaded_json = ctx.message.attachments[0]
        
        if not uploaded_json.filename.endswith('.json'):
            await ctx.send("```The file must be a valid JSON. ```")
            
            return
        
        json_content = await uploaded_json.read()

        try:
            data = json.loads(json_content)

        except json.JSONDecodeError:
            await ctx.send("```This JSON file is malformatted. Please, see: ``` [How to add stories](https://github.com/melosamuel/Dispy/blob/master/README.md)")
            
            return

        if 'name' not in data or 'synopsis' not in data or 'progresses' not in data:
            await ctx.send("```The correct JSON file must have 'name', 'synopsis' and 'progresses' fields.```")
            
            return

        conn = sqlite3.connect('rpg.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO story (name, synopsis) VALUES (?, ?)', (data['name'], data['synopsis']))
            story_id = cursor.lastrowid

        except sqlite3.IntegrityError:
            await ctx.send(f"Story {data['name'].title()} already registered.")
            conn.close()

            return
        
        for progress in data['progresses']:
            cursor.execute('INSERT INTO progress (id, story_id, description) VALUES (?, ?, ?)', (progress["id"], story_id, progress['description']))
            progress_id = cursor.lastrowid

            try:
                for choice in progress['choices']:
                    cursor.execute('INSERT INTO choice (progress_id, value, title, response) VALUES (?, ?, ?, ?)', (progress_id, choice["value"], choice['title'], choice['response']))
            
            except KeyError:
                continue

        conn.commit()
        conn.close()

        await ctx.send(f"```Story '{data['name'].title()}' successfully added.```")

    @commands.command(name="select_character", help="Selects a character to play with")
    async def select_character(self, ctx: discord.ApplicationContext):
        username = ctx.author.name.lower() if not self.user else self.user.get_name()

        conn = sqlite3.connect("rpg.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user WHERE name == ?", (username,))
        user_exists = cursor.fetchone()

        if not user_exists:
            await ctx.send("```You're not registered. Type !registration```")
            conn.close()

            return
        
        if not self.user:
            self.user = User(user_exists[0], user_exists[1])

        cursor.execute("SELECT * FROM character WHERE user_id == ?", (self.user.get_id(),))
        characters_exist = cursor.fetchall()

        conn.close()

        if not characters_exist:
            await ctx.send("```You don't have characters to play with. Type !add_character```")

            return
        
        buttons = [ui.Button(label=character[2].title(), custom_id=character[2]) for character in characters_exist]
        view = ui.View()

        async def callback(interaction: discord.Interaction):
            selected = interaction.data['custom_id']
            await interaction.response.send_message(f"```You've selected {selected.title()}!```", ephemeral=True)

            for character in characters_exist:
                if character[2] == selected:
                    self.character = Character(character[2], character[3], character[4], character[5], character[6], character[8], character[7], character[9], character[10])

        for button in buttons:    
            button.callback = callback
            view.add_item(button)

        await ctx.send(f"**Select your class**", view=view)

    @commands.command(name="select_story", help="Selects a story to play")
    async def select_story(self, ctx: discord.ApplicationContext):
        username = ctx.author.name.lower() if not self.user else self.user.get_name()

        conn = sqlite3.connect("rpg.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user WHERE name == ?", (username,))
        user_exists = cursor.fetchone()

        if not user_exists:
            await ctx.send("```You're not registered. Type !registration```")
            conn.close()

            return
        
        if not self.user:
            self.user = User(user_exists[0], user_exists[1])

        cursor.execute("SELECT * FROM story")
        stories_exists = cursor.fetchall()

        conn.close()

        if not stories_exists:
            await ctx.send("```There are no stories to play.```")

            return
        
        buttons = [ui.Button(label=story[1].title(), custom_id=story[1]) for story in stories_exists]
        view = ui.View()

        async def callback(interaction: discord.Interaction):
            selected = interaction.data['custom_id']
            await interaction.response.send_message(f"```You've selected {selected.title()}!```", ephemeral=True)

            for story in stories_exists:
                if story[1] == selected:
                    self.story = Story(story[0], story[1], story[2])

        for button in buttons:    
            button.callback = callback
            view.add_item(button)

        await ctx.send(f"**Select a story to play**", view=view)

bot.add_cog(RPGCog(bot))

if __name__ == "__main__":
    __init__()
    bot.run(ENV["TOKEN"])