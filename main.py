import discord
from discord.ext import commands
import json
import random
import datetime
import time
import math
import asyncio

print("Démarrage ...")
client = discord.Client()
intents = discord.Intents.all()
token = "ODAzMzY0NTgxOTU0MTU4NzAy.YA8tkg.8vqQ4JU3mpPxNXIeYYXZkWpZ1ro"
bot = commands.Bot(command_prefix="/", intents=intents)
bot.remove_command("help")
cascade_mere = ['player', 'compo', 'list_id_chan']
body = {
    "roles": {
        "list_player": [],
        "total_player": 0,
        "nb_now": 0
    },
    "vote": {
        "list_mutate": [],
        "list_paralysze": [],
        "list_kill": [],
        "list_vote": [],
        "list_heal": [],
        "has_voted": []
    },
    "game": {
        "nb_player": 0,
        "game_started": False,
        "id_choice": 0,
        "nb_night": 0,
        "has_mayor": False,
        "nb_alive": 0
    },
    "cat_sporz": 871350484626206790,
    "list_player": [],
}
list_msg_bvn = ['Bienvenue à bord de la station ', "Bienvenue à bord mais n'oublie pas de te méfier des autres ",
                'Ici on est là pour écraser des mutants ', 'Direction le tableau de bord ']
switch_choice_compo = 1
list_roles = ['mutant', 'medecin', 'informaticien', 'psychologue', 'espion', 'astro', 'fanatique',
              'geneticien', 'hacker']
list_roles_base = []
keepLooping = True
list_already_voted = []
nigh = False
turn = "nobody"
paralysed = ""
list_inspected = []
balance_mutant = 0
has_win = False
mutate_done = False
all_voted = False
eliminate = ""


# renvoie le contenu du fichier json
def get():
    with open('sporz.json') as load:
        load = json.load(load)
    return load


def get_players():
    li = []
    lo = get()
    for p in lo['player'].keys():
        li.append(p)
    return li


# update le fichier json
def push(load):
    with open('sporz.json', "w") as f:
        json.dump(load, f, ensure_ascii=False, indent=4)


def compare(l1, l2):
    from collections import Counter
    if Counter(l1) == Counter(l2):
        return True
    else:
        return False


async def assignment(ctx):
    load = get()
    list_member_done = []
    list_member = list(load['player'].keys())
    for rol in load['compo']:
        for nb_player in range(load['roles'][rol]['total_player']):
            member = random.choice(list_member)
            while member in list_member_done:
                member = random.choice(list_member)
            load['player'][member]['role'] = rol
            load['roles'][rol]['list_player'].append(member)
            load['compo'][rol].append(member)
            list_member_done.append(member)
            for m in ctx.guild.members:
                if m.name[:-5] == member:
                    await m.send(f"Vous êtes {rol}")
    if not compare(list_member, list_member_done):
        load['compo']['astro'] = []
        load['roles']['total_roles'] += 1
        while not compare(list_member, list_member_done):
            member = random.choice(list_member)
            while member in list_member_done:
                member = random.choice(list_member)
            load['player'][member]['role'] = "astro"
            load['roles']['astro']['list_player'].append(member)
            load['compo']['astro'].append(member)
            load['roles']['astro']['total_player'] += 1
            list_member_done.append(member)
            for m in ctx.guild.members:
                print(len(member))
                print(len(m.name))
                if str(m.name[:-5]) == str(member):
                    print("oui")
                    await m.send("Vous êtes astronaute")
    if load['roles']['mutant']['total_player'] >= 1:
        if load['roles']['mutant']['total_player'] > 1:
            load['player'][random.choice(load['roles']['mutant']['list_player'])]['is_original_mutant'] = True
        else:
            load['player'][load['roles']['mutant']['list_player'][0]]['is_original_mutant'] = True
    return load


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


