from discord.enums import ChannelType
from .f_member import FakeUser
from .f_guild import FakeGuild
from .f_context import FakeContext

# ROLES -> [(name, position, all permissions(bool)), ..]
ROLES = [
    ('admin', 2, True),
    ('staff', 1, False)]

# MEMBERS -> [(FakeUser(username), [role name 1, role name 2, ..]), ...]
OWNER = FakeUser(username='Jean-Pierre')
MEMBERS = [
    (OWNER, ['admin']),
    (FakeUser(username='Al'), ['admin']),
    (FakeUser(username='Joe'), ['staff']),
    (FakeUser(username='Billy'), ['staff']),
    (FakeUser(username='John'), []),
    (FakeUser(username='Mike'), []), ]

# CHANNELS_CATEGORIES -> [(parent category name or None, name, position,
# [role name 1, role name 2, ..], [member name 1, member name 2, ..])
# *** roles and members used for permission overwrites
CHANNELS_CATEGORIES = [
    (None, '1st floor', 1, [], []),
    (None, '2nd floor', 1, [], [])]

# CHANNELS -> [(parent category name or None, name, type, position,
# [role name 1, role name 2, ..] or '@everyone', [member name 1, ..])
# *** roles and members used for permission overwrites
CHANNELS = [
    (None, 'reception', ChannelType.text.value, 3, '@everyone', []),
    (None, 'info point', ChannelType.news.value, 3, '@everyone', []),
    ('1st floor', 'shop', ChannelType.store.value, 3, '@everyone', []),
    ('1st floor', 'snack', ChannelType.voice.value, 2, ['staff'], ['John']),
    ('1st floor', 'studio', ChannelType.voice.value, 2, ['staff'], []),
    ('2nd floor', 'meeting room', ChannelType.text.value, 2, [], ['Joe']),
    ('2nd floor', 'boss office', ChannelType.text.value, 2, [], []), ]

# EMOJIS -> [emoji name 1, emoji name 2, ...]
EMOJIS = ['cool', 'good', 'bad', 'strong']

# FULL_GUILD
FULL_GUILD = FakeGuild(
    name="Full guild", roles=ROLES, members=MEMBERS,
    categories=CHANNELS_CATEGORIES, channels=CHANNELS, emojis=EMOJIS)

# CONTEXT
CONTEXT = FakeContext(FULL_GUILD)
