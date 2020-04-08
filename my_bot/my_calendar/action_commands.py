from datetime import datetime
from discord.ext.commands import Cog, command
from tinydb import Query
from validator_collection import checkers
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError

# Configurations of commands -> [[name, help], [name, help], ...]
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
    ['e_thum', 'Update thumbnail url -> #e_thum id https://url.com/thumb.png'],
    ['e_img', 'Update image url -> #e_img id https://url.com/img.png'],
    ['e_zone', 'Update timezone -> #e_zone id Europe/Paris'],
    ['e_loc', 'Update location -> #e_loc id "The place to be"']]
# Formats -> {'name': 'format'}
formats = {
    'date': '%Y/%m/%d', 'time': '%H:%M%p'}
# Success messages -> {name: message, ...}
success_msgs = {
    'init': "Init Ok! to see -> #event {}",  # {} -> event_id
    'delete': "Ok! {} is now deleted",  # {} -> event_id
    'date_format': "date format not valid -> 2020/12/31", }
# Error messages -> {name: message, ...}
error_msgs = {
    'no_space_id': "No space for event id",
    'id_used': "{} is already used, choose another id",  # {} -> event_id
    'no_event': "No event founded with id {}",  # {} -> event_id
    'date_format': "date format not valid -> 2020/12/31", }


class EventActionCommands(Cog, name='Commands Init Add Update Delete Event'):

    def __init__(self, bot):
        self.bot = bot

    # checkers methods
    def get_event(self, event_id):
        """ get event in db: return None or the event"""
        return self.bot.db.table('Event').get(Query().id == event_id)

    def check_date_time(self, check_value, check_format):
        """ check date or time format: return True or False """
        try:
            datetime.strptime(check_value, check_format)
        except ValueError:
            return False
        return True

    # init add delete commands
    @command(name=confs[0][0], help=confs[0][1], ignore_extra=False)
    async def init_event(self, ctx, event_id):
        """ check if there is space in event id and
        save new event if event id is not already used """
        if " " in event_id:  # space not acepted in id
            await ctx.send(error_msgs['no_space_id'])
        elif self.get_event(event_id) is None:  # Create new event and save it
            new_event = {
                'id': event_id, 'guild_id': ctx.message.channel.guild.id,
                'member_id': ctx.message.author.id,
                'timestamp': str(ctx.message.created_at),
                'title': False, 'url': False, 'description': False,
                'thumbnail_url': '', 'image_url': '', 'start_date': False,
                'start_time': False, 'end_date': False, 'end_time': False,
                'zone': False, 'location': False, 'add_list': False}
            self.bot.db.table('Event').insert(new_event)
            await ctx.send(success_msgs['init'].format(event_id))
        else:  # event id already used
            await ctx.send(error_msgs['id_used'].format(event_id))

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
        """ check if event exist and delete it """
        if self.get_event(event_id) is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        else:  # delete event in db
            self.bot.db.table('Event').remove(Query().id == event_id)
            await ctx.send(success_msgs['delete'].format(event_id))

    # update commands
    def update_event(self, event_id, field, value, timestamp):
        """ check if event id exist, check if value is
        - date: for end date if start exist and if it's before  - format
        - time: if start date exist, for end time if start time exist and...
        ... if it's before if no end date - format
        update the specific field and the timestamp """
        Event = Query()
        event_updated = self.bot.db.table('Event').get(Event.id == event_id)
        if event_updated is None:
            # invalid event id
            return "No event founded with id {}".format(event_id)
        if '_date' in field:
            # date checks
            if ('end' in field) and (event_updated['start_date'] is False):
                # invalid end date -> set start date before
                return "Set value for start date before end date"
            try:
                # format
                e_date = datetime.strptime(value, '%Y/%m/%d')
                if ('end' in field) and (e_date <= datetime.strptime(
                        event_updated['start_date'], '%Y/%m/%d')):
                    # invalid end date -> set end date  > start date
                    return "End date must be set after start date > {}".format(
                        event_updated['start_date'])
            except ValueError:
                # invalid format
                return "date format not valid -> 2020/12/31"
        elif '_time' in field:
            # time checks
            if event_updated['start_date'] is False:
                if ('end' in field) and (event_updated['start_time'] is False):
                    # invalid end time -> set start date and time before
                    return "Set value for start date and time before end time"
                # invalid start time -> set start date before
                return "Set value for start date before start time"
            if ('end' in field) and (event_updated['start_time'] is False):
                # invalid end time -> set start time before
                return "Set value for start time before end time"
            try:
                # format
                e_time = datetime.strptime(value, '%H:%M%p')
                if ('end' in field) and (
                        event_updated['end_date'] is False) and (
                            e_time <= datetime.strptime(
                                event_updated['start_time'], '%H:%M%p')):
                    # invalid end time -> set end time > start time
                    return "End time must be set after start time > {}".format(
                        event_updated['start_time'])
            except ValueError:
                # invalid format
                return "time format not valid -> 8:00PM"
        # update field and timestamp
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
        """ check format and update url for a specific event """
        if checkers.is_url(url) is False:
            await ctx.send("url format not valid -> https://newurl.com")
        else:
            await ctx.send(self.update_event(
                event_id, 'url', url, ctx.message.created_at))

    @command(name=confs[6][0], help=confs[6][1], ignore_extra=False)
    async def e_start_date(self, ctx, event_id, e_date):
        """ check date format, update start_date for a specific event """
        if self.check_date_time(e_date, formats['date']) is True:
            pass
        # await ctx.send(self.update_event(
        #     event_id, 'start_date', e_date, ctx.message.created_at))

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
        """ check format and update thumbnail url for a specific event """
        if checkers.is_url(url) is False:
            await ctx.send("url format not valid -> https://newurl.com")
        else:
            await ctx.send(self.update_event(
                event_id, 'thumbnail_url', url, ctx.message.created_at))

    @command(name=confs[11][0], help=confs[11][1], ignore_extra=False)
    async def e_img(self, ctx, event_id, url):
        """ check format and update image url for a specific event """
        if checkers.is_url(url) is False:
            await ctx.send("url format not valid -> https://newurl.com")
        else:
            await ctx.send(self.update_event(
                event_id, 'image_url', url, ctx.message.created_at))

    @command(name=confs[12][0], help=confs[12][1], ignore_extra=False)
    async def e_zone(self, ctx, event_id, e_timezone):
        """ check format and update timezone for a specific event """
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