async def hub_reaction(payload):
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
                if payload.emoji.name in list_roles:
                    load['roles']['total_roles'] += 1
            else:
                if payload.emoji.name == "hacker":
                    if load['roles'][payload.emoji.name]['total_player'] - 1 >= 0:
                        load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "geneticien":
                    if load['roles'][payload.emoji.name]['total_player'] - 1 >= 0:
                        load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "fanatique":
                    if load['roles'][payload.emoji.name]['total_player'] - 1 >= 0:
                        load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "astro":
                    if load['roles'][payload.emoji.name]['total_player'] - 1 >= 0:
                        load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "espion":
                    if load['roles'][payload.emoji.name]['total_player'] - 1 >= 0:
                        load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "medecin":
                    if load['roles'][payload.emoji.name]['total_player'] - 1 >= 0:
                        load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "mutant":
                    if load['roles'][payload.emoji.name]['total_player'] - 1 >= 0:
                        load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "psychologue":
                    if load['roles'][payload.emoji.name]['total_player'] - 1 >= 0:
                        load['roles'][payload.emoji.name]['total_player'] -= 1
                elif payload.emoji.name == "informaticien":
                    if load['roles'][payload.emoji.name]['total_player'] - 1 >= 0:
                        load['roles'][payload.emoji.name]['total_player'] -= 1
                if payload.emoji.name in list_roles:
                    if load['roles']['total_roles'] - 1 >= 0:
                        load['roles']['total_roles'] -= 1
            push(load)
            msg = await bot.get_guild(payload.guild_id).get_channel(payload.channel_id).fetch_message(
                payload.message_id)
            embed = discord.Embed(title="Liste des rôles", description="", color=0x6F00F6)
            for rol in load['compo']:
                embed.add_field(name=f"{rol} :", value=load['roles'][rol]['total_player'], inline=False)
            await msg.edit(embed=embed)
        if payload.emoji.name == "👽":
            switch_choice_compo += 1


# évènement de connexion du bot
@bot.event
async def on_ready():
    try:
        get()
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
    await hub_reaction(payload)


