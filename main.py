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
cascade_mere = ['player', 'compo', 'vote']
body = {
    "roles": {
        "list_player": {},
        "total_player": 0,
        "nb_now": 0
    },
    "game": {
        "nb_player": 0,
        "game_started": False,
        "id_choice": 0
    }
}
list_msg_bvn = ['Bienvenue à bord de la station ', "Bienvenue à bord mais n'oublie pas de te méfier des autres ",
                'Ici on est là pour écraser des mutants ', 'Direction le tableau de bord ']
switch_choice_compo = 1


# renvoie le contenu du fichier json
def get():
    with open('sporz.json') as load:
        load = json.load(load)
    return load


# update le fichier json
def push(load):
    with open('sporz.json', "w") as f:
        json.dump(load, f, ensure_ascii=False, indent=4)


def assignment(ctx):
    pass


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
        load = get()
    except FileNotFoundError:
        load = {}
        push(load)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("/help"))
    print("Le bot a démarré !")


@bot.event
async def on_member_join(member):
    channel = member.guild.channels[1]
    await channel.send(f"{random.choice(list_msg_bvn)} <@{member.id}> !")


@bot.event
async def on_raw_reaction_add(payload):
    global switch_choice_compo
    load = get()
    if payload.user_id != 803364581954158702:
        if load['game']['id_choice'] == payload.message_id:
            if switch_choice_compo % 2 != 0:
                if payload.emoji.name == "hacker":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "geneticien":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "fanatique":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "astro":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "espion":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "medecin":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "mutant":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "psychologue":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "informaticien":
                    load['roles'][payload.emoji.name]['total_player'] += 1
            else:
                if payload.emoji.name == "hacker":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "geneticien":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "fanatique":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "astro":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "espion":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "medecin":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "mutant":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "psychologue":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "informaticien":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
            push(load)
            msg = await bot.get_guild(payload.guild_id).get_channel(payload.channel_id).fetch_message(
                payload.message_id)
            embed = discord.Embed(title="Liste des rôles", description="", color=0x6F00F6)
            for rol in load['compo']:
                embed.add_field(name=f"{rol} :", value=load['roles'][rol]['total_player'], inline=False)
            await msg.edit(embed=embed)
        if payload.emoji.name == "👽":
            switch_choice_compo += 1


@bot.event
async def on_raw_reaction_remove(payload):
    global switch_choice_compo
    load = get()
    if payload.user_id != 803364581954158702:
        if load['game']['id_choice'] == payload.message_id:
            if switch_choice_compo % 2 != 0:
                if payload.emoji.name == "hacker":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "geneticien":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "fanatique":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "astro":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "espion":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "medecin":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "mutant":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "psychologue":
                    load['roles'][payload.emoji.name]['total_player'] += 1
                elif payload.emoji.name == "informaticien":
                    load['roles'][payload.emoji.name]['total_player'] += 1
            else:
                if payload.emoji.name == "hacker":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "geneticien":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "fanatique":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "astro":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "espion":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "medecin":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "mutant":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "psychologue":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "informaticien":
                    load['roles'][payload.emoji.name]['total_player'] -= 1
            push(load)
            msg = await bot.get_guild(payload.guild_id).get_channel(payload.channel_id).fetch_message(
                payload.message_id)
            embed = discord.Embed(title="Liste des rôles", description="", color=0x6F00F6)
            for rol in load['compo']:
                embed.add_field(name=f"{rol} :", value=load['roles'][rol]['total_player'], inline=False)
            await msg.edit(embed=embed)
        if payload.emoji.name == "👽":
            switch_choice_compo += 1


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Liste des commandes", description="", color=0x6F00F6)
    embed.add_field(name="/help", value="Affiche la liste des commandes", inline=False)
    embed.add_field(name="/join", value="Permet de s'inscrire", inline=False)
    embed.add_field(name="/list_player", value="Affiche la liste des joueurs inscrit", inline=False)
    embed.add_field(name="/unjoin", value="Permet de se désinscrire", inline=False)
    embed.add_field(name="/add", value="Ajoute un rôle à la composition", inline=False)
    embed.add_field(name="/role", value="Affiche la liste des rôles dans la composition", inline=False)
    embed.add_field(name="/remove", value="Enlève un rôle de la composition", inline=False)
    embed.add_field(name="/make_compo", value="Panneau de contrôle pour le nombre de rôles dans la composition",
                    inline=False)
    embed.add_field(name="/start", value="Commence le jeu", inline=False)
    embed.add_field(name="/restart", value="Réinitialise les salons et le fichier json", inline=False)
    embed.add_field(name="/list_role", value="Affiche la liste des rôles existant", inline=False)
    embed.add_field(name="/admin", value="Affiche tout le contenu du fichier json", inline=False)
    embed.add_field(name="/clear", value="Permet d'effacer un certains nombre de message", inline=False)
    await ctx.send(embed=embed)


