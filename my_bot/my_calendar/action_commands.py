from datetime import datetime
from discord.ext.commands import Cog, command
from tinydb import Query
from validator_collection import checkers
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError

confs = [
    ['init_event', 'Init an event-> #init_event id_without_space'],
    ['add_event', 'Add event to the list-> #add_event id'],
    ['del_event', 'Delete an event -> #del_event id'],
    ['e_title', 'Update title -> #e_title id "New Title"'],
    ['e_descr', 'Update description -> #e_descr id "New Description"'],
    ['e_url', 'Update url -> #e_url id https://newurl.com'],
    ['e_start_date', 'Update start date -> #e_start_date id 2020/12/31'],
    ['e_start_time', 'Update start time -> #e_start_time id 8:00PM'],
    ['e_end_date', 'Update end date -> #e_end_date id 2020/12/31'],
    ['e_end_time', 'Update end time -> #e_end_time id 8:00PM'],
    ['e_thumb', 'Update thumbnail url -> #e_thumb id https://url.com/thumb.png'],
    ['e_img', 'Update image url -> #e_img id https://url.com/img.png'],
    ['e_zone', 'Update timezone -> #e_zone id Europe/Paris'],
    ['e_loc', 'Update location -> #e_loc id "The place to be"']]


class EventActionCommands(
        Cog, name='Commands "Init, Add, Update, Delete" Event'):

    def __init__(self, bot):
        self.bot = bot

    # init add delete commands
    @command(name=confs[0][0], help=confs[0][1], ignore_extra=False)
    async def init_event(self, ctx, event_id):
        if " " in event_id:
            await ctx.send("id not accept space")
        elif self.bot.db.table(
                'Event').get(Query().id == event_id) is not None:
            await ctx.send("{} : id already used".format(event_id))
        else:
            # Create new event and save it
            new_event = {
                'id': event_id, 'guild_id': ctx.message.channel.guild.id,
                'member_id': ctx.message.author.id,
                'timestamp': str(ctx.message.created_at),
                'title': False, 'url': False, 'description': False,
                # 'thumbnail_url': 'https://placehold.it/150x150',
                # 'image_url': 'https://placehold.it/400x200', 'start_date': False,
                'thumbnail_url': '', 'image_url': '', 'start_date': False,
                'start_time': False, 'end_date': False, 'end_time': False,
                'zone': False, 'location': False, 'add_list': False}
            self.bot.db.table('Event').insert(new_event)
            await ctx.send(
                "Ok! to see -> #event {}".format(event_id))

    # @command(name=confs[1][0], help=confs[1][1], ignore_extra=False)
    # async def add_event(self, ctx, name, date):
    #     """ create and save an evenment """
    #     if self.check_date_format(date) is True:
    #         if self.bot.db.table('Event').search(Query().name == name):
    #             await ctx.send("{} existe déjà.".format(name))  # already exist
    #         else:
    #             # Create new event with datetime that it was created.
    #             new_event = {
    #                 'name': name, 'date': date, 'game': '', 'game_master': '',
    #                 'group': '', 'players': '', 'place': '',
    #                 'created_date': str(datetime.now())}
    #             self.bot.db.table('Event').insert(new_event)  # save event
    #             await ctx.send(
    #                 "Ok! pour voir-> !voir_event \"{}\"".format(name))
    #     else:
    #         await ctx.send("Format date non valide ex: '24/05/20 18:30'")

    @command(name=confs[2][0], help=confs[2][1], ignore_extra=False)
    async def del_event(self, ctx, event_id):
        """ delete an event """
        Event = Query()
        if self.bot.db.table('Event').get(Event.id == event_id) is None:
            await ctx.send("No event founded with id {}".format(event_id))
        else:
            self.bot.db.table('Event').remove(Event.id == event_id)
            await ctx.send("{} deleted".format(event_id))

    # update commands
    def check_date_time_format(self, date_time):
        """ return true if date or time format is validated, else False """
        try:
            datetime.strptime(date_time, '%Y/%m/%d %H:%M%p')
        except ValueError:
            return False
        else:
            return True

    def update_event(self, event_id, field, value, timestamp):
        """ check if event id exist, if value is date or time check format,
        if time check if date exist, update a specific field for an event """
        Event = Query()
        event_updated = self.bot.db.table('Event').get(Event.id == event_id)
        if event_updated is None:
            return "No event founded with id {}".format(event_id)
        if '_date' in field:
            if ('end_' in field) and (
                    event_updated[field.replace('end', 'start')] is False):
                return "Set a value for {} before {}".format(
                    field.replace('end', 'start'), field)
            try:
                e_date = datetime.strptime(value, '%Y/%m/%d')
                if ('end_' in field) and (e_date < datetime.strptime(
                        event_updated[
                            field.replace('end', 'start')], '%Y/%m/%d')):
                    return "{} can't be set before {}".format(
                        field, event_updated[field.replace('end', 'start')])
            except ValueError:
                return "date format not valid -> 2020/12/31"
        if '_time' in field:
            if event_updated[field.replace('time', 'date')] is False:
                return "Set a value for {} before {}".format(
                    field.replace('time', 'date'), field)
            if ('end_' in field) and (
                    event_updated[field.replace('end', 'start')] is False):
                return "Set a value for {} before {}".format(
                    field.replace('end', 'start'), field)
            try:
                e_time = datetime.strptime(value, '%H:%M%p')
                if ('end_' in field) and (event_updated[
                        'start_date'] == event_updated['end_date']) and (
                            e_time <= datetime.strptime(event_updated[
                                field.replace('end', 'start')], '%H:%M%p')):
                    return "{} must be set after {}".format(
                        field, event_updated[field.replace('end', 'start')])
            except ValueError:
                return "time format not valid -> 8:00PM"
        self.bot.db.table('Event').update({field: value}, Event.id == event_id)
        self.bot.db.table('Event').update(
            {'timestamp': str(timestamp)}, Event.id == event_id)
        return "Ok, {} updated! to see -> #event {}".format(field, event_id)

    @command(name=confs[3][0], help=confs[3][1], ignore_extra=False)
    async def e_title(self, ctx, event_id, title):
        """ update title for a specific event """
        await ctx.send(self.update_event(
            event_id, 'title', title, ctx.message.created_at))

    @command(name=confs[4][0], help=confs[4][1], ignore_extra=False)
    async def e_descr(self, ctx, event_id, description):
        """ update description for a specific event """
        await ctx.send(self.update_event(
            event_id, 'description', description, ctx.message.created_at))

    @command(name=confs[5][0], help=confs[5][1], ignore_extra=False)
    async def e_url(self, ctx, event_id, url):
        """ update url for a specific event """
        if checkers.is_url(url) is False:
            await ctx.send("url format not valid -> https://newurl.com")
        else:
            await ctx.send(self.update_event(
                event_id, 'url', url, ctx.message.created_at))

    @command(name=confs[6][0], help=confs[6][1], ignore_extra=False)
    async def e_start_date(self, ctx, event_id, e_date):
        """ update start_date for a specific event """
        await ctx.send(self.update_event(
            event_id, 'start_date', e_date, ctx.message.created_at))

    @command(name=confs[7][0], help=confs[7][1], ignore_extra=False)
    async def e_start_time(self, ctx, event_id, e_time):
        """ update start_time for a specific event """
        await ctx.send(self.update_event(
            event_id, 'start_time', e_time, ctx.message.created_at))

    @command(name=confs[8][0], help=confs[8][1], ignore_extra=False)
    async def e_end_date(self, ctx, event_id, e_date):
        """ update end_date for a specific event """
        await ctx.send(self.update_event(
            event_id, 'end_date', e_date, ctx.message.created_at))

    @command(name=confs[9][0], help=confs[9][1], ignore_extra=False)
    async def e_end_time(self, ctx, event_id, e_time):
        """ update end_time for a specific event """
        await ctx.send(self.update_event(
            event_id, 'end_time', e_time, ctx.message.created_at))

    @command(name=confs[10][0], help=confs[10][1], ignore_extra=False)
    async def e_thumb(self, ctx, event_id, url):
        """ update url for a specific event """
        if checkers.is_url(url) is False:
            await ctx.send("url format not valid -> https://newurl.com")
        else:
            await ctx.send(self.update_event(
                event_id, 'thumbnail_url', url, ctx.message.created_at))

    @command(name=confs[11][0], help=confs[11][1], ignore_extra=False)
    async def e_img(self, ctx, event_id, url):
        """ update url for a specific event """
        if checkers.is_url(url) is False:
            await ctx.send("url format not valid -> https://newurl.com")
        else:
            await ctx.send(self.update_event(
                event_id, 'image_url', url, ctx.message.created_at))

    @command(name=confs[12][0], help=confs[12][1], ignore_extra=False)
    async def e_zone(self, ctx, event_id, e_timezone):
        """ update timezone for a specific event """
        try:
            timezone(e_timezone)
        except UnknownTimeZoneError:
            await ctx.send("".join([
                "timezone not valid, to see a list -> ",
                "https://github.com/JBthePenguin/MyDiscordBotPython/blob/",
                "master/my_bot/my_calendar/pytz_timezones_list.txt"]))
        else:
            await ctx.send(self.update_event(
                event_id, 'zone', e_timezone, ctx.message.created_at))

    @command(name=confs[13][0], help=confs[13][1], ignore_extra=False)
    async def e_location(self, ctx, event_id, location):
        """ update location for a specific event """
        await ctx.send(self.update_event(
            event_id, 'location', location, ctx.message.created_at))
    #
    # @command(name=confs[3][0], help=confs[3][1], ignore_extra=False)
    # async def event_date(self, ctx, name, date):
    #     """ update date for a specific event """
    #     if self.check_date_format(date) is True:
    #         await ctx.send(self.update_event(name, 'date', date))
    #     else:
    #         await ctx.send("Format date non valide ex: '24/05/20 18:30'")
    #
    # @command(name=confs[4][0], help=confs[4][1], ignore_extra=False)
    # async def event_game(self, ctx, name, game):
    #     """ update game for a specific event """
    #     await ctx.send(self.update_event(name, 'game', game))
    #
    # @command(name=confs[5][0], help=confs[5][1], ignore_extra=False)
    # async def event_game_master(self, ctx, name, game_master):
    #     """ update game master for a specific event """
    #     await ctx.send(self.update_event(name, 'game_master', game_master))
    #
    # @command(name=confs[6][0], help=confs[6][1], ignore_extra=False)
    # async def event_group(self, ctx, name, group):
    #     """ update group for a specific event """
    #     await ctx.send(self.update_event(name, 'group', group))
    #
    # @command(name=confs[7][0], help=confs[7][1], ignore_extra=False)
    # async def event_players(self, ctx, name, players):
    #     """ update players for a specific event """
    #     await ctx.send(self.update_event(name, 'players', players))
    #
    # @command(name=confs[8][0], help=confs[8][1], ignore_extra=False)
    # async def event_place(self, ctx, name, place):
    #     """ update place for a specific event """
    #     await ctx.send(self.update_event(name, 'place', place))
