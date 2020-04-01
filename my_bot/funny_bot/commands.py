from discord.ext.commands import Cog, command
import requests
from random import randrange
import html

url_api_joke = "https://www.georgeslasaucisse.fr/api/blague"
url_api_series = "https://www.georgeslasaucisse.fr/api/serieblagues"
url_api_chuck = "https://www.chucknorrisfacts.fr/api/get?data=tri:alea"


class FunnyCommands(Cog, name='Commandes Fun'):

    def __init__(self, bot):
        self.bot = bot

    @command(name="salut", help="-> ?salut", ignore_extra=False)
    async def hello(self, ctx):
        await ctx.send("Salut !!! Je suis là pour faire chier")

    @command(name="blague", help="-> ?blague", ignore_extra=False)
    async def joke(self, ctx):
        response = requests.get(url_api_joke)
        joke = response.json()
        await ctx.send(joke['blague'])
        if joke['reponse'] != '':
            await ctx.send(joke['reponse'])

    @command(
        name="avalanche_blague",
        help="-> ?avalanche_blague", ignore_extra=False)
    async def jokes(self, ctx):
        response = requests.get(url_api_series)
        jokes = response.json()
        for joke in jokes:
            await ctx.send(joke['blague'])
            if joke['reponse'] != '':
                await ctx.send(joke['reponse'])

    @command(name="chuck", help="-> ?chuck", ignore_extra=False)
    async def chuck(self, ctx):
        response = requests.get(url_api_chuck)
        jokes = response.json()
        await ctx.send(html.unescape(jokes[randrange(10)]['fact']))
