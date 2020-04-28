# Configuration title : default and no object
class ConfTitle():
    """ Configuration for a guild's component title in embed and shell """

    def __init__(self, title, obj_type):
        """ Init with a default title and a no obj message """
        self.default = title
        self.no_obj = f"No {obj_type}"


# Configuration Command -> name, help message
class ConfCommand():
    """ Configuration for a command """

    def __init__(self, name, help):
        """ Init with name, help message """
        self.name = name
        self.help = help


#
# GUILD TITLES AND COMMANDS
#
class ConfGuildTitles():
    """ All titles used in shaping.py for guild commands """

    def __init__(self):
        """" Init with title for each component (singular and plural)"""
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


class ConfGuildCommands():
    """ Configuration for all guild commands used in guild.py  """

    def __init__(self):
        """" Init with configuration for each command """
        # guild, owner, members, roles, channel's categories, channels
        self.gld = ConfCommand('guild', "Guild's stats -> #guild")
        self.own = ConfCommand('owner', "The Owner-> #owner")
        self.mem = ConfCommand('mems', "All members -> #mems")
        self.rol = ConfCommand('roles', "All roles -> #roles")
        self.cat = ConfCommand('cats', "All channel's categories -> #cats")
        self.cha = ConfCommand('chans', 'All channels -> #chans')
        # text, voice, private, group, news and store channels
        self.tcha = ConfCommand('tchans', 'All text channels -> #tchans')
        self.vcha = ConfCommand('vchans', 'All voice channels -> #vchans')
        self.ncha = ConfCommand('nchans', 'All news channels -> #nchans')
        self.scha = ConfCommand('schans', 'All store channels -> #schans')
        # emojis, shell
        self.emo = ConfCommand('emos', 'All emojis -> #emos')
        self.shl = ConfCommand('shell', 'Infos in shell -> #shell')


GUILD_COMMANDS = ConfGuildCommands()


#
# COMPONENTS TITLES AND COMMANDS
#
class ConfComponentsTitles():
    """ All titles used in shaping.py for components commands """

    def __init__(self):
        """" Init with title for each component (singular and plural)"""
        # members
        self.mem = ConfTitle('Member', 'member')


COMPONENTS_TITLES = ConfComponentsTitles()


class ConfComponentsCommands():
    """ Configuration for all components commands used in components.py  """

    def __init__(self):
        """" Init with configuration for each command """
        # member
        self.mem = ConfCommand('mem', "Infos of a member -> #mem id_or_name")


COMPONENTS_COMMANDS = ConfComponentsCommands()
