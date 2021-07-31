import discord
from discord.ext import commands
import json
import random
import datetime
import time
import math

print("Démarrage ...")
client = discord.Client()
intents = discord.Intents.all()
token = "token"
bot = commands.Bot(command_prefix="/", intents=intents)
bot.remove_command("help")


def get():
    with open('sporz.json') as load:
        load = json.load(load)
    return load


def push(load):
    with open('sporz.json', "w") as f:
        json.dump(load, f, ensure_ascii=False, indent=4)


@bot.event
async def on_ready():
    try:
        with open('sporz.json') as load:
            load = json.load(load)
    except FileNotFoundError:
        load = {}
        with open('sporz.json', "w") as f:
            json.dump(load, f, ensure_ascii=False, indent=4)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("/help"))
    print("Le bot a démarré !")


@bot.command()
async def help(ctx):
    await ctx.send("Voici les règles du jeu : ...")


@bot.command()
async def start(ctx):
    pass


@bot.command()
async def restart(ctx):
    pass


@bot.command()
async def join(ctx):
    pass


@bot.command()
async def add(ctx):
    pass


@bot.command()
async def cestparti(ctx):
    pass


@bot.command()
async def role(ctx):
    load = get()
    embed = discord.Embed(title="Liste des rôles", description="", color=0x6F00F6)
    for rol in load['compo']:
        embed.add_field(name=f"{rol} :", value=load['compo'][rol], inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def add_role(ctx, arg1, arg2):
    load = get()
    if arg1 not in load['roles']:
        load['roles'][arg1] = {'description': arg2}
        push(load)
        await ctx.send(f'Le rôle : "{arg1}" a bien été ajouté !')
    else:
        await ctx.send(f'Le rôle "{arg1}" existe déjà')
    print("Commande add_role")


@bot.command()
async def delete_role(ctx, arg1):
    load = get()
    if arg1 in load['roles']:
        del load['roles'][arg1]
        push(load)
        await ctx.send(f'Le rôle : "{arg1}" a bien été supprimé !')
    else:
        await ctx.send(f'Le rôle "{arg1}" n\'existe pas')
    print("Commande delete_role")


@bot.command()
async def admin(ctx):
    await ctx.send(get())


@bot.command()  # admin command
async def clear(ctx, nb_mess=1):
    #if str(ctx.author) in get_admins(str(ctx.guild)):
    #    try:
    #        await ctx.channel.purge(limit=int(nb_mess) + 1)
    #    except ValueError:
    #        await ctx.send("Veuillez saisir un nombre")
    #print("Commande clear")
    pass


bot.run(token)
