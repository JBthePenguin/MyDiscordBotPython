from discord import ChannelType
from .s_titles import TITLES
from .s_guild_embed import get_list


def get_objs_str(objs):
    """Return a string with a list of objs"""
    objs.sort(key=lambda obj: obj.name)
    objs_str = ""
    for obj in objs:
        objs_str += f"- {obj.id} - {obj.name}\n"
    return objs_str


def get_emos_str(emojis):
    """Return a string with list of emojis(tup) symbol and name, 3 by line"""
    n_emos = len(emojis)
    emos_str = ""
    for i, emoji in enumerate(emojis):
        emos_str += f"- {str(emoji)} {emoji.name}"
        if ((i + 1) % 3 == 0) or ((i + 1) == n_emos):
            emos_str += "\n"
        else:
            emos_str += " "
    return emos_str


def get_c_type(com_key):
    """Return the corresponding channel type for a specific command key"""
    if com_key == 'tcha':
        return ChannelType.text
    elif com_key == 'vcha':
        return ChannelType.voice
    elif com_key == 'ncha':
        return ChannelType.news
    elif com_key == 'scha':
        return ChannelType.store


def get_chans_cats_str(chans_cats):
    """Return the string for channels sorted by category and type"""
    chanscats_str = ""
    for chans_cat in chans_cats:
        # category title
        sep = '#####'
        if chans_cat[0] is None:
            cat_title = f"No {TITLES['cat'][1]}"
        else:
            cat_title = chans_cat[0].name
        chanscats_str += f"\n{sep} {cat_title} {sep}\n"
        if chans_cat[1]:
            # channels list by type
            for c_key in ['tcha', 'vcha', 'ncha', 'scha']:
                chans = [c for c in chans_cat[1] if (
                    c.type == get_c_type(c_key))]
                if chans:
                    sep = "###"
                    chanscats_str += f"{sep} {len(chans)} {TITLES[c_key][0]}\n"
                    chans.sort(key=lambda chan: chan.name)
                    for chan in chans:
                        chanscats_str += f"- {chan.id} - {chan.name}\n"
        else:
            chanscats_str += f"- No {TITLES['cha'][1]}\n"
    return chanscats_str


class GuildShell():
    """String for a Guild."""

    def __init__(self, guild):
        """Init a string for with all infos for a specific guild."""
        self.guild = guild

    def __str__(self):
        sep = '##########'
        g_str = "\n"
        # Guild and Owner
        for title_obj in [
                (TITLES['gld'][0], self.guild),
                (TITLES['own'][0], self.guild.owner)]:
            g_str += f"\n{sep} {title_obj[0]} {sep}"
            g_str += f"\n- {title_obj[1].id} - {title_obj[1].name}\n"
        # Components: members, roles, ....
        for l_key in [
                'mem', 'rol', 'emo', 'cat', 'cha',
                'tcha', 'vcha', 'ncha', 'scha']:
            objs = get_list(self.guild, l_key)
            if objs:
                g_str += f"\n{sep} {len(objs)} {TITLES[l_key][0]} {sep}\n"
                if l_key == 'emo':
                    g_str += get_emos_str(objs)
                else:
                    g_str += get_objs_str(objs)
            else:
                g_str += f"\n{sep} No {TITLES[l_key][1]} {sep}\n"
        # Channels by Categories
        chans_cats = self.guild.by_category()
        if chans_cats:
            g_str += f"\n\n{sep} CHANNELS BY CATEGORIES {sep}\n"
            g_str += get_chans_cats_str(chans_cats)
        return g_str
