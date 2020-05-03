from .s_titles import TYPE_TITLES, get_s_tup_titles_list


class GuildShell():
    """String for a Guild."""

    def __init__(self, guild):
        """Init a string for infos with guild id and name."""
        self.guild = guild
        self.infos = ''

    def add_list(self, l_titles, objs):
        """Add a list with a title to infos string."""
        if objs:
            if (l_titles[0] == 'Guild') or (l_titles[0] == 'Owner'):
                n_objs = ''
            else:
                n_objs = str(len(objs))
            self.infos += f"\n########## {n_objs} {l_titles[0]} ##########\n"
            if l_titles[0] == 'Emojis':
                self.add_emojis(objs)
            else:
                objs.sort(key=lambda obj: obj.name)
                for obj in objs:
                    self.infos += f"- {obj.id} - {obj.name}\n"
        else:
            self.infos += f"\n########## No {l_titles[1]} ##########\n"

    def add_emojis(self, emojis):
        """Add a tuple of emojis (3 by line)."""
        for i in range(len(emojis)):
            emoji = emojis[i]
            self.infos += f"- {str(emoji)} {emoji.name} "
            if (i + 1) % 3 == 0:
                self.infos += "\n"
        if (i + 1) % 3 != 0:
            self.infos += "\n"

    def add_type_chans(self, chans, c_title):
        """Add channels with a specific type(title)."""
        if chans:
            self.infos += f"### {str(len(chans))} {c_title}\n"
            chans.sort(key=lambda chan: chan.name)
            for chan in chans:
                self.infos += f"- {chan.id} - {chan.name}\n"

    def add_cats_chans(self, chans_cats):
        """Add channels by category and type."""
        if chans_cats:
            self.infos += "\n\n########## CHANNELS BY CATEGORIES ##########\n"
            for chans_cat in chans_cats:
                if chans_cat[0] is None:
                    self.infos += "\n##### No channel category #####\n"
                else:
                    self.infos += f"\n##### {chans_cat[0].name} #####\n"
                if chans_cat[1]:
                    for t_tls in TYPE_TITLES:
                        self.add_type_chans(
                            [c for c in chans_cat[1] if (c.type == t_tls[0])],
                            t_tls[1][0])
                else:
                    self.infos += f"- No channel\n"

    def add_infos(self):
        """Construct a string with all guild's infos."""
        for corres_tup in get_s_tup_titles_list(self.guild):
            self.add_list(corres_tup[0], corres_tup[1])
        # Channels by Category
        self.add_cats_chans(self.guild.by_category())
