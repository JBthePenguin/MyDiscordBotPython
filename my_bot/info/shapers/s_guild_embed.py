from discord import Embed, ChannelType
from ..config import GUILD_TITLES as titles


def get_tup_titles_list(guild):
    """Return a list of tuples with titles and corresponding guild list.
    -> [(titles, list), (titles, list), ...]"""
    return [
        (titles.mem, guild.members), (titles.rol, guild.roles),
        (titles.emo, guild.emojis), (titles.cat, guild.categories),
        (titles.cha, [
            c for c in guild.channels if c.type != ChannelType.category]),
        (titles.tcha, [
            c for c in guild.text_channels if not c.is_news()]),
        (titles.vcha, guild.voice_channels),
        (titles.ncha, [
            c for c in guild.channels if c.type == ChannelType.news]),
        (titles.scha, [
            c for c in guild.channels if c.type == ChannelType.store])]


class GuildEmbed(Embed):
    """Embed for a Guild."""

    def __init__(self, name, icon_url):
        """Init an embed with color, guild name and icon_url."""
        super().__init__(color=0x161616)
        self.set_author(name=name, icon_url=icon_url)

    def add_stat(self, title, objs):
        """Add a field, set name with default title,
        and value with the number of objs."""
        self.add_field(name=title.default, value=str(len(objs)), inline=True)

    def add_title_stats(self, guild):
        """Add title with owner name,
        add fields for guild's stats (number of members, roles,...)."""
        self.title = f"id: {guild.id}"
        for corres_tup in get_tup_titles_list(guild):
            self.add_stat(corres_tup[0], corres_tup[1])
        self.set_footer(text=f"{titles.own.default}: {guild.owner.name}")

    def add_title_objs(self, conf_embed, objs):
        """Add title, add fields id and name, add each obj sorted by name."""
        if objs:
            self.title = conf_embed.default
            if self.title == 'Emojis':  # for emoji
                self.add_emojis(objs)
            else:
                objs.sort(key=lambda obj: obj.name)
                for tup_name_value in [
                        ('ID', [str(obj.id) for obj in objs]),
                        ('Name', [obj.name for obj in objs])]:
                    self.add_field(
                        name=tup_name_value[0],
                        value="\n".join(tup_name_value[1]), inline=True)
            self.set_footer(text=f"Total: {str(len(objs))}")
        else:  # no obj
            self.title = conf_embed.no_obj

    def add_emojis(self, emojis):
        """Add emojis(tuple) symbol and name, separate in 2 fields."""
        half_n_emo = len(emojis) // 2
        for emos in [
                [emo for emo in emojis[half_n_emo:]],
                [emo for emo in emojis[:half_n_emo]]]:
            field = "\n\n".join(
                [f'{str(emoji)} {emoji.name}' for emoji in emos])
            self.add_field(name='\u200b', value=field, inline=True)