@bot.event
async def on_raw_reaction_remove(payload):
    await hub_reaction(payload)


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
    embed.add_field(name="/compo", value="Panneau de contrôle pour le nombre de rôles dans la composition",
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
    if str(ctx.author)[:-5] not in load['player']:
        load['game']['nb_player'] += 1
        load['player'][str(ctx.author)[:-5]] = {
            'role': "None",
            'role_before': "None",
            'isDead': False,
            'is_original_mutant': False,
        }
        load['list_player'].append(str(ctx.author)[:-5])
        push(load)
        for rol in ctx.guild.roles:
            if rol.name == "Joueur":
                await ctx.author.add_roles(rol)
                break
        await ctx.send("Vous êtes désormais inscrit !")
    else:
        await ctx.send("Vous êtes déjà inscrit")


# liste des joueurs inscrit
@bot.command()
async def list_player(ctx):
    load = get()
    embed = discord.Embed(title="Liste des joueurs", description="", color=0x6F00F6)
    for p in load['list_player']:
        embed.add_field(name=f"{p} :", value=".", inline=False)
    await ctx.send(embed=embed)


# se désinscrit
@bot.command()
async def unjoin(ctx):
    load = get()
    if str(ctx.author)[:-5] in load['player']:
        load['game']['nb_player'] -= 1
        del load['player'][str(ctx.author)[:-5]]
        load['list_player'].remove(str(ctx.author)[:-5])
        push(load)
        for rol in ctx.guild.roles:
            if rol.name == "Joueur":
                await ctx.author.remove_roles(rol)
                break
        await ctx.send("Vous vous êtes désinscrit !")
    else:
        await ctx.send("Vous ne faites pas parti de la liste des personnes inscrite")


# ajoute un rôle à la composition
@bot.command()
async def add(ctx, arg=None):
    if arg is not None:
        load = get()
        if arg in load['roles']:
            load['compo'][arg] = []
            push(load)
            await ctx.send("Le rôle a bien été ajouté à la composition")
        else:
            await ctx.send("Ce rôle n'existe pas, voici la liste des rôles existant =>")
            embed = discord.Embed(title="Liste des rôles", description="", color=0x6F00F6)
            for rol in list_roles:
                embed.add_field(name=rol, value="⇧", inline=True)
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
            await ctx.send("La composition actuelle est vide, veuillez la remplire avant d'enlever des rôles via la "
                           "commande `/add <role>`")
    else:
        await ctx.send("Veuillez fournir en paramètre le nom du rôle à exclure de la composition")


@bot.command()
async def compo(ctx):
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
        await ctx.send("Veuillez d'abord rajouter des rôles dans la composition via la commande `/add <role>`")


# commence la partie
@bot.command()
async def start(ctx):
    global list_roles_base
    load = get()
    if not load['game']['game_started']:
        if load['game']['nb_player'] >= 1: # A CHANGER
            if load['roles']['total_roles'] <= 3: # A CHANGER
                load = await assignment(ctx)
                load['game']['game_started'] = True
                for rol in list_roles:
                    load['roles'][rol]['nb_now'] = len(load['roles'][rol]['list_player'])
                for rol in load['compo'].keys():
                    if rol != "astro":
                        list_roles_base.append(rol)
                load['game']['nb_alive'] = len(load['list_player'])
                push(load)
                await game(ctx)
            else:
                await ctx.send("Il n'y a pas assez de rôle, veuillez en ajouter via la commande `/add <role>`")
        else:
            await ctx.send("Il n'y a pas assez de joueurs")
    else:
        await ctx.send("Vous ne pouvez pas relancer de partie, une partie est déjà en cours !")


# reinitialise le fichier json
@bot.command()
async def restart(ctx):
    load = get()
    for rol in ctx.guild.roles:
        if rol.name == "Joueur":
            for player in load['player']:
                for m in bot.get_guild(871137122126553100).members:
                    if m.name == player:
                        await m.remove_roles(rol)
                        break
            break
    for channel in ctx.guild.get_channel(load['cat_sporz']).channels:
        await channel.delete()
    for array in cascade_mere:
        load[array] = {}
    for array in body:
        if array == "roles":
            load['roles']['total_roles'] = 0
            for rol in list_roles:
                load['roles'][rol] = body[array]
        else:
            load[array] = body[array]
    push(load)
    await ctx.send("Le restart a bien été effectué, les inscriptions et la composition des rôles peuvent commencer !")


@bot.command()
async def list_role(ctx):
    embed = discord.Embed(title="Liste des rôles", description="", color=0x6F00F6)
    for rol in list_roles:
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
    global keepLooping
    # await ctx.send(get())
    await ctx.send("caca")
    while keepLooping:
        await asyncio.sleep(3)
    await ctx.send("Prout")


@bot.command()
async def test(ctx, arg):
    global keepLooping
    # await create_channel(ctx, "hacker")
    # await timeout(ctx)
    load = get()
    for channel in ctx.guild.get_channel(load["cat_sporz"]).channels:
        await channel.delete()
    push(load)


@bot.command()  # admin command
async def clear(ctx, nb_mess=1):
    # if str(ctx.author) in get_admins(str(ctx.guild)):
    try:
        await ctx.channel.purge(limit=int(nb_mess) + 1)
    except ValueError:
        await ctx.send("Veuillez saisir un nombre")


async def game(ctx):
    global has_win, keepLooping, paralysed, mutate_done, night, list_inspected, balance_mutant, all_voted, eliminate
    load = get()
    overwrites = modif_perm_name(ctx, load['list_player'], False)
    await ctx.guild.create_text_channel('💻🎮Ordinateur-de-bord', category=get_chan(load["cat_sporz"]),
                                        overwrites=overwrites)
    overwrites = modif_perm_role(ctx, "mutant", False)
    await ctx.guild.create_text_channel('Laboratoire des mutants', category=bot.get_channel(load["cat_sporz"]),
                                        overwrites=overwrites)
    overwrites = modif_perm_role(ctx, "medecin", False)
    await ctx.guild.create_text_channel('Pharmacie des médecins', category=get_chan(load["cat_sporz"]),
                                        overwrites=overwrites)
    overwrites = modif_perm_role(ctx, "informaticien", False)
    await ctx.guild.create_text_channel('Bureau des informaticiens',
                                        category=get_chan(load["cat_sporz"]),
                                        overwrites=overwrites)
    overwrites = modif_perm_role(ctx, "psychologue", False)
    await ctx.guild.create_text_channel("Cabinet des psychologues", category=get_chan(load["cat_sporz"]),
                                        overwrites=overwrites)
    overwrites = modif_perm_role(ctx, "espion", False)
    await ctx.guild.create_text_channel("Chambre des espions", category=get_chan(load["cat_sporz"]),
                                        overwrites=overwrites)
    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(connect=False)}
    await ctx.guild.create_voice_channel('Salon-Vocal-Principal', category=get_chan(load["cat_sporz"]),
                                         overwrites=overwrites)
    for channel in get_chan(load["cat_sporz"]).channels:
        if channel.name == "💻🎮ordinateur-de-bord":
            load['list_id_chan']["ordi"] = channel.id
        elif channel.name == "laboratoire-des-mutants":
            load['list_id_chan']["mutant"] = channel.id
        elif channel.name == "pharmacie-des-médecins":
            load['list_id_chan']["medecin"] = channel.id
        elif channel.name == "bureau-des-informaticiens":
            load['list_id_chan']["informaticien"] = channel.id
        elif channel.name == "cabinet-des-psychologues":
            load['list_id_chan']["psychologue"] = channel.id
        elif channel.name == "chambre-des-espions":
            load['list_id_chan']["espion"] = channel.id
        elif channel.name == "Salon-Vocal-Principal":
            load['list_id_chan']["vocal_ch"] = channel.id
    push(load)
    embed = discord.Embed(title="Liste des commandes", description="\"target\" => nom discord du joueur ciblé",
                          color=0x00ff00)
    embed.add_field(name="Muter quelqu'un", value="/mutate target", inline=False)
    embed.add_field(name="Paralyser quelqu'un", value="/paralyze target", inline=False)
    await get_chan(load['list_id_chan']['mutant']).send(embed=embed)
    await get_chan(load['list_id_chan']['mutant']).send("**Veuillez d'abord commencer par muter une personne**")
    embed = discord.Embed(title="Liste des commandes", description="\"target\" => nom discord du joueur ciblé",
                          color=0xffffff)
    embed.add_field(name="Soigner quelqu'un", value="/heal target", inline=False)
    await get_chan(load['list_id_chan']['medecin']).send(embed=embed)
    embed = discord.Embed(title="Liste des commandes", description="\"target\" => nom discord du joueur ciblé",
                          color=0x000000)
    embed.add_field(name="Inspecter quelqu'un", value="/psy target", inline=False)
    await get_chan(load['list_id_chan']['psychologue']).send(embed=embed)
    embed = discord.Embed(title="Liste des commandes", description="\"target\" => nom discord du joueur ciblé",
                          color=0x00ced1)
    embed.add_field(name="Espionner quelqu'un", value="/spy target", inline=False)
    await get_chan(load['list_id_chan']['espion']).send(embed=embed)
    await ctx.send("Le jeu a commencé, veuillez consulter vos messages privés pour prendre connaissance de votre rôle")
    while not has_win:
        night = True
        paralysed = ""
        list_inspected = []
        balance_mutant = 0
        mutate_done = False
        eliminate = ""
        all_voted = False
        load['game']['nb_night'] += 1
        await get_chan(load['list_id_chan']['ordi']).send(f"🌌 **__Nuit n°{load['game']['nb_night']}__** 🌌")
        await get_chan(load['list_id_chan']['mutant']).edit(overwrites=modif_perm_role(ctx, "mutant", True))
        while keepLooping:
            await asyncio.sleep(2)
        keepLooping = True
        await get_chan(load['list_id_chan']['mutant']).edit(overwrites=modif_perm_role(ctx, "mutant", False))
        for rol in list_roles_base:
            await get_chan(load['list_id_chan']['ordi']).send(f"C'est au tour des {rol}s")
            try:
                if load['player'][paralysed]['role'] == rol:
                    l = []
                    for p in load['player']:
                        if p != paralysed:
                            l.append(p)
                    await get_chan(load['list_id_chan'][rol]).edit(overwrites=modif_perm_name(ctx, l, True))
                    await get_chan(load['list_id_chan'][rol]).send(f"{paralysed} est paralysé(e), il/elle ne pourra pas "
                                                                   f"jouer pendant ce tour")
            except KeyError:
                await get_chan(load['list_id_chan'][rol]).edit(overwrites=modif_perm_role(ctx, rol, True))
                if rol == "informaticien":
                    await get_chan(load['list_id_chan'][rol]).send(f"Il y a {load['roles']['mutant']['nb_now']} mutant(s) à bord !")
                    keepLooping = False
                    await asyncio.sleep(random.randint(1, 3)) # A CHANGER
            if load['roles'][rol]['nb_now'] > 0: # A CHANGER
                while keepLooping:
                    await asyncio.sleep(2)
                keepLooping = True
                await get_chan(load['list_id_chan'][rol]).edit(overwrites=modif_perm_role(ctx, rol, False))
            else:
                await asyncio.sleep(random.randint(1, 3)) # A CHANGER
        main = get_chan(load['list_id_chan']['ordi'])
        await main.send("🪐 **Le vaisseau se réveille** 🪐")
        if balance_mutant == 1:
            await main.send("Cette nuit il y a eu **1** nouvelle infectée et **0** personnes soignées")
        elif balance_mutant == -1:
            await main.send("Cette nuit il y a eu **1** nouvelle infectée et **1** personne soignée")
        elif balance_mutant == -3:
            await main.send("Cette nuit il y a eu **1** nouvelle infectée et **2** personnes soignées")
        await ctx.send("__Nous allons donc procéder au vote du vaiseau__")
        lst = []
        for m in get_players():
            if not load['player'][m]['is_dead']:
                lst.append(m)
        await get_chan(load['list_id_chan']['vocal_ch']).edit(overwrites=modif_voc_perm(ctx, lst, True))
        await main.edit(overwrites=modif_perm_name(ctx, lst, True))
        await main.send("Un channel vocal est désormains à votre disposition pour la durée des votes")
        await main.send("La séssion de vote commence donc et ce pour une durée de 2 minutes")
        begin = datetime.datetime.timestamp(datetime.datetime.now())
        now = datetime.datetime.timestamp(datetime.datetime.now())
        while not all_voted and now - begin >= 120:
            now = datetime.datetime.timestamp(datetime.datetime.now())
            await asyncio.sleep(1)
        await get_chan(load['list_id_chan']['vocal_ch']).edit(overwrites=modif_voc_perm(ctx, lst, False))
        msg = await ctx.send("Les votes sont clos, la personne qui sera éliminité est")
        await asyncio.sleep(1)
        await msg.edit("Les votes sont clos, la personne qui sera éliminité est .")
        await asyncio.sleep(1)
        await msg.edit("Les votes sont clos, la personne qui sera éliminité est ..")
        await asyncio.sleep(1)
        await msg.edit("Les votes sont clos, la personne qui sera éliminité est ...")
        await asyncio.sleep(1)
        eliminate = determine_vote(list(load['vote']['list_vote']))
        await msg.edit(f"Les votes sont clos, la personne qui sera éliminité est **__{eliminate}__** !!")
        await asyncio.sleep(2)
        await main.send(f"Le rôle d'**{eliminate}** était : **{load['player'][eliminate]['role']}**")
        await asyncio.sleep(5)
        await main.send(f"Dites tous au revoir à {eliminate} 👋 avant que nous n'ayons plus de lumière du soleil !")
        b_e = load['player'][eliminate]
        b_e['isDead'] = True
        load['roles'][b_e['role']]['list_player'].remove(eliminate)
        load['roles'][b_e['role']]['nb_now'] -= 1
        b_e['role'] = ""
        b_e['role_before'] = ""
        load['game']['nb_alive'] -= 1
        msg = await main.send("*Recherche de victoire 🔎*")
        await asyncio.sleep(1)
        await msg.edit("*Recherche de victoire 🔍.*")
        await asyncio.sleep(1)
        await msg.edit("*Recherche de victoire 🔎..*")
        await asyncio.sleep(1)
        await msg.edit("*Recherche de victoire 🔍...*")
        await asyncio.sleep(1)
        if load['roles']['mutant']['nb_now'] == 0 :
            has_win = True
            await main.send("**__IL N'Y A PLUS DE MUTANT A BORD !! 🛰__**\n**__🎆🎇✨🎊🎉 LES HABITANTS DU VAISSEAU ONT GAGNÉS !! 🎉🎊✨🎇🎆__**")
        else:
            await main.send("La partie continue ... 🤫")
        push(load)
    await main.send("La partie est donc terminé !")
    await main.send("Voici la liste des membres et de leur rôle")
    for p in load['player']:
        if load['player'][p]['is_original_mutant']:
            await main.send(f"{p} était le mutant originel")
        elif load['player'][p]['role'] == "mutant":
            await main.send(f"{p} était mutant et anciennement {load['player'][p]['role_before']}")
        else:
            await main.send(f"{p} était {load['player'][p]['role']}")
    await main.send("**==========**\nLa partie est terminée veuillez faire la commande `/restart` pour en recommencer une !")


