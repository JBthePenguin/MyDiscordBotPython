from .s_titles import TYPE_TITLES, get_s_tup_titles_list, TITLES
from .s_guild_embed import get_list


def add_emojis(shl_str, emojis):
    """Add a tuple of emojis (3 by line)."""
    # for i in range(len(emojis)):
    for i, emoji in enumerate(emojis):
        shl_str += f"- {str(emoji)} {emoji.name} "
        if (i + 1) % 3 == 0:
            shl_str += "\n"
    if len(emojis) % 3 != 0:
        shl_str += "\n"


def add_list(shl_str, guild, l_key):
    """Add a list with a title to infos string."""
    objs = get_list(guild, l_key)
    if objs:
        n_objs = str(len(objs))
        shl_str += f"\n########## {n_objs} {TITLES[l_key][0]} ##########\n"
        if l_key == 'emo':
            add_emojis(shl_str, objs)
        else:
            objs.sort(key=lambda obj: obj.name)
            for obj in objs:
                shl_str += f"- {obj.id} - {obj.name}\n"
    else:
        shl_str += f"\n########## No {TITLES[l_key][1]} ##########\n"


def add_type_chans(shl_str, chans, c_title):
    """Add channels with a specific type(title)."""
    if chans:
        shl_str += f"### {str(len(chans))} {c_title}\n"
        chans.sort(key=lambda chan: chan.name)
        for chan in chans:
            shl_str += f"- {chan.id} - {chan.name}\n"


def add_cats_chans(shl_str, chans_cats):
    """Add channels by category and type."""
    if chans_cats:
        shl_str += "\n\n########## CHANNELS BY CATEGORIES ##########\n"
        for chans_cat in chans_cats:
            if chans_cat[0] is None:
                shl_str += "\n##### No channel category #####\n"
            else:
                shl_str += f"\n##### {chans_cat[0].name} #####\n"
            if chans_cat[1]:
                for t_tls in TYPE_TITLES:
                    add_type_chans(
                        shl_str,
                        [c for c in chans_cat[1] if (c.type == t_tls[0])],
                        t_tls[1][0])
            else:
                shl_str += f"- No channel\n"


class GuildShell(str):
    """String for a Guild."""

    def __init__(self, guild):
        """Init a string for with all infos for a specific guild."""
        super().__init__()
        # guild_shell.add_infos()
        # Guild and Owner
        self += '\n##########  Guild ##########'
        self += f"\n- {guild.id} - {guild.name}\n"
        self += '\n##########  Owner ##########'
        self += f"\n- {guild.owner.id} - {guild.owner.name}\n"
        # members, roles, ....
        for l_key in [
                'mem', 'rol', 'emo', 'cat', 'cha',
                'tcha', 'vcha', 'ncha', 'scha']:
            add_list(self, guild, l_key)
        # Channels by Categories
        add_cats_chans(self, guild.by_category())







    # def add_infos(self):
    #     """Construct a string with all guild's infos."""
    #     for corres_tup in get_s_tup_titles_list(self.guild):
    #         self.add_list(corres_tup[0], corres_tup[1])
    #     # Channels by Category
    #     self.add_cats_chans(self.guild.by_category())
