from discord import Embed, ChannelType
from .settings import confs_guild as confs
from .checkers import empty_content


def print_list(title, name, objs, confs_key):
    """ Print a list in shell with a title """
    objs_checked = empty_content(objs, name, confs[confs_key]['obj_type'])
    if isinstance(objs_checked, str):
        print('\n' + objs_checked)
    else:
        print(title)
        objs_checked.sort(key=lambda obj: obj.name)
        for obj in objs_checked:
            print("id: {} - {}".format(obj.id, obj.name))


def info_in_shell(guild):
    """ Display infos (id, name) in shell for a specific guild
    - members -roles - channels by category and type"""
    print("\n############## GUILD #######\nid: {} - {}".format(
        guild.id, guild.name))
    print("### Owner ###\nid: {} - {}".format(
        guild.owner.id, guild.owner.name))
    print_list('\n########## MEMBERS #####', guild.name, guild.members, 'mem')
    print_list('\n########## ROLES #####', guild.name, guild.roles, 'rol')
    print('\n########## CHANNELS BY CATEGORY #####')
    if not guild.by_category():
        print('\n{}: no category, no channel'.format(guild.name))
    else:
        for chans_cat in guild.by_category():
            print('\n###### CATEGORY ###')
            if chans_cat[0] is None:
                print("No category")
            else:
                print("id: {} - {}".format(chans_cat[0].id, chans_cat[0].name))
            print('#### CHANNELS ##')
            if not chans_cat[1]:
                print('No Channel')
            else:
                t_ch, v_ch, p_ch, g_ch, n_ch, s_ch = [], [], [], [], [], []
            for channel in chans_cat[1]:
                if channel.type == ChannelType.text:
                    t_ch.append(channel)
                elif channel.type == ChannelType.voice:
                    v_ch.append(channel)
                elif channel.type == ChannelType.private:
                    p_ch.append(channel)
                elif channel.type == ChannelType.group:
                    g_ch.append(channel)
                elif channel.type == ChannelType.news:
                    n_ch.append(channel)
                elif channel.type == ChannelType.store:
                    s_ch.append(channel)
            print_list('## TEXT CHANNELS ', chans_cat[0].name, t_ch, 'tcha')
            print_list('## VOICE CHANNELS ', chans_cat[0].name, v_ch, 'vcha')
            print_list('## PRIVATE CHANNELS ', chans_cat[0].name, p_ch, 'pcha')
            print_list('## GROUP CHANNELS ', chans_cat[0].name, g_ch, 'gcha')
            print_list('## NEWS CHANNELS ', chans_cat[0].name, n_ch, 'ncha')
            print_list('## STORE CHANNELS ', chans_cat[0].name, s_ch, 'scha')


def list_in_embed(objs, author_name, icon_url, title):
    """ Return an embed with a specific list sorted"""
    objs.sort(key=lambda obj: obj.name)
    ids = "\n".join(str(obj.id) for obj in objs)
    names = "\n".join(obj.name for obj in objs)
    embed = Embed(title=title, color=0x161616)
    embed.set_author(name=author_name, icon_url=icon_url)
    embed.add_field(name='ID', value=ids, inline=True)
    embed.add_field(name='Name', value=names, inline=True)
    return embed


def emojis_in_embed(emojis, author_name, icon_url, title):
    """ Return an embed with a tuple of emojis """
    embed = Embed(title=title, color=0x161616)
    symbols = "\n\n".join(str(emoji) for emoji in emojis)
    names = "\n\n".join(emoji.name for emoji in emojis)
    embed.set_author(name=author_name, icon_url=icon_url)
    embed.add_field(name='\u200b', value=symbols, inline=True)
    embed.add_field(name='\u200b', value=names, inline=True)
    return embed