@bot.command()
async def mutate(ctx, member=None):
    global mutate_done, balance_mutant
    load = get()
    if ctx.channel.id == load['list_id_chan']['mutant']:
        if not mutate_done:
            if str(ctx.author)[:-5] not in load['vote']['has_voted']:
                if member is not None:
                    if member in get_players():
                        if member not in load['roles']['mutant']['list_player']:
                            load['vote']['list_mutate'].append(member)
                            load['vote']['has_voted'].append(str(ctx.author)[:-5])
                            await ctx.send(f"Votre vote pour muter {member} a bien été pris en compte")
                            if len(load['vote']['list_mutate']) == load['roles']['mutant']['nb_now']:
                                member = determine_vote(load['vote']['list_mutate'])
                                await ctx.send(f"Les vote pour muter sont terminés, la personne mutée sera donc {member}")
                                load['player'][member]['role_before'] = load['player'][member]['role']
                                load['player'][member]['role'] = "mutant"
                                load['roles'][load['player'][member]['role_before']]['nb_now'] -= 1
                                load['roles'][load['player'][member]['role_before']]['list_player'].remove(member)
                                load['roles']['mutant']['list_player'].append(member)
                                load['roles']['mutant']['nb_now'] += 1
                                mutate_done = True
                                balance_mutant += 1
                                load['vote']['has_voted'] = []
                                load['vote']['list_mutate'] = []
                            push(load)
                        else:
                            await ctx.send("Vous ne pouvez pas muter un mutant")
                    else:
                        await ctx.send("Le joueur n'est pas dans la partie, vous pouvez obtenir la liste des joueurs en faisant `/list_player`")
                else:
                    await ctx.send("Veuillez saisir le nom d'un joueur, pour obtenir la liste des joueurs vous pouvez faire `/list_player`")
            else:
                await ctx.send("Vous ne pouvez pas voter 2 fois ( ͠° ͟ʖ ͡°)")
        else:
            await ctx.send("Vous venez de muter quelqu'un, vous ne pouvez pas en muter un deuxième")
    else:
        await ctx.send("Cette commande n'est pas faisable dans ce channel")


