class ConfCommand():
    """Configuration for a command."""

    def __init__(self, name, help_text):
        """Init with name, help message."""
        self.name = name
        self.help = help_text


class ConfGuildCommands():
    """Configuration for all guild commands used in guild.py ."""

    def __init__(self):
        """Init with configuration for each command."""
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


class ConfComponentsCommands():
    """Configuration for all components commands used in components.py ."""

    def __init__(self):
        """"Init with configuration for each command."""
        # member
        self.mem = ConfCommand('mem', "Infos of a member -> #mem id_or_name")


COMPONENTS_COMMANDS = ConfComponentsCommands()
