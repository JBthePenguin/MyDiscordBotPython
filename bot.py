import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

# Events


@bot.event
async def on_ready():
    """ print in console when bot is started and connected """
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user} is connected to the following guild: {guild.name}')
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_command_error(ctx, error):
    """ send a message with the error """
    if isinstance(error, commands.errors.CommandNotFound):
        # command not found
        await ctx.send(
            "Cette commande n'existe pas, !help pour lister les commandes disponibles")

# Commands


@bot.command(name='list_membres', help='liste de tous les membres')
async def list_membres(ctx):
    """ send a message with the list of all members """
    guild = discord.utils.get(bot.guilds, name=GUILD)
    members = '\n - '.join([member.name for member in guild.members])
    message = f'Membres de la guilde {guild.name}:\n - {members}'
    await ctx.send(message)


@bot.command(name='list_salons', help='liste de tous les salons par catégorie')
async def list_salons(ctx):
    """ send a message with the list of channels by category """
    guild = discord.utils.get(bot.guilds, name=GUILD)
    categories = guild.by_category()
    messages = []
    for category in categories:
        channels = '\n - '.join([channel.name for channel in category[1]])
        messages.append(f'{category[0].name}:\n - {channels}')
    # channels = '\n - '.join([channel.name for channel in GUILD.channels])
    for message in messages:
        await ctx.send(message)


@bot.command(name='list_membres_salon', help=(
    'liste les membres autorisés à aller sur un salon. Paramètre: nom du salon'))
async def list_membres_salon(ctx, channel_name):
    """ send a message with the list of members
    who have permission for a channel"""
    guild = discord.utils.get(bot.guilds, name=GUILD)
    # get channel
    channel = discord.utils.get(guild.channels, name=channel_name)
    if channel is None:
        # no channel with this name
        message = f'Te fous pas de moi, pas de salon {channel_name}'
    else:
        # list authorized members
        auth_members = []
        for member in guild.members:
            permissions = channel.permissions_for(member)
            if permissions.view_channel:
                auth_members.append(member)
        if auth_members == []:
            message = f'Aucun membre autorisé à utiliser le salon {channel.name}'
        else:
            members = '\n - '.join([member.name for member in auth_members])
            message = f'{channel.name}\n - {members}'
    await ctx.send(message)


@bot.command(name='list_roles', help=(
    'liste les différents rôles de la guilde.'))
async def list_roles(ctx):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    roles = '\n - '.join([role.name for role in guild.roles])
    message = f'Rôles de la guilde {guild.name}:\n - {roles}'
    await ctx.send(message)


@bot.command(name='list_membres_role', help=(
    'liste les membres pour un rôle donné. Paramètre: nom du rôle'))
async def list_membres_role(ctx, role_name):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        # no role with this name
        message = f'Pas de rôle {role_name}, soit tu le crées, soit tu me demandes un rôle qui existe'
    else:
        role_members = []
        for member in guild.members:
            if role in member.roles:
                role_members.append(member)
        if role_members == []:
            message = f'Aucun membre avec le rôle {role.name}'
        else:
            members = '\n - '.join([member.name for member in role_members])
            message = f'{role.name}\n - {members}'
    await ctx.send(message)


bot.run(TOKEN)