@bot.command()
async def paralyze(ctx, member=None):
    global paralysed, mutate_done, keepLooping
    load = get()
    if ctx.channel.id == load['list_id_chan']['mutant']:
        if mutate_done:
            if str(ctx.author)[:-5] not in load['vote']['has_voted']:
                if member is not None:
                    if member in get_players():
                        if member not in load['roles']['mutant']['list_player']:
                            load['vote']['list_paralyze'].append(member)
                            load['vote']['has_voted'].append(str(ctx.author)[:-5])
                            await ctx.send(f"Votre vote pour paralyser {member} a bien été pris en compte")
                            if len(load['vote']['list_paralyze']) == load['roles']['mutant']['nb_now']:
                                member = determine_vote(load['vote']['list_paralyze'])
                                await ctx.send(f"Les votes pour paralyser sont terminés, la personne paralysée sera donc {member}")
                                paralysed = member
                                mutate_done = False
                                load['vote']['has_voted'] = []
                                load['vote']['list_paralyze'] = []
                                keepLooping = False
                            push(load)
                        else:
                            await ctx.send("Vous ne pouvez pas paralyser un mutant")
                    else:
                        await ctx.send("Le joueur n'est pas dans la partie, vous pouvez obtenir la liste des joueurs "
                                       "en faisant `/list_player`")
                else:
                    await ctx.send("Veuillez saisir le nom d'un joueur, pour obtenir la liste des joueurs vous pouvez "
                                   "faire `/list_player`")
            else:
                await ctx.send("Vous ne pouvez pas voter 2 fois ( ͠° ͟ʖ ͡°)")
        else:
            await ctx.send("Veuillez attendre que tout le monde ait voté pour élire la personne à muter")
    else:
        await ctx.send("Cette commande n'est pas faisable dans ce channel")


