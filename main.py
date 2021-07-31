import discord
from discord.ext import commands
import json
import random
import datetime
import time
import math

print("Démarrage ...")
client = discord.Client()
token = "NzMyMjEyNzE4NTkzMTE0MTYy.XwxUOw.MdYfKWnA7cv-7pBYftTpoT8aCXE"
bot = commands.Bot(command_prefix="/")
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("/help"))
    print("Le bot a démarré !")


@bot.command()
async def help(ctx):
    await   ctx.send("Voici les règles du jeu : ...")


@bot.command()
async def test(ctx):
    pass


bot.run(token)
