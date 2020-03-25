import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')


@bot.command(name='jet_de_des', help='Simulation de jet de dés, nbre de dés et nombres de face.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


bot.run(TOKEN)

# client = discord.Client()


# @client.event
# async def on_ready():
#     guild = discord.utils.get(client.guilds, name=GUILD)

#     print(
#         f'{client.user} is connected to the following guild:\n'
#         f'{guild.name}(id: {guild.id})'
#     )

#     members = '\n - '.join([member.name for member in guild.members])
#     print(f'Guild Members:\n - {members}')


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content == 'Salut Bottine comment ça va?':
#         response = "Qu'est-ce que ça peut foutre, et c'est quoi ce nom de merde"
#         await message.channel.send(response)


# client.run(TOKEN)
