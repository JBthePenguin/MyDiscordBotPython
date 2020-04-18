from discord import Embed, ChannelType
from .config import (
    title_gld, title_own, title_mem, title_rol, title_cat, title_cha,
    title_tcha, title_vcha, title_ncha, title_scha, title_emo)


class GuildEmbed(Embed):
    """ Embed for Guild """

    def __init__(self, name, icon_url):
        """ Init an embed with color, guild name and icon_url """
        super().__init__(color=0x161616)
        self.set_author(name=name, icon_url=icon_url)

    def add_stat(self, title, objs):
        """ add a field, set name with default title
        and set value with the number of objs """
        self.add_field(name=title.default, value=str(len(objs)), inline=True)

    def add_title_stats(self, guild):
        """ add title with owner name,
        add fields for guild's stats (number of members, roles,...) """
        self.title = f"id: {guild.id}"
        self.add_stat(title_mem, guild.members)
        self.add_stat(title_rol, guild.roles)
        self.add_stat(title_emo, guild.emojis)
        self.add_stat(title_cat, guild.categories)
        self.add_stat(
            title_cha,
            [c for c in guild.channels if c.type != ChannelType.category])
        self.add_stat(
            title_tcha,
            [c for c in guild.text_channels if not c.is_news()])
        self.add_stat(title_vcha, guild.voice_channels)
        self.add_stat(
            title_ncha,
            [c for c in guild.channels if c.type == ChannelType.news])
        self.add_stat(
            title_scha,
            [c for c in guild.channels if c.type == ChannelType.store])
        self.set_footer(text=f"{title_own.default}: {guild.owner.name}")

    def add_title_objs(self, conf_embed, objs):
        """ add title, add fields id and name, add each obj sorted by name"""
        if objs:
            self.title = conf_embed.default
            if self.title == 'Emojis':  # for emoji
                self.add_emojis(objs)
            else:
                objs.sort(key=lambda obj: obj.name)
                ids = "\n".join([str(obj.id) for obj in objs])
                names = "\n".join([obj.name for obj in objs])
                self.add_field(name='ID', value=ids, inline=True)
                self.add_field(name='Name', value=names, inline=True)
            self.set_footer(text=f"Total: {str(len(objs))}")
        else:  # no obj
            self.title = conf_embed.no_obj

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
        if objs:
            if (title.default == 'Guild') or (title.default == 'Owner'):
                n_objs = ''
            else:
                n_objs = str(len(objs))
            self.infos += f"\n########## {n_objs} {title.default} ##########\n"
            if title.default == 'Emojis':
                self.add_emojis(objs)
            else:
                objs.sort(key=lambda obj: obj.name)
                for obj in objs:
                    self.infos += f"- {obj.id} - {obj.name}\n"
        else:
            self.infos += f"\n########## {title.no_obj} ##########\n"

    def add_emojis(self, emojis):
        """ add a tuple of emojis (3 by line)"""
        i = 0
        for emoji in emojis:
            self.infos += f"- {str(emoji)} {emoji.name} "
            if i == 2:
                self.infos += "\n"
                i = 0
            else:
                i += 1

    def add_type_chans(self, chans, title):
        """ add channels with a specific type(title) """
        if chans:
            self.infos += f"### {str(len(chans))} {title.default}\n"
            chans.sort(key=lambda chan: chan.name)
            for chan in chans:
                self.infos += f"- {chan.id} - {chan.name}\n"

    def add_cats_chans(self, chans_cats):
        """ add channels by category and type """
        if chans_cats:
            self.infos += "\n\n########## CHANNELS BY CATEGORIES ##########\n"
            for chans_cat in chans_cats:
                if chans_cat[0] is None:
                    self.infos += f"\n##### {title_cat.no_obj} #####\n"
                else:
                    self.infos += f"\n##### {chans_cat[0].name} #####\n"
                if chans_cat[1]:
                    self.add_type_chans(
                        [c for c in chans_cat[1] if (
                            c.type == ChannelType.text)], title_tcha)
                    self.add_type_chans(
                        [c for c in chans_cat[1] if (
                            c.type == ChannelType.voice)], title_vcha)
                    self.add_type_chans(
                        [c for c in chans_cat[1] if (
                            c.type == ChannelType.news)], title_ncha)
                    self.add_type_chans(
                        [c for c in chans_cat[1] if (
                            c.type == ChannelType.store)], title_scha)
                else:
                    self.infos += f"- {title_cha.no_obj}\n"

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
        self.add_list(
            title_tcha,
            [c for c in self.guild.text_channels if not c.is_news()])
        self.add_list(title_vcha, self.guild.voice_channels)
        self.add_list(
            title_ncha,
            [c for c in self.guild.channels if c.type == ChannelType.news])
        self.add_list(
            title_scha,
            [c for c in self.guild.channels if c.type == ChannelType.store])
        # Emojis
        self.add_list(title_emo, self.guild.emojis)
        # Channels by Category
        self.add_cats_chans(self.guild.by_category())
