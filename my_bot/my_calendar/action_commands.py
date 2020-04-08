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
    ['e_url', 'Update url -> #e_url id https://somewhere.com'],
    ['e_start_date', 'Update start date -> #e_start_date id 2020/12/31'],
    ['e_start_time', 'Update start time -> #e_start_time id 8:00PM'],
    ['e_end_date', 'Update end date -> #e_end_date id 2020/12/31'],
    ['e_end_time', 'Update end time -> #e_end_time id 8:00PM'],
    ['e_thum', 'Update thumbnail url -> #e_thum id https://url.com/thumb.png'],
    ['e_img', 'Update image url -> #e_img id https://url.com/img.png'],
    ['e_zone', 'Update timezone -> #e_zone id Europe/Paris'],
    ['e_loc', 'Update location -> #e_loc id "The place to be"']]
# Formats -> {'name': 'format'}
formats = {'date': '%Y/%m/%d', 'time': '%H:%M%p'}
# Success messages -> {name: message, ...}
success_msgs = {
    'init': "Init Ok! to see -> #event {}",  # {} -> event_id
    'delete': "Ok! {} is now deleted",  # {} -> event_id
    'update_field': "Ok, {} updated! to see -> #event {}",  # {} -> field, id
    'date_format': "date format not valid -> 2020/12/31", }
