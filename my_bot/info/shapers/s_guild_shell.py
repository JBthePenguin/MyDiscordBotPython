from discord import ChannelType
from .s_titles import GUILD_TITLES as titles


def get_tup_titles_list(guild):
    """Return a list of tuples with titles and corresponding guild list.
    -> [(titles, list), (titles, list), ...]"""
    return [
        (titles['gld'], [guild]), (titles['own'], [guild.owner]),
        (titles['mem'], guild.members), (titles['rol'], guild.roles),
        (titles['cat'], guild.categories),
        (titles['cha'], [
            c for c in guild.channels if c.type != ChannelType.category]),
        (titles['tcha'], [
            c for c in guild.text_channels if not c.is_news()]),
        (titles['vcha'], guild.voice_channels),
        (titles['ncha'], [
            c for c in guild.channels if c.type == ChannelType.news]),
        (titles['scha'], [
            c for c in guild.channels if c.type == ChannelType.store]),
        (titles['emo'], guild.emojis)]


def get_tup_type_titles():
    """Return a list of tuples with channel type and corresponding titles.
    -> [(c_type, titles), (c_type, titles), ...]"""
    return [
        (ChannelType.text, titles['tcha']),
        (ChannelType.voice, titles['vcha']),
        (ChannelType.news, titles['ncha']),
        (ChannelType.store, titles['scha'])]


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
        i = 0
        for emoji in emojis:
            self.infos += f"- {str(emoji)} {emoji.name} "
            if i == 2:
                self.infos += "\n"
                i = 0
            else:
                i += 1

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
                    self.infos += f"\n##### No {titles['cat'][1]} #####\n"
                else:
                    self.infos += f"\n##### {chans_cat[0].name} #####\n"
                if chans_cat[1]:
                    for t_tls in get_tup_type_titles():
                        self.add_type_chans(
                            [c for c in chans_cat[1] if (c.type == t_tls[0])],
                            t_tls[1][0])
                else:
                    self.infos += f"- No {titles['cha'][1]}\n"

    def add_infos(self):
        """Construct a string with all guild's infos."""
        for corres_tup in get_tup_titles_list(self.guild):
            self.add_list(corres_tup[0], corres_tup[1])
        # Channels by Category
        self.add_cats_chans(self.guild.by_category())
