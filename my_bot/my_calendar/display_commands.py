from datetime import datetime
# from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog, command
from tinydb import Query

# Configurations of commands -> [[name, help], [name, help], ...]
confs = [
    ['events', 'Tous les events-> !events'],
    ['events_a_venir', 'Les events à venir-> !events_a_venir'],
    ['events_passe', 'Les events passés-> !events_passe'],
    ['events_apres', 'Les events après une date -> !events_apres "25/05/20"'],
    ['events_avant', 'Les events avant une date -> !events_avant "25/05/20"'],
    ['voir_event', 'Affiche un event-> !voir_event "Titre"']]


class EventDisplayCommands(Cog, name='Commandes Affichage Event'):

    def __init__(self, bot):
        self.bot = bot

    def sort_events(self, events, no_msg):
        """ return no events message if list is empty
        or a sorted event list with it if not """
        if events == []:
            return "Aucun évènement {}".format(no_msg)
        else:
            # return sorted events by date
            events.sort(key=lambda event: datetime.strptime(
                event['date'], '%d/%m/%y %H:%M'))
            return events

    def get_events_since_date(self, date, after=True):
        # return all events before or after a date """
        all_events = self.bot.db.table('Event').all()
        selected_events = []
        if after is True:
            for event in all_events:
                if datetime.strptime(event['date'], '%d/%m/%y %H:%M') >= date:
                    selected_events.append(event)
        else:
            for event in all_events:
                if datetime.strptime(event['date'], '%d/%m/%y %H:%M') <= date:
                    selected_events.append(event)
        return selected_events

    def check_date_format(self, date):
        """ return true if date format is validated, else False """
        try:
            datetime.strptime(date, '%d/%m/%y')
        except ValueError:
            return False
        else:
            return True

    def format_event(self, event):
        """ make an embed with an event and return it"""
        spc = "\n\u200b"
        f_game_master = event['game_master'].replace(' ', '\n')
        f_players = event['players'].replace(' ', '\n')
        embed = Embed(title=event['name'] + spc, color=0x38bc35)
        embed.add_field(name='Date', value=event['date'] + spc, inline=False)
        embed.add_field(name='Jeu', value=event['game'] + spc, inline=True)
        embed.add_field(name='MJ', value=f_game_master + spc, inline=True)
        embed.add_field(name='Groupe', value=event['group'] + spc, inline=True)
        embed.add_field(name='Joueurs', value=f_players + spc, inline=True)
        embed.add_field(name='Lieu', value=event['place'] + spc, inline=True)
        return embed

    # commands without params
    @command(name=confs[0][0], help=confs[0][1], ignore_extra=False)
    async def events(self, ctx):
        """ send all events """
        sorted_events = self.sort_events(
            self.bot.db.table('Event').all(), 'enregistré')
        if isinstance(sorted_events, str):
            # no events
            await ctx.send(sorted_events)
        else:
            for event in sorted_events:
                await ctx.send(embed=self.format_event(event))

    @command(name=confs[1][0], help=confs[1][1], ignore_extra=False)
    async def events_future(self, ctx):
        """ send all upcoming events """
        sorted_events = self.sort_events(
            self.get_events_since_date(datetime.now()), 'à venir')
        if isinstance(sorted_events, str):
            # no events
            await ctx.send(sorted_events)
        else:
            for event in sorted_events:
                await ctx.send(embed=self.format_event(event))

    @command(name=confs[2][0], help=confs[2][1], ignore_extra=False)
    async def events_past(self, ctx):
        """ send all past events """
        sorted_events = self.sort_events(
            self.get_events_since_date(datetime.now(), after=False), 'passé')
        if isinstance(sorted_events, str):
            await ctx.send(sorted_events)  # no event
        else:
            for event in sorted_events:
                await ctx.send(embed=self.format_event(event))

    # commands with params
    @command(name=confs[3][0], help=confs[3][1], ignore_extra=False)
    async def events_after(self, ctx, date):
        """ send all events since a date """
        if self.check_date_format(date) is True:
            sorted_events = self.sort_events(self.get_events_since_date(
                datetime.strptime(date, '%d/%m/%y')), 'après {}'.format(date))
            if isinstance(sorted_events, str):
                await ctx.send(sorted_events)  # no events
            else:
                for event in sorted_events:
                    await ctx.send(embed=self.format_event(event))
        else:
            await ctx.send("Format date non valide ex: '24/05/20'")

    @command(name=confs[4][0], help=confs[4][1], ignore_extra=False)
    async def events_before(self, ctx, date):
        """ send all events before a date """
        if self.check_date_format(date) is True:
            sorted_events = self.sort_events(self.get_events_since_date(
                datetime.strptime(date, '%d/%m/%y'), after=False),
                'avant {}'.format(date))
            if isinstance(sorted_events, str):
                await ctx.send(sorted_events)  # no events
            else:
                for event in sorted_events:
                    await ctx.send(embed=self.format_event(event))
        else:
            await ctx.send("Format date non valide ex: '24/05/20'")

    @command(name=confs[5][0], help=confs[5][1], ignore_extra=False)
    async def show_event(self, ctx, name):
        """ send all events """
        event = self.bot.db.table('Event').search(Query().name == name)
        if event == []:
            await ctx.send('No Event "{}"'.format(name))
        else:
            await ctx.send(embed=self.format_event(event[0]))
