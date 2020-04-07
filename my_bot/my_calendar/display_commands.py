from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog, command
from tinydb import Query

# Configurations of commands -> [[name, help], [name, help], ...]
confs = [
    ['events', 'All events-> #events'],
    ['up_events', 'Upcoming events-> #up_events'],
    ['past_events', 'Past events-> #past_events'],
    ['events_after', 'Events after a date -> #events_after 2020-12-31'],
    ['events_before', 'Events before a date -> #events_before 2020-12-31'],
    ['event', 'Display an event-> #event id']]


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
        """ make an embed for an event"""
        if event['title'] is False:
            event['title'] = Embed.Empty
        embed = Embed(title=event['title'], color=0xff0000)
        if event['url'] is False:
            event['url'] = Embed.Empty
        embed.url = event['url']
        if event['description'] is False:
            event['description'] = Embed.Empty
        embed.description = event['description']
        embed.timestamp = datetime.strptime(
            event['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        embed.set_author(
            #  name=self.bot.user.name,
            #  icon_url=self.bot.user.avatar_url)
            name="CalendarBot",
            icon_url="".join([
                "https://raw.githubusercontent.com/JBthePenguin",
                "/MyDiscordBotPython/master/my_bot/my_calendar/icon.png"]))
        embed.set_thumbnail(url=event['thumbnail_url'])
        embed.set_image(url=event['image_url'])
        member = self.bot.get_user(event['member_id'])
        embed.set_footer(
            text=member.name,
            icon_url=member.avatar_url)
        if event['start_date'] is False:
            value = '\u200b'
        else:
            value = event['start_date']
        embed.add_field(
            name='Start date', value=value, inline=True)
        if event['start_time'] is False:
            embed.add_field(name='\u200b', value='\u200b', inline=True)
        else:
            embed.add_field(
                name='Start time', value=event['start_time'], inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        if event['end_date'] is False:
            embed.add_field(name='\u200b', value='\u200b', inline=True)
        else:
            embed.add_field(
                name='End date', value=event['end_date'], inline=True)
        if event['end_time'] is False:
            embed.add_field(name='\u200b', value='\u200b', inline=True)
        else:
            embed.add_field(
                name='End time', value=event['end_time'], inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        if event['time_zone'] is False:
            embed.add_field(name='\u200b', value='\u200b', inline=True)
        else:
            embed.add_field(
                name='Time zone', value=event['time_zone'], inline=True)
        if event['location'] is False:
            embed.add_field(name='\u200b', value='\u200b', inline=True)
        else:
            embed.add_field(
                name='Location', value=event['location'], inline=True)
        embed.add_field(
            name='Event id', value=event['id'], inline=False)
        return embed

    # commands without params
    # @command(name=confs[0][0], help=confs[0][1], ignore_extra=False)
    # async def events(self, ctx):
    #     """ send all events """
    #     sorted_events = self.sort_events(
    #         self.bot.db.table('Event').all(), 'enregistré')
    #     if isinstance(sorted_events, str):
    #         # no events
    #         await ctx.send(sorted_events)
    #     else:
    #         for event in sorted_events:
    #             await ctx.send(embed=self.format_event(event))
    #
    # @command(name=confs[1][0], help=confs[1][1], ignore_extra=False)
    # async def events_future(self, ctx):
    #     """ send all upcoming events """
    #     sorted_events = self.sort_events(
    #         self.get_events_since_date(datetime.now()), 'à venir')
    #     if isinstance(sorted_events, str):
    #         # no events
    #         await ctx.send(sorted_events)
    #     else:
    #         for event in sorted_events:
    #             await ctx.send(embed=self.format_event(event))
    #
    # @command(name=confs[2][0], help=confs[2][1], ignore_extra=False)
    # async def events_past(self, ctx):
    #     """ send all past events """
    #     sorted_events = self.sort_events(
    #         self.get_events_since_date(datetime.now(), after=False), 'passé')
    #     if isinstance(sorted_events, str):
    #         await ctx.send(sorted_events)  # no event
    #     else:
    #         for event in sorted_events:
    #             await ctx.send(embed=self.format_event(event))
    #
    # # commands with params
    # @command(name=confs[3][0], help=confs[3][1], ignore_extra=False)
    # async def events_after(self, ctx, date):
    #     """ send all events since a date """
    #     if self.check_date_format(date) is True:
    #         sorted_events = self.sort_events(self.get_events_since_date(
    #             datetime.strptime(date, '%d/%m/%y')), 'après {}'.format(date))
    #         if isinstance(sorted_events, str):
    #             await ctx.send(sorted_events)  # no events
    #         else:
    #             for event in sorted_events:
    #                 await ctx.send(embed=self.format_event(event))
    #     else:
    #         await ctx.send("Format date non valide ex: '24/05/20'")
    #
    # @command(name=confs[4][0], help=confs[4][1], ignore_extra=False)
    # async def events_before(self, ctx, date):
    #     """ send all events before a date """
    #     if self.check_date_format(date) is True:
    #         sorted_events = self.sort_events(self.get_events_since_date(
    #             datetime.strptime(date, '%d/%m/%y'), after=False),
    #             'avant {}'.format(date))
    #         if isinstance(sorted_events, str):
    #             await ctx.send(sorted_events)  # no events
    #         else:
    #             for event in sorted_events:
    #                 await ctx.send(embed=self.format_event(event))
    #     else:
    #         await ctx.send("Format date non valide ex: '24/05/20'")

    @command(name=confs[5][0], help=confs[5][1], ignore_extra=False)
    async def event(self, ctx, event_id):
        """ send an event in embed """
        if " " in event_id:
            await ctx.send("id not accept space")
        else:
            event = self.bot.db.table('Event').get(Query().id == event_id)
            if event is None:
                await ctx.send("No event founded with id {}".format(event_id))
            else:
                await ctx.send(embed=self.format_event(event))
