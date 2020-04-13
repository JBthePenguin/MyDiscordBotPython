# Configuration title : default and no object
class ConfGuildTitle():
    """ Configuration for guild's component title """

    def __init__(self, title, obj_type):
        """ Init with title and obj type """
        self.default = title
        self.no_obj = f"No {obj_type}"


# shell, owner, members, roles, channel's categories, channels
title_gld = ConfGuildTitle('Guild', 'guild')
title_own = ConfGuildTitle('Owner', 'owner')
title_mem = ConfGuildTitle('Members', 'member')
title_rol = ConfGuildTitle('Roles', 'role')
title_cat = ConfGuildTitle('Channel Categories', 'channel category')
title_cha = ConfGuildTitle('Channels', 'channel')
# text, voice, private, group, news and store channels
title_tcha = ConfGuildTitle('Text Channels', 'text channel')
title_vcha = ConfGuildTitle('Voice Channels', 'voice channel')
title_pcha = ConfGuildTitle('Private Channels', 'private channel')
title_gcha = ConfGuildTitle('Group Channels', 'group channel')
title_ncha = ConfGuildTitle('News Channels', 'news channel')
title_scha = ConfGuildTitle('Store Channels', 'store channel')
# emojis
title_emo = ConfGuildTitle('Emojis', 'emoji')


# Configurations Command -> name, help message, conf_embed
class ConfGuildCommand():
    """ Configuration for guild commands """

    def __init__(self, name, help, conf_embed):
        """ Init with name, help message and config embed"""
        self.name = name
        self.help = help
        self.conf_embed = conf_embed


# owner, members, roles, channel's categories, channels
com_gld = ConfGuildCommand(
    'guild', "Guild's stats -> #guild", ConfGuildTitle('', ''))
com_own = ConfGuildCommand('owner', "The Owner-> #owner", title_own)
com_mem = ConfGuildCommand('mems', "All members -> #mems", title_mem)
com_rol = ConfGuildCommand('roles', "All roles -> #roles", title_rol)
com_cat = ConfGuildCommand(
    'cats', "All channel's categories -> #cats", title_cat)
com_cha = ConfGuildCommand('chans', 'All channels -> #chans', title_cha)
# text, voice, private, group, news and store channels
com_tcha = ConfGuildCommand(
    'tchans', 'All text channels -> #tchans', title_tcha)
com_vcha = ConfGuildCommand(
    'vchans', 'All voice channels -> #vchans', title_vcha)
com_pcha = ConfGuildCommand(
    'pchans', 'All private channels -> #pchans', title_pcha)
com_gcha = ConfGuildCommand(
    'gchans', 'All group channels -> #gchans', title_gcha)
com_ncha = ConfGuildCommand(
    'nchans', 'All news channels -> #nchans', title_ncha)
com_scha = ConfGuildCommand(
    'schans', 'All store channels -> #schans', title_scha)
# emojis, shell
com_emo = ConfGuildCommand('emos', 'All emojis -> #emos', title_emo)
com_shl = ConfGuildCommand(
    'shell', 'Infos in shell -> #shell', ConfGuildTitle('', ''))



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
