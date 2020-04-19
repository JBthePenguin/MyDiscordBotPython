# Configuration title : default and no object
class ConfTitle():
    """ Configuration for a guild's component title in embed and shell """

    def __init__(self, title, obj_type):
        """ Init with a default title and a no obj message """
        self.default = title
        self.no_obj = f"No {obj_type}"


class ConfGuildTitles():
    """ All titles used in shaping.py  """

    def __init__(self):
        """" Init with title for each component """
        # guild, owner, members, roles, channel's categories, channels
        self.gld = ConfTitle('Guild', 'guild')
        self.own = ConfTitle('Owner', 'owner')
        self.mem = ConfTitle('Members', 'member')
        self.rol = ConfTitle('Roles', 'role')
        self.cat = ConfTitle('Channel Categories', 'channel category')
        self.cha = ConfTitle('Channels', 'channel')
        # text, voice, news and store channels
        self.tcha = ConfTitle('Text Channels', 'text channel')
        self.vcha = ConfTitle('Voice Channels', 'voice channel')
        self.ncha = ConfTitle('News Channels', 'news channel')
        self.scha = ConfTitle('Store Channels', 'store channel')
        # emojis
        self.emo = ConfTitle('Emojis', 'emoji')


GUILD_TITLES = ConfGuildTitles()


# Configuration Command -> name, help message, conf_embed
class ConfCommand():
    """ Configuration for a guild command """

    def __init__(self, name, help, conf_embed):
        """ Init with name, help message and config embed (ConfTitle)"""
        self.name = name
        self.help = help
        self.conf_embed = conf_embed


class ConfGuildCommands():
    """ Configuration for all guild commands used in guild.py  """

    def __init__(self):
        """" Init with configuration for each command """
        # guild, owner, members, roles, channel's categories, channels
        self.gld = ConfCommand(
            'guild', "Guild's stats -> #guild", GUILD_TITLES.gld)
        self.own = ConfCommand(
            'owner', "The Owner-> #owner", GUILD_TITLES.own)
        self.mem = ConfCommand(
            'mems', "All members -> #mems", GUILD_TITLES.mem)
        self.rol = ConfCommand(
            'roles', "All roles -> #roles", GUILD_TITLES.rol)
        self.cat = ConfCommand(
            'cats', "All channel's categories -> #cats", GUILD_TITLES.cat)
        self.cha = ConfCommand(
            'chans', 'All channels -> #chans', GUILD_TITLES.cha)
        # text, voice, private, group, news and store channels
        self.tcha = ConfCommand(
            'tchans', 'All text channels -> #tchans', GUILD_TITLES.tcha)
        self.vcha = ConfCommand(
            'vchans', 'All voice channels -> #vchans', GUILD_TITLES.vcha)
        self.ncha = ConfCommand(
            'nchans', 'All news channels -> #nchans', GUILD_TITLES.ncha)
        self.scha = ConfCommand(
            'schans', 'All store channels -> #schans', GUILD_TITLES.scha)
        # emojis, shell
        self.emo = ConfCommand(
            'emos', 'All emojis -> #emos', GUILD_TITLES.emo)
        self.shl = ConfCommand(
            'shell', 'Infos in shell -> #shell', ConfTitle('', ''))


GUILD_COMMANDS = ConfGuildCommands()
# Configurations of commands -> {key: {'name': name, 'help': help text}}
# def conf_dict(title, obj_type):
#     """ return a dict with the name of a command and his help text,
#     for the response the embed's title and obj_type for empty list msg """
#     return {'title': title, 'obj_type': obj_type}

# confs_components = {
#     'rolmem': conf_dict(
#         'role_mems',
#         'Members with a role-> #role_mems "role name or id"'),
#     'catcha': conf_dict(
#         'cat_chans',
#         'Channels with a category-> #cat_chans "cat name or id"'),
#     'chamem': conf_dict(
#         'chan_mems',
#         'Auth Members on chan-> #chan_mems "chan name or id"')}
