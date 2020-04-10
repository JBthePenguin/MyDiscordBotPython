from discord import Embed, ChannelType


def print_list(title, objs):
    """ Print a list in shell with a title """
    print(title)
    objs.sort(key=lambda obj: obj.name)
    for obj in objs:
        print("id: {} - {}".format(obj.id, obj.name))


def info_in_shell(guild):
    """ Display infos (id, name) in shell for a specific guild
    - members -roles - channels by category and type"""
    print_list('####### GUILD #######', [guild])
    print_list('\n##### MEMBERS #####', guild.members)
    print_list('\n##### ROLES #####', guild.roles)
    print('\n##### CHANNELS BY CATEGORY #####')
    for chans_cat in guild.by_category():
        print('\n### CATEGORY ###')
        if chans_cat[0] is None:
            print("No category")
        else:
            print("id: {} - {}".format(chans_cat[0].id, chans_cat[0].name))
        t_channels, v_channels, o_channels = [], [], []
        for channel in chans_cat[1]:
            if channel.type == ChannelType.text:
                t_channels.append(channel)
            elif channel.type == ChannelType.voice:
                v_channels.append(channel)
            else:
                o_channels.append(channel)
        if t_channels != []:
            print_list('# TEXT CHANNELS #', t_channels)
        if v_channels != []:
            print_list('# VOICE CHANNELS #', v_channels)
        if o_channels != []:
            print_list('# OTHER CHANNELS #', o_channels)


def list_in_embed(objs, author_name, icon_url, title="Members"):
    """ Return an embed with a specific list sorted"""
    objs.sort(key=lambda obj: obj.name)
    objs_ids = "\n".join(str(obj.id) for obj in objs)
    objs_names = "\n".join(obj.name for obj in objs)
    embed = Embed(title=title, color=0x161616)
    embed.set_author(name=author_name, icon_url=icon_url)
    embed.add_field(name='ID', value=objs_ids, inline=True)
    embed.add_field(name='Name', value=objs_names, inline=True)
    return embed
