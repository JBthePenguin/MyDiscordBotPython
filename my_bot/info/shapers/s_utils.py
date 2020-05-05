from discord import ChannelType


def get_list(guild, com_key):
    """Return the corresponding guild's list for a specific command key."""
    if com_key == 'mem':
        return guild.members
    elif com_key == 'rol':
        return guild.roles
    elif com_key == 'emo':
        return guild.emojis
    elif com_key == 'cat':
        return guild.categories
    elif com_key == 'cha':
        return [c for c in guild.channels if c.type != ChannelType.category]
    elif com_key == 'tcha':
        return [c for c in guild.text_channels if not c.is_news()]
    elif com_key == 'vcha':
        return guild.voice_channels
    elif com_key == 'ncha':
        return [c for c in guild.text_channels if c.is_news()]
    elif com_key == 'scha':
        return [c for c in guild.channels if c.type == ChannelType.store]


def get_c_type(com_key):
    """Return the corresponding channel type for a specific command key"""
    if com_key == 'tcha':
        return ChannelType.text
    elif com_key == 'vcha':
        return ChannelType.voice
    elif com_key == 'ncha':
        return ChannelType.news
    elif com_key == 'scha':
        return ChannelType.store
