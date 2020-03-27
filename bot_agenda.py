import os
from datetime import datetime
import discord
from dotenv import load_dotenv
from discord.ext import commands
from tinydb import TinyDB, Query


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


class MyBot(commands.Bot):
    """ Custom Bot, subclass discord.ext.commands.Bot """

    def __init__(self):
        """ init discord.ext.commands.Bot and add custom commands """
        super().__init__(command_prefix="!")
        # add json db
        self.db = TinyDB("db.json")
        # add commands
        self.add_command(commands.Command(
            self.add_event,
            name='add_event',
            help='-> !add_event Teuf "le jeu" "@j1, @j2, ..." "@MDJ" "@Estreval" "ici ou là" "01/03/20 18:30"'))
        self.add_command(commands.Command(
            self.events,
            name='events',
            help='-> !events'))

    def run(self):
        super().run(TOKEN)

    # Events
    async def on_ready(self):
        """ print in console when bot is started and connected """
        print(f'{self.user} is connected!')

    async def on_command_error(self, ctx, error):
        """ send a message with the error """
        if isinstance(error, commands.errors.CommandNotFound):
            # command not found
            await ctx.send(
                "Commande invalide. !help pour les lister")

    # Commands

    def create_event(
            self, name, game, players, game_master, group, place, date):
        """ check inputs and save event if it's ok in db.json """
        table = self.db.table('Event')
        if table.search(Query().name == name):
            # the event has already been created.
            return "{} existe déjà.".format(name)
        # check date format
        try:
            datetime.strptime(date, '%d/%m/%y %H:%M')
        except ValueError:
            return "Format date non valide ex: '24/05/20 18:30'"
        # Datetime that the event was created.
        created_date = datetime.now()
        new_event = {
            'name': name, 'game': game, 'players': players,
            'game_master': game_master, 'group': group, 'place': place,
            'date': date, 'created_date': str(created_date),
        }
        try:
            # save event
            table.insert(new_event)
            return "{} est enregistré.".format(name)
        except ValueError:
            return "J'ai foiré l'enregistrement. Ya un soucis"

    def get_event(self, name):
        # return a event for a speific name
        table = self.db.table('Event')
        events = table.search(Query().name == name)
        return events[0]

    def get_events(self):
        # return all events
        table = self.db.table('Event')
        return table.all()

    def format_event(self, event):
        """ make a table with an event """
        f_players = event['players'].replace(', ', '\n')
        embed = discord.Embed(title=event['name'], color=0x38bc35)
        embed.add_field(name='Jeu', value=event['game'], inline=True)
        embed.add_field(name='Joueurs', value=f_players, inline=True)
        embed.add_field(name='MJ', value=event['game_master'], inline=True)
        embed.add_field(name='Groupe', value=event['group'], inline=True)
        embed.add_field(name='Lieu', value=event['place'], inline=True)
        embed.add_field(name='Date', value=event['date'], inline=True)
        return embed

    async def add_event(
            self, ctx, name, game, players, game_master, group, place, date):
        """ create and save an evenment """
        event_created_msg = self.create_event(
            name, game, players, game_master, group, place, date)
        await ctx.send(event_created_msg)
        if 'est enregistré.' in event_created_msg:
            event = self.get_event(name)
            await ctx.send(embed=self.format_event(event))

    async def events(self, ctx):
        """ send all events """
        events = self.get_events()
        for event in events:
            await ctx.send(embed=self.format_event(event))


bot = MyBot()
bot.run()
