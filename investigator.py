import discord
from discord.ext import commands
import datetime
import pytz

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="v!", intents=intents)

@bot.command()
async def creation(ctx):
    await ctx.send("**ID CREATION TIME INVESTIGATOR ACTIVATED, STATE THE TARGETS BOT ID**")
    
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()
    
    msg = await bot.wait_for("message", check=check)
    bot_id = int(msg.content)
    
    creation_time = discord.utils.snowflake_time(bot_id)
    utc_time = creation_time.astimezone(pytz.utc)
    formatted_time = utc_time.strftime("%m/%d/%Y %I:%M:%S %p UTC")
    
    await ctx.send(f"**SUCCESSFUL** : Bot ID `{bot_id}` was created on: `{formatted_time}`")

bot.run("Made by Ira")
