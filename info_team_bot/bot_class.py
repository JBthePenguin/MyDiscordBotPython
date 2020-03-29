import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from commands import InfoCommand

load_dotenv()
GUILD = os.getenv('DISCORD_GUILD')


class InfoTeamBot(commands.Bot):
    """ Custom Bot, subclass discord.ext.commands.Bot """

    def __init__(self):
        """ init discord.ext.commands.Bot and add custom commands """
        super().__init__(command_prefix="!")
        # add commands
        # self.add_command(commands.Command(
        #     self.list_membres,
        #     name='list_membres',
        #     help='liste de tous les membres de la guilde.'))
        self.add_cog(InfoCommand(self))
        # self.add_command(commands.Command(
        #     self.list_roles,
        #     name='list_roles',
        #     help='liste les différents rôles de la guilde.'))
        self.add_command(commands.Command(
            self.list_membres_role,
            name='list_membres_role',
            help='liste les membres pour un rôle donné. Paramètre: nom du rôle'))
        self.add_command(commands.Command(
            self.list_salons,
            name='list_salons',
            help='liste les différents salons de la guilde par catégorie.'))
        self.add_command(commands.Command(
            self.list_membres_salon,
            name='list_membres_salon',
            help='liste les membres autorisés à aller sur un salon. Paramètre: nom du salon'))

    def run(self, token):
        super().run(token)

    def get_guild(self):
        """ return the guild with this name """
        return discord.utils.get(self.guilds, name=GUILD)

    # Events
    async def on_ready(self):
        """ print in console when bot is started and connected """
        print(f'{self.user} is connected to "{self.get_guild().name}"')

    async def on_command_error(self, ctx, error):
        """ send a message with the error """
        if isinstance(error, commands.errors.CommandNotFound):
            # command not found
            await ctx.send(
                "Cette commande n'existe pas. !help pour lister les commandes disponibles")

    # Commands
    # async def list_membres(self, ctx):
    #     """ send a message with the list of all members """
    #     members = '\n - '.join(
    #         [member.name for member in self.get_guild().members])
    #     message = f'Membres de la guilde {GUILD}:\n - {members}'
    #     await ctx.send(message)

    # async def list_roles(self, ctx):
    #     """ send a message with the list of roles """
    #     roles = '\n - '.join([role.name for role in self.get_guild().roles])
    #     message = f'Rôles de la guilde {GUILD}:\n - {roles}'
    #     await ctx.send(message)

    async def list_membres_role(self, ctx, role_name):
        """ send a message with the list of members for a specific role """
        guild = self.get_guild()
        role = discord.utils.get(guild.roles, name=role_name)
        if role is None:
            # no role with this name
            message = f'Pas de rôle {role_name}, soit tu le crées, soit tu me demandes un rôle qui existe'
        else:
            role_members = []
            for member in guild.members:
                if role in member.roles:
                    role_members.append(member)
            if role_members == []:
                message = f'Aucun membre avec le rôle {role.name}'
            else:
                members = '\n - '.join([member.name for member in role_members])
                message = f'{role.name}\n - {members}'
        await ctx.send(message)

    async def list_salons(self, ctx):
        """ send a message with the list of channels by category """
        categories = self.get_guild().by_category()
        messages = []
        for category in categories:
            channels = '\n - '.join([channel.name for channel in category[1]])
            messages.append(f'{category[0].name}:\n - {channels}')
        # channels = '\n - '.join([channel.name for channel in GUILD.channels])
        for message in messages:
            await ctx.send(message)

    async def list_membres_salon(self, ctx, channel_name):
        """ send a message with the list of members
        who have permission for a channel"""
        guild = self.get_guild()
        # get channel
        channel = discord.utils.get(guild.channels, name=channel_name)
        if channel is None:
            # no channel with this name
            message = f'Te fous pas de moi, pas de salon {channel_name}'
        else:
            # list authorized members
            auth_members = []
            for member in guild.members:
                permissions = channel.permissions_for(member)
                if permissions.view_channel:
                    auth_members.append(member)
            if auth_members == []:
                message = f'Aucun membre autorisé à utiliser le salon {channel.name}'
            else:
                members = '\n - '.join(
                    [member.name for member in auth_members])
                message = f'{channel.name}\n - {members}'
        await ctx.send(message)