@bot.command()
async def heal(ctx, member=None):
    global paralysed, keepLooping, balance_mutant
    load = get()
    if ctx.channel.id == load['list_id_chan']['medecin']:
        if str(ctx.author)[:-5] not in load['vote']['has_voted']:
            if member is not None:
                if member in get_players():
                    if member not in load['vote']['list_heal']:
                        load['vote']['list_heal'].append(member)
                        load['vote']['has_voted'].append(str(ctx.author)[:-5])
                        if load['player'][member]['role'] == "mutant":
                            if not load['player'][member]['is_original_mutant']:
                                rol = load['player'][member]['role']
                                load['roles'][rol]['list_player'].remove(member)
                                load['roles'][rol]['nb_now'] -= 1
                                load['player'][member]['role'] = load['player'][member]['role_before']
                                rol = load['player'][member]['role']
                                load['roles'][rol]['list_player'].append(member)
                                load['roles'][rol]['nb_now'] += 1
                                load['player'][member]['role_before'] = ""
                                balance_mutant -= 2
                        await ctx.send(f"{member} est soigné")
                        if len(load['vote']['list_heal']) == load['roles']['medecin']['nb_now']:
                            load['vote']['has_voted'] = []
                            load['vote']['list_heal'] = []
                            keepLooping = False
                        push(load)
                    else:
                        await ctx.send("La personne est déjà soignée")
                else:
                    await ctx.send("Le joueur n'est pas dans la partie, vous pouvez obtenir la liste des joueurs en faisant `/list_player`")
            else:
                await ctx.send("Veuillez saisir le nom d'un joueur, pour obtenir la liste des joueurs vous pouvez faire `/list_player`")
        else:
            await ctx.send("Vous ne pouvez pas soigner 2 fois ( ͠° ͟ʖ ͡°)")
    else:
        await ctx.send("Cette commande n'est pas faisable dans ce channel")


