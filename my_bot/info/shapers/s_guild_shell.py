from .s_titles import TITLES
from .s_utils import get_list, get_c_type


class GuildShell():
    """Guild Infos to display in shell"""

    def __init__(self, guild):
        """Init a string for with all infos for a specific guild."""
        self.guild = guild
        self.sep = '##########'

    def __str__(self):
        """Return a string with all guild's infos."""
        g_str = "\n"
        g_str += self.get_gld_own_str()
        g_str += self.get_objs_str()
        g_str += self.get_chans_cats_str()
        return g_str

    def get_gld_own_str(self):
        """Return a string with guild and owner infos."""
        gld_own_str = ""
        for title_obj in [
                (TITLES['gld'][0], self.guild),
                (TITLES['own'][0], self.guild.owner)]:
            gld_own_str += f"\n{self.sep} {title_obj[0]} {self.sep}"
            gld_own_str += f"\n- {title_obj[1].id} - {title_obj[1].name}\n"
        return gld_own_str

    def get_objs_str(self):
        """Return a string for a list of objs, or for a tuples -> emojis."""
        objs_str = ""
        for l_key in [
                'mem', 'rol', 'emo', 'cat', 'cha',
                'tcha', 'vcha', 'ncha', 'scha']:
            objs = get_list(self.guild, l_key)
            if objs:
                objs_str += f"\n{self.sep} {len(objs)} "
                objs_str += f"{TITLES[l_key][0]} {self.sep}\n"
                if l_key == 'emo':  # for emojis
                    n_emos = len(objs)
                    for i, emoji in enumerate(objs):
                        objs_str += f"- {str(emoji)} {emoji.name}"
                        if ((i + 1) % 3 == 0) or ((i + 1) == n_emos):
                            objs_str += "\n"
                        else:
                            objs_str += " "
                else:  # for objs
                    objs.sort(key=lambda obj: obj.name)
                    for obj in objs:
                        objs_str += f"- {obj.id} - {obj.name}\n"
            else:  # no objs
                objs_str += f"\n{self.sep} No {TITLES[l_key][1]} {self.sep}\n"
        return objs_str

    def get_chans_cats_str(self):
        """Return the string for channels sorted by category and type"""
        cc_str = ""
        chans_cats = self.guild.by_category()
        if chans_cats:
            cc_str += f"\n\n{self.sep} CHANNELS BY CATEGORIES {self.sep}\n"
            for chans_cat in chans_cats:
                # title
                if chans_cat[0] is None:  # without category
                    cat_title = f"No {TITLES['cat'][1]}"
                else:  # with category
                    cat_title = chans_cat[0].name
                cc_str += f"\n##### {cat_title} #####\n"
                if chans_cat[1]:  # channels
                    for c_key in ['tcha', 'vcha', 'ncha', 'scha']:
                        chans = [c for c in chans_cat[1] if (
                            c.type == get_c_type(c_key))]
                        if chans:  # by type
                            cc_str += f"### {len(chans)} {TITLES[c_key][0]}\n"
                            chans.sort(key=lambda chan: chan.name)
                            for chan in chans:  # sorted list
                                cc_str += f"- {chan.id} - {chan.name}\n"
                else:  # No channels
                    cc_str += f"- No {TITLES['cha'][1]}\n"
        return cc_str
