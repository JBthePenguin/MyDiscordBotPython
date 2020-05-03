from discord import Embed
from .s_titles import get_tup_titles_list, get_titles


class GuildEmbed(Embed):
    """Embed for a Guild."""

    def __init__(self, name, icon_url):
        """Init an embed with color, guild name and icon_url."""
        super().__init__(color=0x161616)
        self.set_author(name=name, icon_url=icon_url)

    def add_stat(self, o_title, objs):
        """Add a field, set name with title and value with number of objs."""
        self.add_field(name=o_title, value=str(len(objs)), inline=True)

    def add_title_stats(self, guild):
        """Add title with owner name,
        add fields for guild's stats (number of members, roles,...)."""
        self.title = f"id: {guild.id}"
        for corres_tup in get_tup_titles_list(guild):
            self.add_stat(corres_tup[0][0], corres_tup[1])
        self.set_footer(text=f"Owner: {guild.owner.name}")

    def add_title_objs(self, titles_key, objs):
        """Add title, add fields id and name, add each obj sorted by name."""
        if objs:
            self.title = get_titles(titles_key)[0]
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
            self.title = f"No {get_titles(titles_key)[1]}"

    def add_emojis(self, emojis):
        """Add emojis(tuple) symbol and name, separate in 2 fields."""
        half_n_emo = len(emojis) // 2
        for emos in [
                [emo for emo in emojis[half_n_emo:]],
                [emo for emo in emojis[:half_n_emo]]]:
            field = "\n\n".join(
                [f'{str(emoji)} {emoji.name}' for emoji in emos])
            self.add_field(name='\u200b', value=field, inline=True)
