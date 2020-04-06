from datetime import datetime
from discord.ext.commands import Cog, command
from tinydb import Query

confs = [
    ['init_event', 'Init an event-> #init_event id_without_space'],
    ['add_event', 'Add event to the list-> #add_event id'],
    ['del_event', 'Delete an event -> !del_event id'],
    ['event_titre', 'Modifie le titre -> !event_titre "Titre" "New Titre"'],
    ['event_date', 'Modifie la date -> !event_date "Titre" "25/05/20 18:30"'],
    ['event_jeu', 'Modifie le jeu -> !event_jeu "Titre" "Nom du jeu"'],
    ['event_mj', 'Modifie le mj -> !event_mj "Titre" "@MJ1 @MJ2"'],
    ['event_groupe', 'Modifie le groupe -> !event_groupe "Titre" "@Groupe"'],
    [
        'event_joueurs',
        'Modifie les joueurs -> !event_joueurs "Titre" "@J1 @J2 ..."'],
    ['event_lieu', 'Modifie le lieu -> !event_lieu "Titre" "Nom du lieu"']]


class EventActionCommands(Cog, name='Commandes "Ajout, Modif, Suppr" Event'):

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

    # def update_event(self, name, field, value):
    #     """ update a specific field for an event
    #     and for name field check if already used """
    #     change_name = False
    #     if field == 'name':
    #         if self.bot.db.table('Event').search(Query().name == value):
    #             return "{} existe déjà.".format(value)  # name already used
    #         change_name = True
    #     if self.bot.db.table('Event').search(Query().name == name) == []:
    #         return "Pas d'évènement au nom de '{}'".format(name)
    #     else:
    #         self.bot.db.table('Event').update(
    #             {field: value}, Query().name == name)
    #         if change_name is True:
    #             return "Ok! pour voir-> !voir_event \"{}\"".format(value)
    #         return "Ok! pour voir-> !voir_event \"{}\"".format(name)

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
                'author_id': ctx.message.author.id,
                'timestamp': str(ctx.message.created_at),
                'title': False, 'url': False, 'description': False,
                'thumbnail_url': 'https://placehold.it/150x150', 'image_url': 'https://placehold.it/150x150', 'start_date': False,
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
        """ delete an evenment """
        if self.bot.db.table('Event').get(Query().id == event_id) is None:
            await ctx.send("No event founded with id {}".format(event_id))
        else:
            self.bot.db.table('Event').remove(Query().id == event_id)
            await ctx.send("{} deleted".format(event_id))

    # update commands
    # @command(name=confs[2][0], help=confs[2][1], ignore_extra=False)
    # async def event_name(self, ctx, name, new_name):
    #     """ update name - title for a specific event """
    #     await ctx.send(self.update_event(name, 'name', new_name))
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
