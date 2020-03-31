from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog, command

# Configurations of commands -> [[name, help], [name, help], ...]
confs = [
    ['events', 'Tous les events-> !events'],
    ['events_a_venir', 'Les events à venir-> !events_a_venir'],
    ['events_passe', 'Les events passés-> !events_passe'],
    ['events_apres', 'Les events après une date -> !events_apres "25/05/20"'],
    ['events_avant', 'Les events avant une date -> !events_avant "25/05/20"'],
    ['voir_event', 'Affiche un event-> !voir_event "Titre"'],
    ['add_event', 'Ajoute un event -> !add_event "Titre" "25/05/20 18:30"'],
    ['del_event', 'Supprime un event -> !del_event "Titre"'],
    ['event_titre', 'Modifie le titre -> !event_titre "Titre" "New Titre"'],
    ['event_date', 'Modifie la date -> !event_date "Titre" "25/05/20 18:30"'],
    ['event_jeu', 'Modifie le jeu -> !event_jeu "Titre" "Nom du jeu"'],
    ['event_mj', 'Modifie le mj -> !event_mj "Titre" "@MJ1 @MJ2"'],
    ['event_groupe', 'Modifie le groupe -> !event_groupe "Titre" @Groupe"'],
    [
        'event_joueurs',
        'Modifie les joueurs -> !event_joueurs "Titre" "@J1 @J2 ..."'],
    ['event_lieu', 'Modifie le lieu -> !event_lieu "Titre" "Nom du lieu"']]


class EventCommands(Cog, name='Commandes Event'):

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

    def format_event(self, event):
        """ make an embed with an event and return it"""
        space = "\n\u200b"
        f_game_master = event['game_master'].replace(' ', '\n')
        f_players = event['players'].replace(' ', '\n')
        embed = Embed(title=event['name'] + space, color=0x38bc35)
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

    # commands without params
    @command(name=confs[0][0], help=confs[0][1], ignore_extra=False)
    async def events(self, ctx):
        """ send all events """
        # sorted_events = self.bot.db.table('Event').all()
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
            # no events
            await ctx.send(sorted_events)
        else:
            for event in sorted_events:
                await ctx.send(embed=self.format_event(event))
