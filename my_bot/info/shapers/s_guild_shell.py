from discord import ChannelType
from ..config import GUILD_TITLES as titles


class GuildShell():
    """String for a Guild."""

    def __init__(self, guild):
        """Init a string for infos with guild id and name."""
        self.guild = guild
        self.infos = ''

    def add_list(self, title, objs):
        """Add a list with a title to infos string."""
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
        """Add a tuple of emojis (3 by line)."""
        i = 0
        for emoji in emojis:
            self.infos += f"- {str(emoji)} {emoji.name} "
            if i == 2:
                self.infos += "\n"
                i = 0
            else:
                i += 1

    def add_type_chans(self, chans, title):
        """Add channels with a specific type(title)."""
        if chans:
            self.infos += f"### {str(len(chans))} {title.default}\n"
            chans.sort(key=lambda chan: chan.name)
            for chan in chans:
                self.infos += f"- {chan.id} - {chan.name}\n"

    def add_cats_chans(self, chans_cats):
        """Add channels by category and type."""
        if chans_cats:
            self.infos += "\n\n########## CHANNELS BY CATEGORIES ##########\n"
            for chans_cat in chans_cats:
                if chans_cat[0] is None:
                    self.infos += f"\n##### {titles.cat.no_obj} #####\n"
                else:
                    self.infos += f"\n##### {chans_cat[0].name} #####\n"
                if chans_cat[1]:
                    self.add_type_chans(
                        [c for c in chans_cat[1] if (
                            c.type == ChannelType.text)], titles.tcha)
                    self.add_type_chans(
                        [c for c in chans_cat[1] if (
                            c.type == ChannelType.voice)], titles.vcha)
                    self.add_type_chans(
                        [c for c in chans_cat[1] if (
                            c.type == ChannelType.news)], titles.ncha)
                    self.add_type_chans(
                        [c for c in chans_cat[1] if (
                            c.type == ChannelType.store)], titles.scha)
                else:
                    self.infos += f"- {titles.cha.no_obj}\n"

    def add_infos(self):
        """Construct a string with all guild's infos."""
        # guild and owner
        self.add_list(titles.gld, [self.guild])
        self.add_list(titles.own, [self.guild.owner])
        # members, roles, channel's categories, channels
        self.add_list(titles.mem, self.guild.members)
        self.add_list(titles.rol, self.guild.roles)
        self.add_list(titles.cat, self.guild.categories)
        self.add_list(
            titles.cha,
            [c for c in self.guild.channels if c.type != ChannelType.category])
        # text, voice, private, group, news and store channels
        self.add_list(
            titles.tcha,
            [c for c in self.guild.text_channels if not c.is_news()])
        self.add_list(titles.vcha, self.guild.voice_channels)
        self.add_list(
            titles.ncha,
            [c for c in self.guild.channels if c.type == ChannelType.news])
        self.add_list(
            titles.scha,
            [c for c in self.guild.channels if c.type == ChannelType.store])
        # Emojis
        self.add_list(titles.emo, self.guild.emojis)
        # Channels by Category
        self.add_cats_chans(self.guild.by_category())
