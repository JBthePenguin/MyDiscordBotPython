from discord import Embed, ChannelType
# from .config import confs_guild as confs
#  from .checking import empty_content


class GuildEmbed(Embed):
    """ Embed for Guild """

    def __init__(self, name, icon_url):
        """ Init an embed with color, author name and icon_url """
        super().__init__(color=0x161616)
        self.set_author(name=name, icon_url=icon_url)

    def add_title_objs(self, conf_embed, objs):
        """ add title, add fields id and name, add each obj sorted by name"""
        if not objs:  # no obj
            self.title = f"No {conf_embed.obj_type}"
        else:
            self.title = conf_embed.title
            if conf_embed.obj_type == 'emoji':  # for emoji
                self.add_emojis(objs)
            else:
                objs.sort(key=lambda obj: obj.name)
                ids = "\n".join([str(obj.id) for obj in objs])
                names = "\n".join([obj.name for obj in objs])
                self.add_field(name='ID', value=ids, inline=True)
                self.add_field(name='Name', value=names, inline=True)

    def add_emojis(self, emojis):
        """ Return an embed with a tuple of emojis """
        half_n_emo = len(emojis) // 2
        first_emos = [emo for emo in emojis[half_n_emo:]]
        second_emos = [emo for emo in emojis[:half_n_emo]]
        first_field = "\n\n".join([
            f'{str(emoji)} {emoji.name}' for emoji in first_emos])
        second_field = "\n\n".join([
            f'{str(emoji)} {emoji.name}' for emoji in second_emos])
        self.add_field(name='\u200b', value=first_field, inline=True)
        self.add_field(name='\u200b', value=second_field, inline=True)


def print_list(title, name, objs_checked, confs_key):
    """ Print a list in shell with a title """
    # objs_checked = empty_content(objs, name, confs[confs_key]['obj_type'])
    if isinstance(objs_checked, str):
        print('\n' + objs_checked)
    else:
        print(title)
        objs_checked.sort(key=lambda obj: obj.name)
        for obj in objs_checked:
            print("id: {} - {}".format(obj.id, obj.name))


def info_in_shell(guild):
    """ Display infos (id, name) in shell for a specific guild
    - members -roles - channels by category and type"""
    print("\n############## GUILD #######\nid: {} - {}".format(
        guild.id, guild.name))
    print("### Owner ###\nid: {} - {}".format(
        guild.owner.id, guild.owner.name))
    print_list('\n########## MEMBERS #####', guild.name, guild.members, 'mem')
    print_list('\n########## ROLES #####', guild.name, guild.roles, 'rol')
    print('\n########## CHANNELS BY CATEGORY #####')
    if not guild.by_category():
        print('\n{}: no category, no channel'.format(guild.name))
    else:
        for chans_cat in guild.by_category():
            print('\n###### CATEGORY ###')
            if chans_cat[0] is None:
                print("No category")
            else:
                print("id: {} - {}".format(chans_cat[0].id, chans_cat[0].name))
            print('#### CHANNELS ##')
            if not chans_cat[1]:
                print('No Channel')
            else:
                t_ch, v_ch, p_ch, g_ch, n_ch, s_ch = [], [], [], [], [], []
            for channel in chans_cat[1]:
                if channel.type == ChannelType.text:
                    t_ch.append(channel)
                elif channel.type == ChannelType.voice:
                    v_ch.append(channel)
                elif channel.type == ChannelType.private:
                    p_ch.append(channel)
                elif channel.type == ChannelType.group:
                    g_ch.append(channel)
                elif channel.type == ChannelType.news:
                    n_ch.append(channel)
                elif channel.type == ChannelType.store:
                    s_ch.append(channel)
            print_list('## TEXT CHANNELS ', chans_cat[0].name, t_ch, 'tcha')
            print_list('## VOICE CHANNELS ', chans_cat[0].name, v_ch, 'vcha')
            print_list('## PRIVATE CHANNELS ', chans_cat[0].name, p_ch, 'pcha')
            print_list('## GROUP CHANNELS ', chans_cat[0].name, g_ch, 'gcha')
            print_list('## NEWS CHANNELS ', chans_cat[0].name, n_ch, 'ncha')
            print_list('## STORE CHANNELS ', chans_cat[0].name, s_ch, 'scha')