# s'inscrire
@bot.command()
async def join(ctx):
    load = get()
    if str(ctx.author) not in load['player']:
        load['game']['nb_player'] += 1
        load['player'][str(ctx.author)] = {'role': "None", 'isDead': False}
        push(load)
        for rol in ctx.guild.roles:
            if rol.name == "joueur":
                break
        await ctx.author.add_roles(rol)
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
async def unjoin(ctx):
    load = get()
    if str(ctx.author) in load['player']:
        load['game']['nb_player'] -= 1
        del load['player'][str(ctx.author)]
        push(load)
        for rol in ctx.guild.roles:
            if rol.name == "joueur":
                break
        await ctx.author.remove_roles(rol)
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
            await ctx.send("Ce rôle n'existe pas, voici la liste des rôles existant =>")
            embed = discord.Embed(title="Liste des rôles", description="", color=0x6F00F6)
            for rol in load['roles']:
                embed.add_field(name=f"{rol}", value="⇧", inline=True)
            await ctx.send(embed=embed)
    else:
        await ctx.send("Veuillez fournir en paramètre le nom du rôle à inclure dans la composition")


# liste des rôles dans la composition
@bot.command()
async def role(ctx):
    load = get()
    if load['compo'] != {}:
        embed = discord.Embed(title="Liste des rôles dans la compo", description="", color=0x6F00F6)
        for rol in load['compo']:
            embed.add_field(name=f"{rol} :", value=load['compo'][rol], inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Veuillez d'abord rajouter des rôles dans la composition via la commande `/add <role>`")


# enlève un rôle de composition
@bot.command()
async def remove(ctx, arg=None):
    if arg is not None:
        load = get()
        if load['compo'] != {}:
            if arg in load['compo']:
                del load['compo'][arg]
                push(load)
                await ctx.send("Le rôle a bien été supprimé de la composition")
            else:
                await ctx.send("Ce rôle n'est pas dans la composition actuelle, voici la liste des rôles dans la "
                               "composition =>")
                embed = discord.Embed(title="Liste des rôles", description="", color=0x6F00F6)
                for rol in load['compo']:
                    embed.add_field(name=f"{rol}", value="⇧", inline=True)
                await ctx.send(embed=embed)
        else:
            await ctx.send("La composition actuelle est vide, veuillez la remplire avant d'enlever des rôles")
    else:
        await ctx.send("Veuillez fournir en paramètre le nom du rôle à exclure de la composition")


@bot.command()
async def make_compo(ctx):
    load = get()
    if load['compo'] != {}:
        embed = discord.Embed(title="Liste des rôles", description="", color=0x6F00F6)
        for rol in load['compo']:
            embed.add_field(name=f"{rol} :", value=load['roles'][rol]['total_player'], inline=False)
        await ctx.send(embed=embed)
        time.sleep(0.5)
        for msg in await ctx.message.channel.history(limit=1).flatten():
            id_last = msg.id
            break
        load['game']['id_choice'] = id_last
        push(load)
        for emojis in ctx.guild.emojis:
            if emojis.name in list(load['compo']):
                await msg.add_reaction(emojis)
        await msg.add_reaction("👽")
    else:
        await ctx.send("Veuillez d'abord rajouter des rôles dans la composition")


# commence la partie
@bot.command()
async def start(ctx):
    load = get()
    if load['game']['nb_player'] >= 4:
        for cat in ctx.guild.categories:
            if cat == "🎮👽vaisseau-de-jeu":
                break
        await ctx.guild.create_text_channel('💻🎮Ordinateur-de-bord', category=cat)
        assignment(ctx)
        load['game']['game_started'] = True
        push(load)
        await ctx.send("Le jeu commence !")
    else:
        await ctx.send("Il n'y a pas assez de joueurs")


# reinitialise le fichier json
@bot.command()
async def restart(ctx):
    load = get()
    for array in cascade_mere:
        load[array] = {}
    for array in body:
        if array == "roles":
            for rol in load['roles']:
                load['roles'][rol] = body[array]
        else:
            load[array] = body[array]
    push(load)
    for cat in ctx.guild.categories:
        if cat == "🎮👽vaisseau-de-jeu":
            break
    for channel in cat.channels:
        await channel.delete()
    await ctx.send("Le restart a bien été effectué, les inscriptions et la composition des rôles peuvent commencer !")


@bot.command()
async def cestparti(ctx):
    pass


@bot.command()
async def list_role(ctx):
    load = get()
    embed = discord.Embed(title="Liste des rôles", description="", color=0x6F00F6)
    for rol in load['roles']:
        embed.add_field(name=f"{rol}", value="⇧", inline=True)
    await ctx.send(embed=embed)


# @bot.command()
# async def add_role(ctx, arg1, arg2):
#     load = get()
#     if arg1 not in load['roles']:
#         load['roles'][arg1] = {'description': arg2}
#         push(load)
#         await ctx.send(f'Le rôle : "{arg1}" a bien été ajouté !')
#     else:
#         await ctx.send(f'Le rôle "{arg1}" existe déjà')
#     print("Commande add_role")


# @bot.command()
# async def delete_role(ctx, arg1):
#     load = get()
#     if arg1 in load['roles']:
#         del load['roles'][arg1]
#         push(load)
#         await ctx.send(f'Le rôle : "{arg1}" a bien été supprimé !')
#     else:
#         await ctx.send(f'Le rôle "{arg1}" n\'existe pas')
#     print("Commande delete_role")


@bot.command()
async def admin(ctx):
    await ctx.send(get())


@bot.command()
async def test(ctx):
    # await create_channel(ctx, "hacker")
    # await timeout(ctx)
    load = get()

    push(load)


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
