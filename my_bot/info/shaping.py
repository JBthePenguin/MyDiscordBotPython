from discord import Embed, ChannelType
from .config import (
    title_gld, title_own, title_mem, title_rol, title_cat, title_cha,
    title_tcha, title_vcha, title_pcha, title_gcha, title_ncha, title_scha,
    title_emo)


class GuildEmbed(Embed):
    """ Embed for Guild """

    def __init__(self, name, icon_url):
        """ Init an embed with color, guild name and icon_url """
        super().__init__(color=0x161616)
        self.set_author(name=name, icon_url=icon_url)

    def add_title_objs(self, conf_embed, objs):
        """ add title, add fields id and name, add each obj sorted by name"""
        if not objs:  # no obj
            self.title = conf_embed.no_obj
        else:
            self.title = conf_embed.default
            if self.title == 'Emojis':  # for emoji
                self.add_emojis(objs)
            else:
                objs.sort(key=lambda obj: obj.name)
                ids = "\n".join([str(obj.id) for obj in objs])
                names = "\n".join([obj.name for obj in objs])
                self.add_field(name='ID', value=ids, inline=True)
                self.add_field(name='Name', value=names, inline=True)

    def add_emojis(self, emojis):
        """ add emojis(tuple) symbol and name, separate in 2 fields """
        half_n_emo = len(emojis) // 2
        first_emos = [emo for emo in emojis[half_n_emo:]]
        second_emos = [emo for emo in emojis[:half_n_emo]]
        first_field = "\n\n".join([
            f'{str(emoji)} {emoji.name}' for emoji in first_emos])
        second_field = "\n\n".join([
            f'{str(emoji)} {emoji.name}' for emoji in second_emos])
        self.add_field(name='\u200b', value=first_field, inline=True)
        self.add_field(name='\u200b', value=second_field, inline=True)


class GuildShell():
    """ String for guild """

    def __init__(self, guild):
        """ Init a string for infos with guild id and name """
        self.guild = guild
        self.infos = ''

    def add_list(self, title, objs):
        """ add a list with a title to infos string """
        if not objs:
            self.infos += f"\n########## {title.no_obj} ##########\n"
        else:
            self.infos += f"\n########## {title.default} ##########\n"
            if title.default == 'Emojis':
                self.add_emojis(objs)
            else:
                objs.sort(key=lambda obj: obj.name)
                for obj in objs:
                    self.infos += f"- {obj.id} - {obj.name}\n"

    def add_emojis(self, emojis):
        """ add a tuple of emojis """
        i = 0
        for emoji in emojis:
            self.infos += f"- {str(emoji)} {emoji.name} "
            if i == 2:
                self.infos += "\n"
                i = 0
            else:
                i += 1

    def add_infos(self):
        """ Construct a string with all guild's infos """
        # guild and owner
        self.add_list(title_gld, [self.guild])
        self.add_list(title_own, [self.guild.owner])
        # members, roles, channel's categories, channels
        self.add_list(title_mem, self.guild.members)
        self.add_list(title_rol, self.guild.roles)
        self.add_list(title_cat, self.guild.categories)
        self.add_list(
            title_cha,
            [c for c in self.guild.channels if c.type != ChannelType.category])
        # text, voice, private, group, news and store channels
        self.add_list(title_tcha, self.guild.text_channels)
        self.add_list(title_vcha, self.guild.voice_channels)
        self.add_list(
            title_pcha,
            [c for c in self.guild.channels if c.type == ChannelType.private])
        self.add_list(
            title_gcha,
            [c for c in self.guild.channels if c.type == ChannelType.group])
        self.add_list(
            title_ncha,
            [c for c in self.guild.channels if c.type == ChannelType.news])
        self.add_list(
            title_scha,
            [c for c in self.guild.channels if c.type == ChannelType.store])
        # Emojis
        self.add_list(title_emo, self.guild.emojis)


# for chans_cat in guild.by_category():
# if chans_cat[0] is None:
# if not chans_cat[1]:
# for channel in chans_cat[1]: