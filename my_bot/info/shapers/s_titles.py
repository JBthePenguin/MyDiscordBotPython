from discord import ChannelType

# All titles used for shaping guild infos."""
# singular and plurial except for guild and owner
TITLES = {
    # guild, owner
    'gld': ('Guild', 'guild'), 'own': ('Owner', 'owner'),
    # members, roles, channel's categories, channels, emojis
    'mem': ('Members', 'member'), 'rol': ('Roles', 'role'),
    'cat': ('Channel Categories', 'channel category'),
    'cha': ('Channels', 'channel'), 'emo': ('Emojis', 'emoji'),
    # text, voice, news and store channels
    'tcha': ('Text Channels', 'text channel'),
    'vcha': ('Voice Channels', 'voice channel'),
    'ncha': ('News Channels', 'news channel'),
    'scha': ('Store Channels', 'store channel')}


def get_titles(titles_key):
    """return titles for a specific key"""
    return TITLES[titles_key]


def get_tup_titles_list(guild):
    """Return a list of tuples with titles and corresponding guild list.
    -> [(titles, list), (titles, list), ...]"""
    return [
        (TITLES['mem'], guild.members), (TITLES['rol'], guild.roles),
        (TITLES['emo'], guild.emojis), (TITLES['cat'], guild.categories),
        (TITLES['cha'], [
            c for c in guild.channels if c.type != ChannelType.category]),
        (TITLES['tcha'], [
            c for c in guild.text_channels if not c.is_news()]),
        (TITLES['vcha'], guild.voice_channels),
        (TITLES['ncha'], [
            c for c in guild.channels if c.type == ChannelType.news]),
        (TITLES['scha'], [
            c for c in guild.channels if c.type == ChannelType.store])]


def get_s_tup_titles_list(guild):
    """Return a list of tuples with titles and corresponding guild list.
    for shell -> [(titles, list), (titles, list), ...]"""
    tup_titles_list = get_tup_titles_list(guild)
    tup_titles_list.insert(0, (TITLES['gld'], [guild]))
    tup_titles_list.insert(1, (TITLES['own'], [guild.owner]))
    return tup_titles_list


# list of tuples with channel type and corresponding titles.
# -> [(c_type, titles), (c_type, titles), ...]"""
TYPE_TITLES = [
    (ChannelType.text, TITLES['tcha']),
    (ChannelType.voice, TITLES['vcha']),
    (ChannelType.news, TITLES['ncha']),
    (ChannelType.store, TITLES['scha'])]
