from discord.ext import commands

import discord
import sqlite3

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

        await ctx.send("```User successfully registered! ```")

        conn.commit()
        conn.close()

bot.add_cog(RPGCog(bot))

if __name__ == "__main__":
    __init__()
    bot.run(ENV["TOKEN"])