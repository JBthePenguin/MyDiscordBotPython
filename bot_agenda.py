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
            self.events,
            name='events',
            help='Liste tous les évènements-> !events'))
        self.add_command(commands.Command(
            self.add_event,
            name='add_event',
            help='Ajoute un évènement -> !add_event "Titre" "25/05/20 18:30"'))
        self.add_command(commands.Command(
            self.del_event,
            name='del_event',
            help='Supprime un évènement -> !del_event "Titre"'))
        self.add_command(commands.Command(
            self.event_name,
            name='event_titre',
            help='Modifie le titre -> !event_titre "Titre" "New Titre"'))
        self.add_command(commands.Command(
            self.event_date,
            name='event_date',
            help='Modifie la date -> !event_date "Titre" "25/05/20 18:30"'))
        self.add_command(commands.Command(
            self.event_game,
            name='event_jeu',
            help='Modifie le jeu -> !event_jeu "Titre" "Nom du jeu"'))
        self.add_command(commands.Command(
            self.event_game_master,
            name='event_mj',
            help='Modifie le mj -> !event_mj "Titre" "@MJ1 @MJ2"'))
        self.add_command(commands.Command(
            self.event_group,
            name='event_groupe',
            help='Modifie le groupe -> !event_groupe "Titre" @Groupe"'))
        self.add_command(commands.Command(
            self.event_players,
            name='event_joueurs',
            help='Modifie les joueurs -> !event_joueurs "Titre" "@J1 @J2 ..."'))
        self.add_command(commands.Command(
            self.event_place,
            name='event_lieu',
            help='Modifie le lieu -> !event_lieu "Titre" "Nom du lieu"'))

    def run(self):
        super().run(TOKEN)

    async def on_ready(self):
        """ print in console when bot is started and connected """
        print(f'{self.user} is connected!')

    async def on_command_error(self, ctx, error):
        """ send a message with the error """
        await ctx.send(
            "Commande invalide. !help pour les lister\n" + str(error))

    # Methods used for Events
    def create_event(self, name, date):
        """ check if an event allready exist with this name,
        add created date and save event if it's not in db.json """
        table = self.db.table('Event')
        if table.search(Query().name == name):
            # the event has already been created.
            return "{} existe déjà.".format(name)
        # Datetime that the event was created.
        created_date = datetime.now()
        new_event = {
            'name': name, 'date': date, 'game': '', 'game_master': '',
            'group': '', 'players': '', 'place': '',
            'created_date': str(created_date),
        }
        try:
            # save event
            table.insert(new_event)
            return "'{}' est enregistré.".format(name)
        except ValueError:
            return "J'ai foiré l'enregistrement. Ya un soucis"

    def update_event(self, name, field, value):
        """ update a specific field for an event """
        change_name = False
        if field == 'name':
            table = self.db.table('Event')
            if table.search(Query().name == value):
                # the name has already used.
                return "{} existe déjà.".format(value)
            change_name = True
        event = self.get_event(name)
        if event is False:
            return "Pas d'évènement au nom de '{}'".format(name)
        else:
            table = self.db.table('Event')
            table.update({field: value}, Query().name == name)
            if change_name is True:
                return self.get_event(value)
            return self.get_event(name)

    def delete_event(self, name):
        """ delete a specific event """
        event = self.get_event(name)
        if event is False:
            return "Pas d'évènement au nom de '{}'".format(name)
        else:
            table = self.db.table('Event')
            table.remove(Query().name == name)
            return "'{}' est supprimé.".format(name)

    def get_event(self, name):
        # return a event for a speific name
        table = self.db.table('Event')
        events = table.search(Query().name == name)
        if events == []:
            return False
        else:
            return events[0]

    def get_events(self):
        # return all events
        table = self.db.table('Event')
        return table.all()

    def format_event(self, event):
        """ make a table with an event """
        space = "\n\u200b"
        f_game_master = event['game_master'].replace(' ', '\n')
        f_players = event['players'].replace(' ', '\n')
        embed = discord.Embed(title=event['name'] + space, color=0x38bc35)
        embed.add_field(
            name='Date', value=event['date'] + space, inline=False)
        embed.add_field(
            name='Jeu', value=event['game'] + space, inline=True)
        embed.add_field(
            name='MJ', value=f_game_master + space, inline=True)
        embed.add_field(
            name='Groupe', value=event['group'] + space, inline=True)
        embed.add_field(
            name='Joueurs', value=f_players + space, inline=True)
        embed.add_field(
            name='Lieu', value=event['place'] + space, inline=True)
        return embed

    def check_date_format(self, date):
        """ return true if date format is validated, else False """
        try:
            datetime.strptime(date, '%d/%m/%y %H:%M')
        except ValueError:
            return False
        else:
            return True

    # Commands for Events
    async def add_event(self, ctx, name, date):
        """ create and save an evenment """
        if self.check_date_format(date) is True:
            event_created_msg = self.create_event(name, date)
            await ctx.send(event_created_msg)
            if 'est enregistré.' in event_created_msg:
                event = self.get_event(name)
                await ctx.send(embed=self.format_event(event))
        else:
            await ctx.send("Format date non valide ex: '24/05/20 18:30'")

    async def del_event(self, ctx, name):
        """ create and save an evenment """
        event_deleted_msg = self.delete_event(name)
        await ctx.send(event_deleted_msg)

    async def event_name(self, ctx, name, new_name):
        """ update game_master for a specific event """
        event = self.update_event(name, 'name', new_name)
        if isinstance(event, str):
            await ctx.send(event)
        else:
            await ctx.send(embed=self.format_event(event))

    async def event_date(self, ctx, name, date):
        """ update date for a specific event """
        if self.check_date_format(date) is True:
            event = self.update_event(name, 'date', date)
            if isinstance(event, str):
                await ctx.send(event)
            else:
                await ctx.send(embed=self.format_event(event))
        else:
            await ctx.send("Format date non valide ex: '24/05/20 18:30'")

    async def event_game(self, ctx, name, game):
        """ update game for a specific event """
        event = self.update_event(name, 'game', game)
        if isinstance(event, str):
            await ctx.send(event)
        else:
            await ctx.send(embed=self.format_event(event))

    async def event_game_master(self, ctx, name, game_master):
        """ update game_master for a specific event """
        event = self.update_event(name, 'game_master', game_master)
        if isinstance(event, str):
            await ctx.send(event)
        else:
            await ctx.send(embed=self.format_event(event))

    async def event_group(self, ctx, name, group):
        """ update group for a specific event """
        event = self.update_event(name, 'group', group)
        if isinstance(event, str):
            await ctx.send(event)
        else:
            await ctx.send(embed=self.format_event(event))

    async def event_players(self, ctx, name, players):
        """ update players for a specific event """
        event = self.update_event(name, 'players', players)
        if isinstance(event, str):
            await ctx.send(event)
        else:
            await ctx.send(embed=self.format_event(event))

    async def event_place(self, ctx, name, place):
        """ update place for a specific event """
        event = self.update_event(name, 'place', place)
        if isinstance(event, str):
            await ctx.send(event)
        else:
            await ctx.send(embed=self.format_event(event))

    async def events(self, ctx):
        """ send all events """
        events = self.get_events()
        if events == []:
            await ctx.send("Aucun évènement enregistré")
        else:
            # sorted event by date
            events.sort(key=lambda event: datetime.strptime(
                event['date'], '%d/%m/%y %H:%M'))
            for event in events:
                await ctx.send(embed=self.format_event(event))


bot = MyBot()
bot.run()
