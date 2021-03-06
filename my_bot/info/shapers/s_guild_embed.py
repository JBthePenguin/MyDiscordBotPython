from discord import Embed
from .s_titles import TITLES
from .s_utils import get_list


class GuildEmbed(Embed):
    """Embed for a Guild."""

    def __init__(self, guild, com_key):
        """Init an embed with color, guild name and icon_url.
        -> add all guild's stats if from guild command."""
        super().__init__(color=0x161616)
        self.set_author(name=guild.name, icon_url=guild.icon_url)
        if com_key == 'gld':
            self.add_guild_stats(guild)
        else:
            self.add_objs_list(guild, com_key)

    def add_guild_stats(self, guild):
        """Add title with id and footer with owner name.
        and fields for all guild's stats (number of members, roles,...)."""
        self.title = f"id: {guild.id}"
        for com_key in [
                'mem', 'rol', 'emo', 'cat', 'cha',
                'tcha', 'vcha', 'ncha', 'scha']:
            self.add_field(
                name=TITLES[com_key][0],
                value=str(len(get_list(guild, com_key))), inline=True)
        self.set_footer(text=f"{TITLES['own'][0]}: {guild.owner.name}")

    def add_objs_list(self, guild, com_key):
        """Add title, add fields id and name, add each obj sorted by name,
        or call add_emojis if it's emo, ste footer with total objs.
        Or place no obj message in title."""
        objs = get_list(guild, com_key)
        if objs:
            self.title = TITLES[com_key][0]
            if com_key == 'emo':  # for emojis
                self.add_emojis(objs)
            else:  # for objs
                objs.sort(key=lambda obj: obj.name)
                for tup_name_value in [
                        ('ID', [str(obj.id) for obj in objs]),
                        ('Name', [obj.name for obj in objs])]:
                    self.add_field(
                        name=tup_name_value[0],
                        value="\n".join(tup_name_value[1]), inline=True)
            self.set_footer(text=f"Total: {str(len(objs))}")
        else:  # no objs
            self.title = f"No {TITLES[com_key][1]}"

    def add_emojis(self, emojis):
        """Add emojis(tuple) symbol and name, separate in 2 fields."""
        half_n_emo = len(emojis) // 2
        for emos in [
                [emo for emo in emojis[half_n_emo:]],
                [emo for emo in emojis[:half_n_emo]]]:
            field = "\n\n".join(
                [f'{str(emoji)} {emoji.name}' for emoji in emos])
            self.add_field(name='\u200b', value=field, inline=True)
