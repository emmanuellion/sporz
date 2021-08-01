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
cascade_mere = ['player', 'compo', 'vote', 'game']


# renvoie le contenu du fichier json
def get():
    with open('sporz.json') as load:
        load = json.load(load)
    return load


# update le fichier json
def push(load):
    with open('sporz.json', "w") as f:
        json.dump(load, f, ensure_ascii=False, indent=4)


# crée un channel pour un certain rôle
async def create_channel(ctx, rol):
    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)}
    load = get()
    for id in load['roles'][rol]['list_player']:
        overwrites[ctx.guild.get_member(int(id))] = discord.PermissionOverwrite(read_messages=True)
    for category in await ctx.guild.fetch_channels():
        if category.name == "🎮👽vaisseau-de-jeu":
            break
    await ctx.guild.create_text_channel(f"channel for {rol}", overwrites=overwrites, category=category)


# update les permissions
async def timeout(ctx):
    for member in ctx.channel.members:
        print(member)
        await ctx.channel.set_permissions(member, read_messages=True, send_messages=False)


# évènement de connexion du bot
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


# s'inscrire
@bot.command()
async def join(ctx):
    load = get()
    if str(ctx.author) not in load['player']:
        load['player'][str(ctx.author)] = {'role': "None", 'isDead': False}
        push(load)
        await ctx.send("Vous êtes désormais inscrit !")
    else:
        await ctx.send("Vous êtes déjà inscrit")


# liste des joueurs inscrit
@bot.command()
async def list_player(ctx):
    load = get()
    embed = discord.Embed(title="Liste des joueurs", description="", color=0x6F00F6)
    for p in load['player']:
        embed.add_field(name=f"{p} :", value=load['player'][p]['isDead'], inline=False)
    await ctx.send(embed=embed)


# se désinscrit
@bot.command()
async def unsign(ctx):
    load = get()
    if str(ctx.author) in load['player']:
        del load['player'][str(ctx.author)]
        push(load)
        await ctx.send("Vous vous êtes désinscrit !")
    else:
        await ctx.send("Vous ne faites pas parti de la liste des personnes inscrite")


# ajoute un rôle à la composition
@bot.command()
async def add(ctx, arg=None):
    if arg is not None:
        load = get()
        if arg in load['roles']:
            load['compo'][arg] = {}
            push(load)
            await ctx.send("Le rôle a bien été ajouté à la composition")
        else:
            await ctx.send("Ce rôle n'existe pas")
    else:
        await ctx.send("Veuillez fournir en paramètre le nom du rôle à inclure dans la composition")


# liste des rôles dans la composition
@bot.command()
async def role(ctx):
    load = get()
    embed = discord.Embed(title="Liste des rôles dans la compo", description="", color=0x6F00F6)
    for rol in load['compo']:
        embed.add_field(name=f"{rol} :", value=load['compo'][rol], inline=False)
    await ctx.send(embed=embed)


# enlève un rôle de composition
@bot.command()
async def remove(ctx, arg=None):
    if arg is not None:
        load = get()
        if arg in load['compo']:
            del load['compo'][arg]
            push(load)
            await ctx.send("Le rôle a bien été supprimé de la composition")
        else:
            await ctx.send("Ce rôle n'est pas dans la compo actuelle")
    else:
        await ctx.send("Veuillez fournir en paramètre le nom du rôle à exclure de la composition")


# commence la partie
@bot.command()
async def start(ctx):
    await ctx.send("Le jeu commence !")


# reinitialise le fichier json
@bot.command()
async def restart(ctx):
    load = get()
    for array in load:
        if array != "roles":
            load[array] = {}
    push(load)
    await ctx.send("Le restart a bien été effectué, les inscriptions et la composition des rôles peuvent commencer !")




@bot.command()
async def help(ctx):
    await ctx.send("Voici les règles du jeu : ...")


@bot.command()
async def cestparti(ctx):
    pass


@bot.command()
async def list_role(ctx):
    load = get()
    embed = discord.Embed(title="Liste des rôles", description="", color=0x6F00F6)
    for rol in load['roles']:
        embed.add_field(name=f"{rol} :", value=load['roles'][rol]['description'], inline=False)
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


@bot.command()
async def test(ctx):
    await create_channel(ctx, "hacker")
    # await timeout(ctx)
    pass


@bot.command()  # admin command
async def clear(ctx, nb_mess=1):
    # if str(ctx.author) in get_admins(str(ctx.guild)):
    try:
        await ctx.channel.purge(limit=int(nb_mess) + 1)
    except ValueError:
        await ctx.send("Veuillez saisir un nombre")
    print("Commande clear")
    # pass


bot.run(token)