@bot.command()
async def psy(ctx, member=None):
    global paralysed, keepLooping, list_inspected
    load = get()
    if ctx.channel.id == load['list_id_chan']['psychologue']:
        if str(ctx.author)[:-5] not in load['vote']['has_voted']:
            if member is not None:
                if member in get_players():
                    if member not in load['vote']['list_heal']:
                        if load['player'][member]['role'] == "mutant":
                            await ctx.send(f"{member} est mutant 👽")
                        else:
                            await ctx.send(f"{member} n'est pas mutant ✅")
                        load['vote']['has_voted'].append(str(ctx.author)[:-5])
                        load['vote']['list_heal'].append(member)
                        list_inspected.append(member)
                        if len(load['vote']['has_voted']) == load['roles']['psychologue']['nb_now']:
                            load['vote']['has_voted'] = []
                            load['vote']['list_heal'] = []
                            keepLooping = False
                        push(load)
                    else:
                        await ctx.send("La personne a déjà étée inspectée")
                else:
                    await ctx.send("Le joueur n'est pas dans la partie, vous pouvez obtenir la liste des joueurs en faisant `/list_player`")
            else:
                await ctx.send("Veuillez saisir le nom d'un joueur, pour obtenir la liste des joueurs vous pouvez faire `/list_player`")
        else:
            await ctx.send("Vous ne pouvez pas inspecter 2 fois ( ͠° ͟ʖ ͡°)")
    else:
        await ctx.send("Cette commande n'est pas faisable dans ce channel")


