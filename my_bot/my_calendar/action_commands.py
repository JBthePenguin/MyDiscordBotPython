from datetime import datetime
from discord.ext.commands import Cog, command
from tinydb import Query
from validator_collection import checkers

confs = [
    ['init_event', 'Init an event-> #init_event id_without_space'],
    ['add_event', 'Add event to the list-> #add_event id'],
    ['del_event', 'Delete an event -> #del_event id'],
    ['e_title', 'Update title -> #e_title id "New Title"'],
    ['e_descr', 'Update description -> #e_descr id "New Description"'],
    ['e_url', 'Update url -> #e_url id "https://newurl.com"'],
    ['event_date', 'Modifie la date -> !event_date "Titre" "25/05/20 18:30"'],
    ['event_jeu', 'Modifie le jeu -> !event_jeu "Titre" "Nom du jeu"'],
    ['event_mj', 'Modifie le mj -> !event_mj "Titre" "@MJ1 @MJ2"'],
    ['event_groupe', 'Modifie le groupe -> !event_groupe "Titre" "@Groupe"'],
    [
        'event_joueurs',
        'Modifie les joueurs -> !event_joueurs "Titre" "@J1 @J2 ..."'],
    ['event_lieu', 'Modifie le lieu -> !event_lieu "Titre" "Nom du lieu"']]


class EventActionCommands(
        Cog, name='Commands "Init, Add, Update, Delete" Event'):

    def __init__(self, bot):
        self.bot = bot

    def check_date_format(self, date):
        """ return true if date format is validated, else False """
        try:
            datetime.strptime(date, '%d/%m/%y %H:%M')
        except ValueError:
            return False
        else:
            return True

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
                'time_zone': False, 'location': False, 'add_list': False}
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
    def update_event(self, event_id, field, value):
        """ update a specific field for an event """
        Event = Query()
        if self.bot.db.table('Event').get(Event.id == event_id) is None:
            return "No event founded with id {}".format(event_id)
        self.bot.db.table('Event').update({field: value}, Event.id == event_id)
        return "Ok, {} updated! to see -> #event {}".format(field, event_id)

    @command(name=confs[3][0], help=confs[3][1], ignore_extra=False)
    async def e_title(self, ctx, event_id, title):
        """ update title for a specific event """
        await ctx.send(self.update_event(event_id, 'title', title))

    @command(name=confs[4][0], help=confs[4][1], ignore_extra=False)
    async def e_descr(self, ctx, event_id, description):
        """ update description for a specific event """
        await ctx.send(self.update_event(event_id, 'description', description))

    @command(name=confs[5][0], help=confs[5][1], ignore_extra=False)
    async def e_url(self, ctx, event_id, url):
        """ update url for a specific event """
        if checkers.is_url(url) is False:
            await ctx.send("url format not valid -> https://newurl.com")
        else:
            await ctx.send(self.update_event(event_id, 'url', url))
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