# Error messages -> {name: message, ...}
error_msgs = {
    'no_space_id': "No space for event id",
    'id_used': "{} is already used, choose another id",  # {} -> event_id
    'no_event': "No event founded with id {}",  # {} -> event_id
    'url_format': "url format not valid -> https://somewhere.com",
    'date_format': "date format not valid -> 2020/12/31",
    'time_format': "time format not valid -> 10:30PM",
    'zone': "".join([
        "timezone not valid, to see a list -> ",
        "https://github.com/JBthePenguin/MyDiscordBotPython/blob/",
        "master/my_bot/my_calendar/pytz_timezones_list.txt"]),
    't_before': "Invalid timing -> start before {}",  # {}-> end value
    't_after': "Invalid timing -> end after {}",  # {}-> start value
    'no_start': "No start {} -> Set value for start_{}", }  # {}-> date or time


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

    def check_timing(self, start_value, end_value, check_format):
        """ check timing between start and end date or time:
        return True or False """
        if datetime.strptime(start_value, check_format) > datetime.strptime(
                end_value, check_format):
            return False
        return True

    # init add delete commands
    @command(name=confs[0][0], help=confs[0][1], ignore_extra=False)
    async def init_event(self, ctx, event_id):
        """ check if there is space in event id and
        save new event if event id is not already used """
        if " " in event_id:  # space not acepted
            await ctx.send(error_msgs['no_space_id'])
        elif self.get_event(event_id) is None:  # Create new event and save it
            new_event = {
                'id': event_id, 'guild_id': ctx.message.channel.guild.id,
                'member_id': ctx.message.author.id,
                'timestamp': str(ctx.message.created_at),
                'title': None, 'url': None, 'description': None,
                'thumbnail_url': '', 'image_url': '', 'start_date': None,
                'start_time': None, 'end_date': None, 'end_time': None,
                'zone': None, 'location': None, 'add_list': False}
            self.bot.db.table('Event').insert(new_event)
            await ctx.send(success_msgs['init'].format(event_id))
        else:  # id already used
            await ctx.send(error_msgs['id_used'].format(event_id))

    @command(name=confs[1][0], help=confs[1][1], ignore_extra=False)
    async def add_event(self, ctx, event_id):
        """ add event to the list """
        if self.get_event(event_id) is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))

    @command(name=confs[2][0], help=confs[2][1], ignore_extra=False)
    async def del_event(self, ctx, event_id):
        """ check if event exist and delete it """
        if self.get_event(event_id) is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        else:  # delete event
            self.bot.db.table('Event').remove(Query().id == event_id)
            await ctx.send(success_msgs['delete'].format(event_id))

    # update commands
    def update_event(self, id, field, value, timestamp):
        """ update specific field and timestamp on specific event:
        return success message """
        self.bot.db.table('Event').update(
            {field: value, 'timestamp': str(timestamp)}, Query().id == id)
        return success_msgs['update_field'].format(field, id)

    @command(name=confs[3][0], help=confs[3][1], ignore_extra=False)
    async def e_title(self, ctx, event_id, title):
        """ check if event exist and update title field """
        if self.get_event(event_id) is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        else:  # update title field
            await ctx.send(self.update_event(
                event_id, 'title', title, ctx.message.created_at))

    @command(name=confs[4][0], help=confs[4][1], ignore_extra=False)
    async def e_descr(self, ctx, event_id, description):
        """ check if event exist and update description field """
        if self.get_event(event_id) is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        else:  # update description field
            await ctx.send(self.update_event(
                event_id, 'description', description, ctx.message.created_at))

    @command(name=confs[5][0], help=confs[5][1], ignore_extra=False)
    async def e_url(self, ctx, event_id, url):
        """ check if event exist, valid format, update url field """
        if self.get_event(event_id) is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        elif checkers.is_url(url) is False:  # format url invalid
            await ctx.send(error_msgs["url_format"])
        else:  # update url field
            await ctx.send(self.update_event(
                event_id, 'url', url, ctx.message.created_at))

    @command(name=confs[6][0], help=confs[6][1], ignore_extra=False)
    async def e_start_date(self, ctx, event_id, start_date):
        """ check if event exist, valid format and timing,
        update start_date field """
        event = self.get_event(event_id)
        if event is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        elif self.check_date_time(
                start_date, formats['date']) is False:  # format date invalid
            await ctx.send(error_msgs['date_format'])
        elif (event['end_date'] is not None) and (
                self.check_timing(
                    start_date, event['end_date'],
                    formats['date']) is False):  # timing invalid
            await ctx.send(error_msgs['t_before'].format(event['end_date']))
        else:  # update start_date field
            await ctx.send(self.update_event(
                event_id, 'start_date', start_date, ctx.message.created_at))

    @command(name=confs[7][0], help=confs[7][1], ignore_extra=False)
    async def e_start_time(self, ctx, event_id, start_time):
        """ check if event and start date exist, valid format and timing,
        update start_time field """
        event = self.get_event(event_id)
        if event is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        elif event['start_date'] is None:  # no start date
            await ctx.send(error_msgs['no_start'].format('date'))
        elif self.check_date_time(
                start_time, formats['time']) is False:  # format time invalid
            await ctx.send(error_msgs['time_format'])
        elif (event['end_date'] is None) and (
                event['end_time'] is not None) and (self.check_timing(
                    start_time, event['end_time'],
                    formats['time']) is False):  # timing invalid
            await ctx.send(error_msgs['t_before'].format(event['end_time']))
        else:  # update start_time field
            await ctx.send(self.update_event(
                event_id, 'start_time', start_time, ctx.message.created_at))

    @command(name=confs[8][0], help=confs[8][1], ignore_extra=False)
    async def e_end_date(self, ctx, event_id, end_date):
        """ check if event and start date exist, valid format and timing,
        update end_date field """
        event = self.get_event(event_id)
        if event is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        elif event['start_date'] is None:  # no start date
            await ctx.send(error_msgs['no_start'].format('date'))
        elif self.check_date_time(
                end_date, formats['date']) is False:  # format date invalid
            await ctx.send(error_msgs['date_format'])
        elif self.check_timing(event['start_date'], end_date, formats[
                'date']) is False:  # timing invalid
            await ctx.send(error_msgs['t_after'].format(event['start_date']))
        else:  # update end_date field
            await ctx.send(self.update_event(
                event_id, 'end_date', end_date, ctx.message.created_at))

    @command(name=confs[9][0], help=confs[9][1], ignore_extra=False)
    async def e_end_time(self, ctx, event_id, end_time):
        """ check if event and start date and time exist,
        valid format and timing if no end date, update end_time field """
        event = self.get_event(event_id)
        if event is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        elif event['start_time'] is None:  # no start time
            await ctx.send(error_msgs['no_start'].format('time'))
            if event['start_date'] is None:  # no start date
                await ctx.send(error_msgs['no_start'].format('date'))
        elif self.check_date_time(
                end_time, formats['time']) is False:  # format time invalid
            await ctx.send(error_msgs['time_format'])
        elif (event['end_date'] is None) and (self.check_timing(
                event['start_time'],
                end_time, formats['time']) is False):  # timing invalid
            await ctx.send(error_msgs['t_after'].format(event['start_time']))
        else:  # update end_time field
            await ctx.send(self.update_event(
                event_id, 'end_time', end_time, ctx.message.created_at))

    @command(name=confs[10][0], help=confs[10][1], ignore_extra=False)
    async def e_thumb(self, ctx, event_id, url):
        """ check if event exist, valid format, update thumbnail url field """
        if self.get_event(event_id) is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        elif checkers.is_url(url) is False:  # format url invalid
            await ctx.send(error_msgs["url_format"])
        else:  # update thumbnail_url field
            await ctx.send(self.update_event(
                event_id, 'thumbnail_url', url, ctx.message.created_at))

    @command(name=confs[11][0], help=confs[11][1], ignore_extra=False)
    async def e_img(self, ctx, event_id, url):
        """ check if event exist, valid format, update image url field """
        if self.get_event(event_id) is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        elif checkers.is_url(url) is False:  # format url invalid
            await ctx.send(error_msgs["url_format"])
        else:  # update image_url field
            await ctx.send(self.update_event(
                event_id, 'image_url', url, ctx.message.created_at))

    @command(name=confs[12][0], help=confs[12][1], ignore_extra=False)
    async def e_zone(self, ctx, event_id, e_timezone):
        """ check if event exist, format and update timezone field """
        if self.get_event(event_id) is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        else:
            try:
                timezone(e_timezone)
            except UnknownTimeZoneError:  # invalid timezone format
                await ctx.send(error_msgs['zone'])
            else:
                await ctx.send(self.update_event(
                    event_id, 'zone', e_timezone, ctx.message.created_at))

    @command(name=confs[13][0], help=confs[13][1], ignore_extra=False)
    async def e_location(self, ctx, event_id, location):
        """ check if event exist and update location field """
        if self.get_event(event_id) is None:  # no event with this id
            await ctx.send(error_msgs['no_event'].format(event_id))
        else:  # update location field
            await ctx.send(self.update_event(
                event_id, 'location', location, ctx.message.created_at))