@bot.command()
async def spy(ctx, member=None):
    global paralysed, keepLooping
    load = get()
    if ctx.channel.id == load['list_id_chan']['espion']:
        if str(ctx.author)[:-5] not in load['vote']['has_voted']:
            if member is not None:
                if member in get_players():
                    if member not in load['vote']['list_heal']:
                        await ctx.send("**==========**")
                        temp = 0
                        if load['player'][member]['role'] == "mutant":
                            await ctx.send(f"{member} a été(e) muté(e)")
                            temp += 1
                        if member == paralysed:
                            await ctx.send(f"{member} a été(e) paralysé(e)")
                            temp += 1
                        if member in list_inspected:
                            await ctx.send(f"{member} a été(e) inspecté(e)")
                            temp += 1
                        if temp == 0:
                            await ctx.send(f"{member} n'est pas muté(e), paralysé(e) et inspecté(e)")
                        load['vote']['has_voted'].append(str(ctx.author)[:-5])
                        load['vote']['list_heal'].append(member)
                        if len(load['vote']['has_voted']) == load['roles']['espion']['nb_now']:
                            load['vote']['has_voted'] = []
                            load['vote']['list_heal'] = []
                            keepLooping = False
                        push(load)

                    else:
                        await ctx.send("La personne a déjà étée espionnée")
                else:
                    await ctx.send("Le joueur n'est pas dans la partie, vous pouvez obtenir la liste des joueurs en faisant `/list_player`")
            else:
                await ctx.send("Veuillez saisir le nom d'un joueur, pour obtenir la liste des joueurs vous pouvez faire `/list_player`")
        else:
            await ctx.send("Vous ne pouvez pas espionner 2 fois ( ͠° ͟ʖ ͡°)")
    else:
        await ctx.send("Cette commande n'est pas faisable dans ce channel")


@bot.command()
async def vote(ctx, member=None):
    global all_voted
    load = get()
    if ctx.channel.id == load['list_id_chan']['ordi']:
        if str(ctx.author)[:-5] not in load['vote']['has_voted']:
            if member is not None:
                if member in get_players():
                    load['vote']['has_voted'].append(str(ctx.author)[:-5])
                    load['vote']['list_vote'].append(member)
                    if len(load['vote']['has_voted']) == load['roles']['espion']['nb_now']:
                        load['vote']['has_voted'] = []
                        load['vote']['list_vote'] = []
                        all_voted = True
                    push(load)
                else:
                    await ctx.send("Le joueur n'est pas dans la partie, vous pouvez obtenir la liste des joueurs en faisant `/list_player`")
            else:
                await ctx.send("Veuillez saisir le nom d'un joueur, pour obtenir la liste des joueurs vous pouvez faire `/list_player`")
        else:
            await ctx.send("Vous ne pouvez pas espionner 2 fois ( ͠° ͟ʖ ͡°)")
    else:
        await ctx.send("Cette commande n'est pas faisable dans ce channel")


def modif_perm_role(ctx, rol, give):
    load = get()
    perm = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False)}
    for member in load['player']:
        if load['player'][member]['role'] == rol:
            if give:
                perm[ctx.guild.get_member_named(member)] = discord.PermissionOverwrite(read_messages=True,
                                                                                       send_messages=True)
            else:
                perm[ctx.guild.get_member_named(member)] = discord.PermissionOverwrite(read_messages=True,
                                                                                       send_messages=False)
    return perm


def modif_perm_name(ctx, lname, give: bool):
    perm = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False)
    }
    for name in lname:
        if give:
            perm[ctx.guild.get_member_named(name)] = discord.PermissionOverwrite(read_messages=True,
                                                                                 send_messages=True)
        else:
            perm[ctx.guild.get_member_named(name)] = discord.PermissionOverwrite(read_messages=True,
                                                                                 send_messages=False)
    return perm


def modif_voc_perm(ctx, lname, give: bool):
    perm = {
        ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
    }
    for name in lname:
        if give:
            perm[ctx.guild.get_member_named(name)] = discord.PermissionOverwrite(connect=True)
        else:
            perm[ctx.guild.get_member_named(name)] = discord.PermissionOverwrite(connect=False)
    return perm


def get_chan(id):
    return bot.get_channel(id)


def determine_vote(l):
    a = {k: l.count(k) for k in l}
    for z in a:
        if a[z] > 1:
            return a[1]
        else:
            l = list(a.keys())
            return random.choice(l)


bot.run(token)
