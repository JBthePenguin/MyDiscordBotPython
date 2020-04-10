# Configurations of commands -> {key: {'name': name, 'help': help text}}
def conf_dict(name, help, title, obj_type):
    """ return a dict with the name of a command and his help text,
    for the response the embed's title and obj_type for empty list msg """
    return {'name': name, 'help': help, 'title': title, 'obj_type': obj_type}


confs = {
    'shl': conf_dict('shell', 'Display infos in shell -> #shell', '', ''),
    'mem': conf_dict(
        'mems', "All members -> #mems",
        'Members', 'member'),
    'rol': conf_dict(
        'roles', "All roles -> #roles",
        'Roles', 'role'),
    'cat': conf_dict(
        'cats', "All channel's categories -> #cats",
        'Channel Categories', 'channel category'),
    'cha': conf_dict(
        'chans', 'All channels -> #chans',
        'Channels', 'channel'),
    'tcha': conf_dict(
        'tchans', 'All text channels -> #tchans',
        'Text Channels', 'text channel'),
    'vcha': conf_dict(
        'vchans', 'All voice channels -> #vchans',
        'Voice Channels', 'voice channel'), }
    # 'rolmem': conf_dict(
    #     'role_mems',
    #     'Members with a role-> #role_mems "role name or id"'),
    # 'catcha': conf_dict(
    #     'cat_chans',
    #     'Channels with a category-> #cat_chans "cat name or id"'),
    # 'chamem': conf_dict(
    #     'chan_mems',
    #     'Auth Members on chan-> #chan_mems "chan name or id"')}

# Error messages -> {name: message, ...}
error_msgs = {
    'no_exist': "{}: {} not exist",  # {} -> obj field, value
    'empty_list': "{}: No {}", }  # {} -> location, obj type
