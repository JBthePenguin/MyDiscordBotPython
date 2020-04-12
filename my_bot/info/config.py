class ConfigGuildEmbed():
    """ Configuration for a guild embed """

    def __init__(self, title, obj_type):
        """ Init with title and obj type """
        self.title = title
        self.obj_type = obj_type


class ConfGuildCommand():
    """ Configuration for guild commands """

    def __init__(self, name, help, embed_title, embed_obj_type):
        """ Init with name, help message and config embed"""
        self.name = name
        self.help = help
        self.conf_embed = ConfigGuildEmbed(embed_title, embed_obj_type)


# Configurations Command ->
#   -> name, help message,
#   -> embed onfiguration, title and obj type

# shell
conf_shl = ConfGuildCommand(
    'shell', 'Display infos in shell -> #shell',
    '', '')
# owner
conf_own = ConfGuildCommand(
    'owner', "The Owner-> #owner",
    'Owner', 'owner')
# members
conf_mem = ConfGuildCommand(
    'mems', "All members -> #mems",
    'Members', 'member')
# roles
conf_rol = ConfGuildCommand(
    'roles', "All roles -> #roles",
    'Roles', 'role')
# channel's categories
conf_cat = ConfGuildCommand(
    'cats', "All channel's categories -> #cats",
    'Channel Categories', 'channel category')
# channels
conf_cha = ConfGuildCommand(
    'chans', 'All channels -> #chans',
    'Channels', 'channel')
# text channels
conf_tcha = ConfGuildCommand(
    'tchans', 'All text channels -> #tchans',
    'Text Channels', 'text channel')
# voice channels
conf_vcha = ConfGuildCommand(
    'vchans', 'All voice channels -> #vchans',
    'Voice Channels', 'voice channel')
# private channels
conf_pcha = ConfGuildCommand(
    'pchans', 'All private channels -> #pchans',
    'Private Channels', 'private channel')
# group channels
conf_gcha = ConfGuildCommand(
    'gchans', 'All group channels -> #gchans',
    'Group Channels', 'group channel')
# news channels
conf_ncha = ConfGuildCommand(
    'nchans', 'All news channels -> #nchans',
    'News Channels', 'news channel')
# store channels
conf_scha = ConfGuildCommand(
    'schans', 'All store channels -> #schans',
    'Store Channels', 'store channel')
# emojis
conf_emo = ConfGuildCommand(
    'emos', 'All emojis -> #emos',
    'Emojis', 'emoji')




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
