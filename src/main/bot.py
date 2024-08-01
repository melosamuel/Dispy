from discord import ui
from discord.ext import commands

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

class RPGCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="registration", help="Starts user registration")
    async def registration(self, ctx: discord.ApplicationContext):
        self.username = ctx.author.name.lower()

        conn = sqlite3.connect("rpg.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user WHERE name == ?", (self.username,))
        user_exists = cursor.fetchone()

        if user_exists:
            await ctx.send("```You're already registered. ```")
            conn.close()

            return
        
        cursor.execute("INSERT INTO user (name) VALUES (?)", (self.username,))

        await ctx.send("```User successfully registered!```")

        conn.commit()
        conn.close()

    @commands.command(name="add_character", help="Add a new user's character")
    async def add_character(self, ctx: discord.ApplicationContext):
        self.username = ctx.author.name.lower()

        conn = sqlite3.connect("rpg.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user WHERE name == ?", (self.username,))
        user_exists = cursor.fetchone()

        if not user_exists:
            await ctx.send("```You're not registered. Type !registration```")
            conn.close()

            return
        
        self.user_id = user_exists[0]

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

            cursor.execute("INSERT INTO character (user_id, name, class, level, xp, defense, dexterity, hp, strength, wisdom) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.user_id, name, selected, 0, 0, character_class["defense"], character_class["dexterity"], character_class["hp"], character_class["strength"], character_class["wisdom"]))

            conn.commit()
            conn.close()

            await ctx.send("```Character created successfully.```")

        for button in buttons:    
            button.callback = callback
            view.add_item(button)

        await ctx.send(f"**Select your class**", view=view)

bot.add_cog(RPGCog(bot))

if __name__ == "__main__":
    __init__()
    bot.run(ENV["TOKEN"])