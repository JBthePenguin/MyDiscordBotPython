from discord import Embed


def info_in_shell(guild):
    """ Display infos (id, name) in shell for a specific guild
    - members -roles - channels by category"""
    print('###########')  # guild
    print("Guild id: {} - {}".format(guild.id, guild.name))
    print('###########')  # members
    for member in guild.members:
        print("Member id: {} - {}".format(member.id, member.name))
    print('#####')  # roles
    for role in guild.roles:
        print("Role id: {} - {}".format(role.id, role.name))
    for chans_by_cat in guild.by_category():  # channel categories
        print('#####')
        if chans_by_cat[0] is None:
            print("No category")
        else:
            print(
                "Category id: {} - {}".format(
                    chans_by_cat[0].id, chans_by_cat[0].name))
        for channel in chans_by_cat[1]:  # channels
            print(
                "-- Chan -- id: {} - {}".format(channel.id, channel.name))


def list_in_embed(objs, author_name, icon_url, title="Members"):
    """ Return an embed with a specific list """
    objs_ids = "\n".join(str(obj.id) for obj in objs)
    objs_names = "\n".join(obj.name for obj in objs)
    embed = Embed(title=title, color=0x161616)
    embed.set_author(name=author_name, icon_url=icon_url)
    embed.add_field(name='ID', value=objs_ids, inline=True)
    embed.add_field(name='Name', value=objs_names, inline=True)
    return embed
